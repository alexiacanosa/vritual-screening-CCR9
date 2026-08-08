"use client"

import type React from "react"
import { useState, useRef } from "react"
import { Cloud, File, X } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

interface UploadedDocument {
  id: string
  name: string
  size: number
  type: string
  uploadedAt: Date
  file: File
}

interface DocumentUploaderProps {
  onDocumentsChange?: (documents: UploadedDocument[]) => void
}

export function DocumentUploader({ onDocumentsChange }: DocumentUploaderProps) {
  const [documents, setDocuments] = useState<UploadedDocument[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    processFiles(files)
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      processFiles(e.target.files)
    }
  }

  const processFiles = (files: FileList) => {
    setIsUploading(true)
    const newDocs: UploadedDocument[] = []

    Array.from(files).forEach((file) => {
      const doc: UploadedDocument = {
        id: Math.random().toString(36).substr(2, 9),
        name: file.name,
        size: file.size,
        type: file.type,
        uploadedAt: new Date(),
        file: file, 
      }
      newDocs.push(doc)
    })

    setDocuments((prev) => {
      const updated = [...prev, ...newDocs]
      onDocumentsChange?.(updated)
      return updated
    })
    setIsUploading(false)
  }

  const removeDocument = (id: string) => {
    setDocuments((prev) => {
      const updated = prev.filter((doc) => doc.id !== id)
      onDocumentsChange?.(updated)
      return updated
    })
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i]
  }

  const formatDate = (date: Date): string => {
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Subir documentos</h1>
      </div>

      {/* Upload Zone */}
      <Card
        className="border-2 border-dashed border-border bg-card p-8 transition-all duration-200 hover:border-primary hover:bg-muted"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="rounded-full bg-primary/10 p-4">
            <Cloud className="h-8 w-8 text-primary" />
          </div>
          <div className="text-center space-y-2">
            <h2 className="text-xl font-semibold text-foreground">
              {isDragging ? "Deixe os documentos aquí" : "Arrastre aquí os seus documentos"}
            </h2>
            <p className="text-sm text-muted-foreground">
              ou{" "}
              <button
                onClick={() => fileInputRef.current?.click()}
                className="font-semibold text-primary hover:underline"
              >
                buscar nos teus arquivos
              </button>
            </p>
          </div>
          <p className="text-xs text-muted-foreground">SOLO SOPORTA CSV</p>
          <Button onClick={() => fileInputRef.current?.click()} className="mt-4" disabled={isUploading}>
            {isUploading ? "Subindo..." : "Seleccione ficheiros"}
          </Button>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileInput}
          className="hidden"
          accept=".csv"
        />
      </Card>

      {/* Uploaded Documents List */}
      {documents.length > 0 && (
        <Card className="bg-card p-6">
          <h3 className="mb-4 text-lg font-semibold text-foreground">Arquivos subidos ({documents.length})</h3>
          <div className="space-y-3">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between rounded-lg border border-border bg-background p-4 transition-colors hover:bg-muted"
              >
                <div className="flex items-center gap-3">
                  <div className="rounded-lg bg-primary/10 p-2">
                    <File className="h-5 w-5 text-primary" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-foreground text-sm truncate">{doc.name}</p>
                    <div className="flex gap-2 mt-1 text-xs text-muted-foreground">
                      <span>{formatFileSize(doc.size)}</span>
                      <span>•</span>
                      <span>{formatDate(doc.uploadedAt)}</span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => removeDocument(doc.id)}
                  className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
                  aria-label={`Borrar ${doc.name}`}
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Empty State Message */}
      {documents.length === 0 && !isUploading && (
        <div className="rounded-lg border border-dashed border-border bg-muted/30 p-8 text-center">
          <p className="text-sm text-muted-foreground">
            Sen documentos subidos.
          </p>
        </div>
      )}
    </div>
  )
}
