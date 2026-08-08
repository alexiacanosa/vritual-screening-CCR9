"use client"

import { useState } from "react"
import { DocumentUploader } from "@/components/document-uploader"
import { DocumentOptions } from "@/components/document-options"
import { ProcessingStatus } from "@/components/processing-status"
import { ResultsTable } from "@/components/results-table"
import { parseProteinLigandCSV } from "@/lib/csv-parser"

interface UploadedDocument {
  id: string
  file: File
  name: string
  size: number
  uploadedAt: Date
}

interface ProcessResult {
  status: string
  total_processed: number
  successful: number
  partial_success: number
  errors: number
  results: Array<{
    protein_sequence: string
    ligand_smiles: string
    model1_result?: { score?: number; error?: string }
    model2_result?: { probability?: number; error?: string }
    model3_result?: { score?: number; error?: string }
    model4_result?: { score?: number; error?: string }
    weighted_ranking?: number
    status: string
    error?: string
  }>
  error_details?: string[] | null
}

export default function Home() {
  const [documents, setDocuments] = useState<UploadedDocument[]>([])
  const [selectedOptions, setSelectedOptions] = useState<string[]>([])
  const [processingState, setProcessingState] = useState({
    isProcessing: false,
    isComplete: false,
    error: null as string | null,
    result: null as ProcessResult | null,
  })

  const handleDocumentsChange = (docs: UploadedDocument[]) => {
    setDocuments(docs)
  }

  const handleProcessDocuments = async (options: string[]) => {
    if (documents.length < 1) {
      setProcessingState({
        isProcessing: false,
        isComplete: false,
        error: "Por favor suba 1 documento",
        result: null,
      })
      return
    }

    setProcessingState({
      isProcessing: true,
      isComplete: false,
      error: null,
      result: null,
    })

    try {
      const allRows: { protein_sequence: string; ligand_smiles: string }[] = []

      for (const doc of documents) {
        const rows = await parseProteinLigandCSV(doc.file)
        allRows.push(...rows)
      }

      const response = await fetch("http://localhost:8000/get_predictions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: allRows,
          options: options,
        }),
      })

      if (!response.ok) {
        throw new Error(`Fallo no backend ${response.status}`)
      }

      const result = await response.json()

      setProcessingState({
        isProcessing: false,
        isComplete: true,
        error: null,
        result,
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Error desconocido"

      setProcessingState({
        isProcessing: false,
        isComplete: false,
        error: `Fallo ao procesar documento: ${errorMessage}`,
        result: null,
      })
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-background to-muted">
      <header className="border-b border-border shadow-sm bg-primary">
        <div className="mx-auto max-w-5xl px-4 md:px-8 py-6">
          <h1 className="text-4xl font-bold text-foreground">Proxecto Integrador</h1>
        </div>
      </header>

      <div className="mx-auto max-w-5xl px-4 md:px-8 py-8">
        <div className="grid grid-cols-3 gap-8 mb-8">
          <div className="col-span-2">
            <DocumentUploader onDocumentsChange={handleDocumentsChange} />
          </div>
          <div>
            <DocumentOptions
              documentCount={documents.length}
              isProcessing={processingState.isProcessing}
              onProcess={handleProcessDocuments}
            />
          </div>
        </div>

        {processingState.isProcessing || processingState.isComplete || processingState.error ? (
          <ProcessingStatus
            isProcessing={processingState.isProcessing}
            isComplete={processingState.isComplete}
            error={processingState.error}
            documentCount={documents.length}
            optionsCount={selectedOptions.length}
          />
        ) : null}

        {processingState.isComplete && processingState.result?.results && (
          <div className="mt-8">
            <ResultsTable
              data={processingState.result.results.map((r: any) => {
                const model1_score = typeof r.model1_result?.score === "number" ? r.model1_result.score : undefined
                const model2_score = typeof r.model2_result?.affinity === "number" ? r.model2_result.affinity : undefined
                const model3_score = typeof r.model3_result?.score === "number" ? r.model3_result.score : undefined
                const model4_score = typeof r.model4_result?.score === "number" ? r.model4_result.score : undefined

                return {
                  protein_sequence: r.protein_sequence,
                  ligand_smiles: r.ligand_smiles,
                  model1_score,
                  model2_score,
                  model3_score,
                  model4_score,
                  weighted_ranking: r.weighted_ranking,
                  error: r.error || (r.status === "error" ? "O procesado fallou" : undefined),
                }
              })}
            />
          </div>
        )}
      </div>
    </main>
  )
}
