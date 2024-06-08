import React, { useState } from 'react'
import './Generate.css'
import GeneratorForm from '../../components/GeneratorForm/GeneratorForm'
import DropButton from '../../components/DropButton/DropButton'

interface DropdownOption {
  value: number
  label: string
}

const Generate: React.FC = () => {
  const [imageSrc, setImageSrc] = useState<string | null>(null)
  const [dropdownOptions1, setDropdownOptions1] = useState<DropdownOption[]>([])
  const [responseReceived, setResponseReceived] = useState<boolean>(false)

  const dropdownOptions2 = [
    { value: 0, label: 'Минимализм' },
    { value: 1, label: 'Современный' },
    { value: 2, label: 'Классический' },
  ]

  const handleImageUpload = async (files: FileList) => {
    const file = files[0]
    setImageSrc(URL.createObjectURL(file))
    setResponseReceived(false)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://127.0.0.1:8000/get-dropdown-options', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
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
      <div className="image-display-container-generate">
        {imageSrc && <img src={imageSrc} alt="Uploaded Preview" className="image-preview" />}
      </div>
      <div className="button-container-generate">
        <DropButton onImageUpload={handleImageUpload} />
      </div>
      <GeneratorForm
        dropdownOptions1={dropdownOptions1}
        dropdownOptions2={dropdownOptions2}
        responseReceived={responseReceived}
      />
    </div>
  )
}

export default Generate
