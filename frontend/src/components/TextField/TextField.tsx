import './TextField.css'
import React, { useRef } from 'react'

interface TextFieldProps {
  value: string
  onChange: (newValue: string) => void
  label: string
}

const TextField: React.FC<TextFieldProps> = ({ value, onChange, label }) => {
  const textFieldRef = useRef<HTMLInputElement>(null)

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value)
  }

  return (
    <div className="textfield-container" ref={textFieldRef}>
      <label className="textfield-label" htmlFor="textfield">
        {label}
      </label>
      <input
        type="text"
        className="textfield-input"
        value={value}
        onChange={handleChange}
        id="textfield"
        title={value}
      />
    </div>
  )
}

export default TextField
