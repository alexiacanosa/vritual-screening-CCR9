import torch
from torch_geometric.data import Data
from rdkit import Chem
import numpy as np
import networkx as nx

from gnn import GNNNet  
import warnings
warnings.filterwarnings("ignore")

# ==============================================================
# --- Basic one-hot helpers
# ==============================================================
def one_of_k_encoding(x, allowable_set):
    if x not in allowable_set:
        raise ValueError(f"Input {x} not in allowable set {allowable_set}")
    return [x == s for s in allowable_set]


def one_of_k_encoding_unk(x, allowable_set):
    """Unknown entries go to last element."""
    if x not in allowable_set:
        x = allowable_set[-1]
    return [x == s for s in allowable_set]

# ==============================================================
# --- Atom feature function (78-dimensional)
# ==============================================================
def atom_features(atom):
    return np.array(
        one_of_k_encoding_unk(atom.GetSymbol(),
            ['C','N','O','S','F','Si','P','Cl','Br','Mg','Na','Ca','Fe','As',
             'Al','I','B','V','K','Tl','Yb','Sb','Sn','Ag','Pd','Co','Se',
             'Ti','Zn','H','Li','Ge','Cu','Au','Ni','Cd','In','Mn','Zr','Cr',
             'Pt','Hg','Pb','X']
        ) +
        one_of_k_encoding(atom.GetDegree(), list(range(11))) +
        one_of_k_encoding_unk(atom.GetTotalNumHs(), list(range(11))) +
        one_of_k_encoding_unk(atom.GetImplicitValence(), list(range(11))) +
        [atom.GetIsAromatic()]
    )

# ==============================================================
# --- Convert SMILES to molecular graph (78-dim atom features)
# ==============================================================
def mol_to_graph_features(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    atoms = mol.GetAtoms()
    x = torch.tensor([atom_features(a) for a in atoms], dtype=torch.float)

    # edges (bidirectional)
    edge_index = [[], []]
    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        edge_index[0] += [i, j]
        edge_index[1] += [j, i]

    edge_index = torch.tensor(edge_index, dtype=torch.long)

    data = Data(x=x, edge_index=edge_index)
    data.y = torch.zeros(1)
    return data

# ==============================================================
# --- Convert protein sequence to graph (54-dim residue features)
# ==============================================================
def seq_feature(seq):
    """Build protein residue graph with 54-dim features per residue."""
    amino_acids = list("ACDEFGHIKLMNPQRSTVWY")  # 20 types

    features = []
    for res in seq:
        features.append(one_of_k_encoding_unk(res, amino_acids))  # 20-dim
    features = np.array(features, dtype=float)

    # pad to 54 dims (model was trained with 54 features)
    if features.shape[1] < 54:
        pad = np.zeros((features.shape[0], 54 - features.shape[1]))
        features = np.concatenate([features, pad], axis=1)

    x = torch.tensor(features, dtype=torch.float)

    # sequential edges
    edge_index = [[], []]
    for i in range(len(seq) - 1):
        edge_index[0] += [i, i + 1]
        edge_index[1] += [i + 1, i]
    edge_index = torch.tensor(edge_index, dtype=torch.long)

    data = Data(x=x, edge_index=edge_index)
    data.y = torch.zeros(1)
    return data

# ==============================================================
# --- Load pretrained model (handles mismatched keys)
# ==============================================================
def load_model(model_path, device):
    checkpoint = torch.load(model_path, map_location=device)

    model = GNNNet().to(device)
    model_state = model.state_dict()
    new_state = {}

    for k, v in checkpoint.items():
        new_key = k

        # handle mismatches both ways
        if ".lin.weight" in k and k.replace(".lin.weight", ".weight") in model_state:
            new_key = k.replace(".lin.weight", ".weight")
        elif k.endswith(".weight") and not k.endswith(".lin.weight") and k.replace(".weight", ".lin.weight") in model_state:
            new_key = k.replace(".weight", ".lin.weight")

        # fix transposed matrices if needed
        if new_key in model_state:
            expected_shape = model_state[new_key].shape
            if v.shape[::-1] == expected_shape:
                v = v.T

        new_state[new_key] = v

    missing, unexpected = model.load_state_dict(new_state, strict=False)
    model.eval()
    return model


# ==============================================================
# --- Run inference for one drug–protein pair
# ==============================================================
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = "model_GNNNet_davis.model"

    # ------------------------------
    # Input: 1 drug + 1 protein | Output: prediction in pKd
    # ------------------------------
    drug_smiles = "CCC1=NN=C2N1C3=C(C4=C(S3)CCC4)C(=NC2)C5=CC=CC=C5Cl"  
    protein_seq = (
        "ASMEDYVNFNFEDFYCEKNNVRQFASHFLPPLYWLVFIVGALGNSLVILVYWYCARAKTATDMFLLNLAIADLLFLVTLPFWAIAAADQWKFQTFMCKVVNSMYKMNFYSCVLLIMCICVDRYIAIAQAMRAHTWREKRLLYSKMVCFTIWVLAAALCIPEILYSQIKEESGIAICTMVYPSDESTKLKSAVLALKVILGFFLPFVVMACCYTIIIHTLIQAKKSSKHKALKATITVLTVFVLSQFPYNCILLVQTIDAYAMFISNCAVSTAIDICFQVTQAIAFFHSCLNPVLYVFVGERFRRDLVKTLKNLGAISQAAAHHHHHHHHHH"
    )

    # ------------------------------
    # Convert inputs to graphs
    # ------------------------------
    mol_graph = mol_to_graph_features(drug_smiles)
    pro_graph = seq_feature(protein_seq)

    mol_graph = mol_graph.to(device)
    pro_graph = pro_graph.to(device)

    # ------------------------------
    # Load pretrained model
    # ------------------------------
    model = load_model(model_path, device)

    # ------------------------------
    # Run prediction
    # ------------------------------
    with torch.no_grad():
        pred = model(mol_graph, pro_graph)

    print("\nPredicted affinity:", float(pred))
    pKd = pred
    Kd = 10**(-pKd)                  # M
    ic50_simple = Kd                 # M, approx IC50 ≈ Kd
    # if you want Cheng-Prusoff with factor (1 + [S]/Km):
    factor = 2.0                     # example (e.g. [S]=Km)
    ic50_cp = Kd * factor

    # display in pM:
    print("Kd (M):",float(Kd))
    print("Kd (pM):", float(Kd*1e12))
    print("IC50 approx (pM):", float(ic50_simple*1e12))
    print("IC50 (pM) with factor", factor, ":", float(ic50_cp*1e12)) 