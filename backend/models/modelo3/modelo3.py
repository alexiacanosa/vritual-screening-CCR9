import torch
import scipy.sparse as sp
import numpy as np
import os

# --- Import ML Models ---
# These files MUST exist in the same directory.
# They are currently STUBS and must be replaced with your real model code.
from MINDG import MINDG
from HDN import get_model
from HOAGCN import MixHopNetwork, create_propagator_matrix, features_to_sparse

# --- Import Preprocessing ---
# You need to have DeepPurpose installed: pip install DeepPurpose
try:
    from DeepPurpose.dataset import data_process
except ImportError:
    print("Error: DeepPurpose library not found.")
    print("Please install it: pip install DeepPurpose")
    exit()

# -----------------------------
# 1. Device setup
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️ Using device: {device}")

# -----------------------------
# 2. Input Data (SMILES and Protein Sequence)
# -----------------------------
v_d_smiles = ["CCO"]  # Example Drug (Ethanol)
v_p_seq = ["MENFQKVEKIGEGTYGVVYKARNK"] # Example Protein Sequence

# --- Process Data ---
# We must convert strings to numerical vectors.
# NOTE: You MUST use the SAME encodings as your training data.
# These are common guesses, but may be wrong for your model.
DRUG_ENCODING = 'Morgan'
TARGET_ENCODING = 'Conjoint_triad'
print(f"🧬 Processing input data with encodings: Drug='{DRUG_ENCODING}', Target='{TARGET_ENCODING}'")

# data_process expects lists and a dummy 'y'
# We use 'no_split' to just get back the processed data
try:
    # --- FIX ---
    # data_process with no_split returns 5 values: X_drug, X_target, y, drug_names, target_names
    # We capture all 5 to avoid the "too many values to unpack" error.
    X_drug, X_target, _, _, _ = data_process(
        X_drug=v_d_smiles,
        X_target=v_p_seq,
        y=[0],  # Dummy label
        drug_encoding=DRUG_ENCODING,
        target_encoding=TARGET_ENCODING,
        split_method='no_split'
    )
except Exception as e:
    print(f"Error processing data with DeepPurpose: {e}")
    print("Are the encodings correct? Are SMILES/sequences valid?")
    exit()

# # --- NEW: Add validation check ---
# if not isinstance(X_drug, np.ndarray) or not np.issubdtype(X_drug.dtype, np.number):
#     print(f"--- 🚫 ERROR: Data processing failed ---")
#     print(f"DeepPurpose.data_process did not convert the SMILES string '{v_d_smiles[0]}' into numbers.")
#     print(f"Instead, X_drug is: {X_drug}")
#     print("This almost always means a dependency like 'rdkit-pypi' is missing or not installed correctly.")
#     print("Please make sure you have installed it in your environment:")
#     print("pip install rdkit-pypi")
#     exit()
# # --- End of new check ---

# Convert processed arrays to tensors
v_d = torch.tensor(X_drug, dtype=torch.float32).to(device)
v_p = torch.tensor(X_target, dtype=torch.float32).to(device)

print(f"Drug tensor shape: {v_d.shape}")   # e.g., [1, 1024] for Morgan
print(f"Protein tensor shape: {v_p.shape}") # e.g., [1, 147] for Conjoint_triad

# -----------------------------
# 3. Initialize HDN
# -----------------------------
# NOTE: This uses the STUB model from HDN.py
print("Initializing HDN model...")
hdn_model = get_model().model.to(device)

# -----------------------------
# 4. Initialize HOAGCN
# -----------------------------
# NOTE: This 'feature_number' is a critical magic number.
# It MUST match the number of nodes in the graph used for training.
feature_number = 6100
print(f"Initializing HOAGCN model with feature_number={feature_number}...")

# NOTE: This uses the STUB model from HOAGCN.py
hoagcn_model = MixHopNetwork(
    feature_number=feature_number,
    class_number=1,
    layers_1=[32, 32, 32, 32],
    layers_2=[32, 32, 32, 32],
    hidden1=64,
    hidden2=32,
    dropout=0.1,
    device=device
).to(device)

# -----------------------------
# 5. Create dummy propagation matrix + features
# -----------------------------
# This creates an identity matrix for A and features,
# assuming a featureless graph or one-hot node features.
# This MUST match your training setup.
print("Creating dummy graph inputs (propagation matrix & features)...")
A = sp.eye(feature_number, format="csr")

# NOTE: This uses the STUB function from HOAGCN.py
propagation_matrix = create_propagator_matrix(A, device)
# NOTE: This uses the STUB function from HOAGCN.py
features = features_to_sparse(np.eye(feature_number), device)

# -----------------------------
# 6. Combine into MINDG
# -----------------------------
print("Initializing MINDG model...")
# NOTE: This uses the STUB model from MINDG.py
model = MINDG(
    hdn_model=hdn_model,
    hoagcn_model=hoagcn_model,
    propagation_matrix=propagation_matrix,
    features=features,
    alpha=0.5
).to(device)

# -----------------------------
# 7. Load checkpoint & Run Inference
# -----------------------------
checkpoint_file = "mindg_BindingDB_Kd_epoch10.pt"
if not os.path.exists(checkpoint_file):
    print(f"--- ⚠️ WARNING ⚠️ ---")
    print(f"Checkpoint file not found: {checkpoint_file}")
    print("The script will continue with RANDOMLY INITIALIZED weights.")
    print("Predictions will be meaningless.")
    print("-------------------------")
else:
    try:
        print(f"Loading checkpoint from {checkpoint_file}...")
        checkpoint = torch.load(checkpoint_file, map_location=device)
        state_dict = checkpoint["state_dict"] if "state_dict" in checkpoint else checkpoint

        missing, unexpected = model.load_state_dict(state_dict, strict=False)
        if missing:
            print("⚠️ Missing keys:", missing)
        if unexpected:
            print("⚠️ Unexpected keys:", unexpected)
        
        print("✅ MINDG model weights loaded successfully!")
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        print("Running with initialized weights instead.")

model.eval()

# -----------------------------
# 8. Example inference
# -----------------------------
# NOTE: These indices (0 and 0) are magic numbers.
# They must correspond to the correct drug/protein nodes in your graph.
idx1 = torch.tensor([0]).to(device)
idx2 = torch.tensor([0]).to(device)

print("Running inference...")
try:
    with torch.no_grad():
        pred = model(v_d, v_p, idx1, idx2)

    print("-------------------------")
    print(f"🎯 Prediction: {pred.item() if torch.is_tensor(pred) else pred}")
    print("-------------------------")
    if not os.path.exists(checkpoint_file):
        print("(Note: This prediction is meaningless as no checkpoint was loaded.)")

except Exception as e:
    print(f"--- 🚫 INFERENCE FAILED 🚫 ---")
    print(f"An error occurred during model forward pass: {e}")
    print("This often happens if tensor dimensions from data processing (HDN)")
    print("or graph features (HOAGCN) do not match the model's architecture.")
    print("Please check your STUB models and input data processing.")
    print("-----------------------------")
