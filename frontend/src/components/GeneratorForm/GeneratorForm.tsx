import './GeneratorForm.css'
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Dropdown from '../Dropdown/Dropdown'
import TextField from '../TextField/TextField'

interface GeneratorProps {
  dropdownOptions1: { value: number; label: string }[]
  dropdownOptions2: { value: number; label: string }[]
  responseReceived: boolean
}

const Generator: React.FC<GeneratorProps> = ({
  dropdownOptions1,
  dropdownOptions2,
  responseReceived,
}) => {
  const { t }: { t: (key: string) => string } = useTranslation() // Define the type of t explicitly
  const defaultTextValue = ''
  const [dropdownValue1, setDropdownValue1] = useState<number>(
    dropdownOptions2.length > 0 ? dropdownOptions2[0].value : 0,
  )
  const [dropdownValue2, setDropdownValue2] = useState<number>(
    dropdownOptions2.length > 0 ? dropdownOptions2[0].value : 0,
  )
  const [textValue1, setTextValue1] = useState<string>(defaultTextValue)
  const [textValue2, setTextValue2] = useState<string>(defaultTextValue)
  const [useTextField, setUseTextField] = useState<boolean>(false)
  const navigate = useNavigate()

  const handleGenerate = () => {
    const options = {
      value1: useTextField ? textValue1 : dropdownValue1,
      value2: useTextField ? textValue2 : dropdownValue2,
    }

    navigate('/collage', { state: { options } })
  }

  const toggleInputType = () => {
    setUseTextField(!useTextField)
  }

  return (
    <div className="generator-container">
      {!responseReceived ? (
        <div>{t('Loading')}</div>
      ) : (
        <div className="generator-input-container">
          <div className="generator-input-field">
            {useTextField ? (
              <TextField value={textValue1} onChange={setTextValue1} label={t('Background')} />
            ) : (
              <Dropdown
                options={dropdownOptions1}
                onChange={setDropdownValue1}
                label={t('Background')}
              />
            )}
          </div>
          <div className="generator-input-field">
            {useTextField ? (
              <TextField value={textValue2} onChange={setTextValue2} label={t('Style')} />
            ) : (
              <Dropdown
                options={dropdownOptions2}
                onChange={setDropdownValue2}
                label={t('Style')}
              />
            )}
          </div>
        </div>
      )}
      <button
        className="generator-generate-button"
        onClick={handleGenerate}
        disabled={!responseReceived}
      >
        {t('Generate')}
      </button>
      <button
        className="generator-toggle-button"
        onClick={toggleInputType}
        disabled={!responseReceived}
      >
        {useTextField ? t('Back') : t('Not satisfied with the background or style?')}{' '}
      </button>
    </div>
  )
}

export default Generator
