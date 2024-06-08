import React, { useState, useEffect, useRef } from 'react'
import './Dropdown.css'

interface Option {
  value: string
  label: string
}

interface DropdownProps {
  options: Option[]
  onChange: (selectedValue: string) => void
  label: string
}

const Dropdown: React.FC<DropdownProps> = ({ options, onChange, label }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false)
  const [selectedValue, setSelectedValue] = useState<string>('')
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Set selected value to the first option value if options exist and selectedValue is not set
    if (options.length > 0 && !selectedValue) {
      setSelectedValue(options[0].value)
    }
  }, [options, selectedValue])

  const handleToggleDropdown = () => {
    setIsOpen(!isOpen)
  }

  const handleOptionClick = (value: string) => {
    setSelectedValue(value)
    onChange(value)
    setIsOpen(false)
  }

  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setIsOpen(false)
    }
  }

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  return (
    <div className="dropdown-container" ref={dropdownRef}>
      <label className="dropdown-label" htmlFor="dropdown">
        {label}
      </label>
      <div className={`dropdown-header ${isOpen ? 'open' : ''}`} onClick={handleToggleDropdown}>
        <div className="dropdown-header-text">
          {options.find((option) => option.value === selectedValue)?.label || 'Select'}{' '}
          {/* Add fallback text if no selected value */}
        </div>
        <img
          src="./src/components/icons/DropdownArrow.svg"
          alt="dropdown-arrow"
          className={`dropdown-arrow ${isOpen ? 'open' : ''}`}
        />
      </div>
      {isOpen && (
        <div className="dropdown-options">
          {options.map((option) => (
            <div
              key={option.value}
              className="dropdown-option dropdown-option-scrollable"
              onClick={() => handleOptionClick(option.value)}
              title={option.label}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Dropdown
