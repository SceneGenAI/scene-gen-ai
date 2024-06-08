import React, { useRef, useState, useEffect } from 'react'
import './DropButton.css'

interface DropButtonProps {
  onImageUpload: (files: FileList) => void
}

const DropButton: React.FC<DropButtonProps> = ({ onImageUpload }) => {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement | null>(null)

  const handleDrop = (event: DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(false)
    const files = event.dataTransfer?.files
    if (files && files.length) {
      onImageUpload(files)
    }
  }

  const handleDragOver = (event: DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (event: DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(false)
  }

  const handleFileInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files && files.length) {
      onImageUpload(files)
    }
  }

  const handleClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  useEffect(() => {
    document.addEventListener('drop', handleDrop)
    document.addEventListener('dragover', handleDragOver)
    document.addEventListener('dragleave', handleDragLeave)
    return () => {
      document.removeEventListener('drop', handleDrop)
      document.removeEventListener('dragover', handleDragOver)
      document.removeEventListener('dragleave', handleDragLeave)
    }
  }, [])

  return (
    <div className="drop-button-container" onClick={handleClick}>
      <p>Выберите файл</p>
      <input
        type="file"
        id="file"
        multiple
        ref={fileInputRef}
        onChange={handleFileInputChange}
        title="Выберите файл для загрузки"
      />
      {isDragging && <div className="overlay" />}
    </div>
  )
}

export default DropButton
