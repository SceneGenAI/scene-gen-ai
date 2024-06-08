import './Dropdown.css'
import React, { useState, useEffect, useRef } from 'react'
import { useTheme, Theme } from '../../contexts/ThemeProvider'

interface Option {
  value: number
  label: string
}

interface DropdownProps {
  options: Option[]
  onChange: (selectedValue: number) => void
  label: string
}

const Dropdown: React.FC<DropdownProps> = ({ options, onChange, label }) => {
  const { theme } = useTheme()
  const [isOpen, setIsOpen] = useState<boolean>(false)
  const [selectedValue, setSelectedValue] = useState<number>(0)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (options.length > 0 && !selectedValue) {
      setSelectedValue(options[0].value)
    }
  }, [options, selectedValue])

  const handleToggleDropdown = () => {
    setIsOpen(!isOpen)
  }

  const handleOptionClick = (value: number) => {
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
          {options.find((option) => option.value === selectedValue)?.label || 'Пусто'}{' '}
        </div>
        {theme === Theme.LIGHT ? (
          <img
            src="./src/components/icons/DropdownArrowLight.svg"
            alt="dropdown-arrow"
            className={`dropdown-arrow ${isOpen ? 'open' : ''}`}
          />
        ) : (
          <img
            src="./src/components/icons/DropdownArrowDark.svg"
            alt="dropdown-arrow"
            className={`dropdown-arrow ${isOpen ? 'open' : ''}`}
          />
        )}
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
