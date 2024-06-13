import './Dropdown.css';
import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { useTheme, Theme } from '../../contexts/ThemeProvider';

interface Option {
  value: number;
  label: string;
}

interface DropdownProps {
  options: { [key: string]: Option[] };
  onChange: (selectedValue: number) => void;
  label: string;
}

const Dropdown: React.FC<DropdownProps> = ({ options, onChange, label }) => {
  const { i18n } = useTranslation();
  const { theme } = useTheme();
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selectedValue, setSelectedValue] = useState<number>(0);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (
      options[i18n.language].length > 0 &&
      !options[i18n.language].find((opt) => opt.value === selectedValue)
    ) {
      setSelectedValue(options[i18n.language][0].value);
    }
  }, [i18n.language, selectedValue]);

  const handleToggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (value: number) => {
    setSelectedValue(value);
    onChange(value);
    setIsOpen(false);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="dropdown-container" ref={dropdownRef}>
      <label className="dropdown-label" htmlFor="dropdown">
        {label}
      </label>
      <div className={`dropdown-header ${isOpen ? 'open' : ''}`} onClick={handleToggleDropdown}>
        <div className="dropdown-header-text">
          {options[i18n.language].find((option) => option.value === selectedValue)?.label ||
            'Пусто'}{' '}
        </div>
        {theme === Theme.LIGHT ? (
          <img
            src="/icons/DropdownArrowLight.svg"
            alt="dropdown-arrow"
            className={`dropdown-arrow ${isOpen ? 'open' : ''}`}
          />
        ) : (
          <img
            src="/icons/DropdownArrowDark.svg"
            alt="dropdown-arrow"
            className={`dropdown-arrow ${isOpen ? 'open' : ''}`}
          />
        )}
      </div>
      {isOpen && (
        <div className="dropdown-options">
          {options[i18n.language].map((option) => (
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
  );
};

export default Dropdown;
