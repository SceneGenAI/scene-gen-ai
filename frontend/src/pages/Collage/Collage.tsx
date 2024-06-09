import './Collage.css'
import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { useTheme, Theme } from '../../contexts/ThemeProvider'

interface DropdownOption {
  value: string
  label: string
}

const Collage: React.FC = () => {
  const { theme } = useTheme()
  const location = useLocation()
  const { options, imageFile } = location.state as {
    options: { value1: DropdownOption; value2: DropdownOption }
    imageFile: File
  }

  const [images, setImages] = useState<string[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const sendRequest = async () => {
      const formData = new FormData()
      formData.append('file', imageFile)
      formData.append('background', options.value1.value)
      // formData.append('style', options.value2.value)

      try {
        const response = await fetch('http://localhost:8000/background-generation', {
          method: 'POST',
          body: formData,
        })

        const result = await response.json()
        setImages(result.images)
      } catch (error) {
        console.error('Error:', error)
      } finally {
        setLoading(false)
      }
    }

    sendRequest()
  }, [options, imageFile])

  return (
    <div>
      {loading ? (
        <div>Загрузка...</div>
      ) : (
        <div className="collage">
          <div className="collage-image-display-container">
            {images.map((image, index) => (
              <div className="collage-image-preview-container" key={index}>
                <a
                  href={`data:image/png;base64,${btoa(image)}`}
                  download={`collage_${index + 1}.png`}
                >
                  <img
                    src={`data:image/png;base64,${btoa(image)}`}
                    alt={`Collage ${index + 1}`}
                    className="collage-image-preview"
                  />
                </a>
                {theme === Theme.LIGHT ? (
                  <img
                    src="./src/components/icons/DownloadLight.svg"
                    alt={`download ${index + 1}`}
                    className="collage-download-icon"
                  />
                ) : (
                  <img
                    src="./src/components/icons/DownloadDark.svg"
                    alt={`download ${index + 1}`}
                    className="collage-download-icon"
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Collage
