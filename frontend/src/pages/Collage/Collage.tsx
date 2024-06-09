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
  const { options } = location.state as {
    options: { value1: DropdownOption; value2: DropdownOption }
  }

  const [images, setImages] = useState<string[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const sendRequest = async () => {
      try {
        const response = await fetch('http://localhost:8000/get-images', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            option1: options.value1.value,
            option2: options.value2.value,
          }),
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
  }, [options])

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
