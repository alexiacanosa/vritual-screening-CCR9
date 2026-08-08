export async function parseProteinLigandCSV(file: File): Promise<{ protein_sequence: string; ligand_smiles: string }[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const text = reader.result as string;
        const lines = text.split("\n").filter((line) => line.trim() !== "");
        
        if (lines.length === 0) {
          throw new Error("CSV file is empty");
        }

        const firstLine = lines[0];
        const delimiter = firstLine.includes(";") ? ";" : firstLine.includes("\t") ? "\t" : ",";
        
        const firstLineParts = firstLine.split(delimiter).map(p => p.trim());
        const isHeaderRow = firstLineParts[0]?.toLowerCase().includes("protein") || 
                           firstLineParts[0]?.toLowerCase().includes("sequence");
        
        let proteinColIndex = 0;
        let ligandColIndex = 1;
        let dataStartIndex = 0;
        
        if (isHeaderRow) {
          const headers = firstLineParts.map(h => h.toLowerCase());
          proteinColIndex = headers.findIndex(h => h.includes("protein") || h.includes("sequence"));
          ligandColIndex = headers.findIndex(h => h.includes("ligand") || h.includes("smiles"));
          dataStartIndex = 1;
        }
        
        const rows = lines
          .slice(dataStartIndex)
          .map((line) => {
            const parts = line.split(delimiter).map(p => p.trim());
            const protein_sequence = parts[proteinColIndex];
            const ligand_smiles = parts[ligandColIndex];
            
            if (!protein_sequence || !ligand_smiles || protein_sequence === "" || ligand_smiles === "") {
              return null;
            }
            
            return { protein_sequence, ligand_smiles };
          })
          .filter((row) => row !== null) as { protein_sequence: string; ligand_smiles: string }[];
        
        if (rows.length === 0) {
          throw new Error("No valid rows found in CSV (each row needs both protein_sequence and ligand_smiles)");
        }
        
        console.log("[v0] Parsed CSV successfully:", rows.length, "valid rows found with delimiter:", delimiter);
        resolve(rows);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsText(file);
  });
}
