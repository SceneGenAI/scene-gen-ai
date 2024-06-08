import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import './Collage.css'

interface DropdownOption {
  value: string
  label: string
}

const Collage: React.FC = () => {
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
          <div className="image-display-container-collage">
            {images.map((image, index) => (
              <div className="image-preview-container-collage" key={index}>
                <a
                  href={`data:image/png;base64,${btoa(image)}`}
                  download={`collage_${index + 1}.png`}
                >
                  <img
                    src={`data:image/png;base64,${btoa(image)}`}
                    alt={`Collage ${index + 1}`}
                    className="image-preview-collage"
                  />
                </a>
                <img
                  src="./src/components/icons/Download.svg"
                  alt={`download ${index + 1}`}
                  className="download-icon"
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Collage
