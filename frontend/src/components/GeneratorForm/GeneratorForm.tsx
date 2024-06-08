import React, { useState } from 'react'
import Dropdown from '../Dropdown/Dropdown'
import TextField from '../TextField/TextField'
import './Generator.css'

interface GeneratorProps {
  dropdownOptions1: { value: string; label: string }[]
  dropdownOptions2: { value: string; label: string }[]
  responseReceived: boolean
}

const Generator: React.FC<GeneratorProps> = ({
  dropdownOptions1,
  dropdownOptions2,
  responseReceived,
}) => {
  const defaultTextValue = ''

  const [dropdownValue1, setDropdownValue1] = useState<string>(
    dropdownOptions2.length > 0 ? dropdownOptions2[0].value : '',
  )
  const [dropdownValue2, setDropdownValue2] = useState<string>(
    dropdownOptions2.length > 0 ? dropdownOptions2[0].value : '',
  )
  const [textValue1, setTextValue1] = useState<string>(defaultTextValue)
  const [textValue2, setTextValue2] = useState<string>(defaultTextValue)
  const [useTextField, setUseTextField] = useState<boolean>(false)

  const handleGenerate = () => {
    const data = {
      value1: useTextField ? textValue1 : dropdownValue1,
      value2: useTextField ? textValue2 : dropdownValue2,
    }

    fetch('/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data)
      })
      .catch((error) => {
        console.error('Error:', error)
      })
  }

  const toggleInputType = () => {
    setUseTextField(!useTextField)
  }

  return (
    <div className="generator-container">
      {!responseReceived ? (
        <div>Загрузка...</div>
      ) : (
        <div className="input-container">
          <div className="input-field">
            {useTextField ? (
              <TextField value={textValue1} onChange={setTextValue1} label="Фон" />
            ) : (
              <Dropdown options={dropdownOptions1} onChange={setDropdownValue1} label="Фон" />
            )}
          </div>
          <div className="input-field">
            {useTextField ? (
              <TextField value={textValue2} onChange={setTextValue2} label="Стиль" />
            ) : (
              <Dropdown options={dropdownOptions2} onChange={setDropdownValue2} label="Стиль" />
            )}
          </div>
        </div>
      )}
      <button className="generate-button" onClick={handleGenerate} disabled={!responseReceived}>
        Сгенерировать
      </button>
      <button className="toggle-button" onClick={toggleInputType}>
        {useTextField ? 'Вернуться' : 'Не устроил фон или стиль?'}
      </button>
    </div>
  )
}

export default Generator
