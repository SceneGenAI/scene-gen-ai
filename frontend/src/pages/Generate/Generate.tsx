import './Generate.css'
import React, { useState } from 'react'
import GeneratorForm from '../../components/GeneratorForm/GeneratorForm'
import DropButton from '../../components/DropButton/DropButton'

interface DropdownOption {
  value: number
  label: string
}

const Generate: React.FC = () => {
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [dropdownOptions1, setDropdownOptions1] = useState<DropdownOption[]>([])
  const [responseReceived, setResponseReceived] = useState<boolean>(false)

  const dropdownOptions2 = [
    { value: 0, label: 'Минимализм' },
    { value: 1, label: 'Современный' },
    { value: 2, label: 'Классический' },
  ]

  const handleImageUpload = async (files: FileList) => {
    const file = files[0]
    setImageFile(file)
    setResponseReceived(false)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/prompt-generation', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        console.log(data)
        setDropdownOptions1(data)
        setResponseReceived(true)
      } else {
        console.error('Failed to fetch dropdown options')
      }
    } catch (error) {
      console.error('Error fetching dropdown options:', error)
    }
  }

  return (
    <div className="generate">
      <div className="generate-image-display-container">
        {imageFile && (
          <img
            src={URL.createObjectURL(imageFile)}
            alt="Uploaded Preview"
            className="generate-image-preview"
          />
        )}
      </div>
      <div className="generate-button-container">
        <DropButton onImageUpload={handleImageUpload} />
      </div>
      <GeneratorForm
        dropdownOptions1={dropdownOptions1}
        dropdownOptions2={dropdownOptions2}
        responseReceived={responseReceived}
        imageFile={imageFile}
      />
    </div>
  )
}

export default Generate
