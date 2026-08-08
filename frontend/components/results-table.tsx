"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Download } from "lucide-react"

interface ResultRow {
  protein_sequence: string
  ligand_smiles: string
  model1_score?: number
  model2_score?: number
  model3_score?: number
  model4_score?: number
  weighted_ranking?: number
  error?: string
}

interface ResultsTableProps {
  data: ResultRow[]
}

const formatScore = (value?: number): string => {
  if (value === undefined || value === null) return "—"

  // notación científica
  if (Math.abs(value) < 0.0001 && value !== 0) {
    return value.toExponential(2)
  }

  // 4 decimales de normal
  return value.toFixed(4)
}

export function ResultsTable({ data }: ResultsTableProps) {
  if (!data || data.length === 0) {
    return null
  }

  const downloadCSV = () => {
    const headers = [
      "Index",
      "Protein Sequence",
      "Ligand SMILES",
      "Model 1",
      "Model 2",
      "Model 3",
      "Model 4",
      "Weighted Ranking",
      "Status",
    ]
    const csv = [
      headers.join(","),
      ...data.map((row, idx) =>
        [
          idx + 1,
          `"${row.protein_sequence}"`,
          `"${row.ligand_smiles}"`,
          formatScore(row.model1_score),
          formatScore(row.model2_score),
          formatScore(row.model3_score),
          formatScore(row.model4_score),
          formatScore(row.weighted_ranking),
          row.error ? `"Error: ${row.error}"` : "Success",
        ].join(","),
      ),
    ].join("\n")

    const blob = new Blob([csv], { type: "text/csv" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "results.csv"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  return (
    <Card className="bg-card border border-border overflow-hidden">
      <div className="p-6 border-b border-border flex justify-between items-center">
        <h2 className="text-xl font-semibold text-foreground">Resultados ({data.length} filas)</h2>
        <Button onClick={downloadCSV} variant="outline" size="sm" className="gap-2 bg-transparent">
          <Download className="h-4 w-4" />
          Descargar CSV
        </Button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-muted border-b border-border sticky top-0">
            <tr>
              <th className="px-4 py-3 text-left font-semibold text-foreground">#</th>
              <th className="px-4 py-3 text-left font-semibold text-foreground max-w-xs truncate">Proteina</th>
              <th className="px-4 py-3 text-left font-semibold text-foreground max-w-xs truncate">Ligando</th>
              <th className="px-4 py-3 text-center font-semibold text-foreground">Modelo 1</th>
              <th className="px-4 py-3 text-center font-semibold text-foreground">Modelo 2</th>
              <th className="px-4 py-3 text-center font-semibold text-foreground">Modelo 3</th>
              <th className="px-4 py-3 text-center font-semibold text-foreground">Modelo 4</th>
              <th className="px-4 py-3 text-center font-semibold text-foreground bg-accent/10">Rank</th>
              <th className="px-4 py-3 text-left font-semibold text-foreground">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {data.map((row, index) => (
              <tr key={index} className="hover:bg-muted/50 transition-colors">
                <td className="px-4 py-3 text-muted-foreground">{index + 1}</td>
                <td className="px-4 py-3 font-mono text-xs truncate max-w-xs" title={row.protein_sequence}>
                  {row.protein_sequence.slice(0, 30)}...
                </td>
                <td className="px-4 py-3 font-mono text-xs truncate max-w-xs" title={row.ligand_smiles}>
                  {row.ligand_smiles.slice(0, 30)}...
                </td>
                <td className="px-4 py-3 text-center font-mono text-sm text-foreground">
                  {formatScore(row.model1_score)}
                </td>
                <td className="px-4 py-3 text-center font-mono text-sm text-foreground">
                  {formatScore(row.model2_score)}
                </td>
                <td className="px-4 py-3 text-center font-mono text-sm text-foreground">
                  {formatScore(row.model3_score)}
                </td>
                <td className="px-4 py-3 text-center font-mono text-sm text-foreground">
                  {formatScore(row.model4_score)}
                </td>
                <td className="px-4 py-3 text-center font-bold font-mono text-accent bg-accent/10 rounded">
                  {formatScore(row.weighted_ranking)}
                </td>
                <td className="px-4 py-3 text-xs">
                  {row.error ? (
                    <span className="text-red-500 font-medium">Error: {row.error}</span>
                  ) : (
                    <span className="text-green-600 font-medium">Correcto</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
