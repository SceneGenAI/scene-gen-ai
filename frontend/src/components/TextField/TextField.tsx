import './TextField.css';
import React, { useRef } from 'react';
import { useTranslation } from 'react-i18next';

interface TextFieldProps {
  value: string;
  onChange: (newValue: string) => void;
  label: string;
}

const TextField: React.FC<TextFieldProps> = ({ value, onChange, label }) => {
  const { i18n } = useTranslation();
  const textFieldRef = useRef<HTMLInputElement>(null);
  const enRegex = /[^a-z0-9 ,.!?]/gi;
  const ruRegex = /[^а-яё0-9 ,.!?]/gi;

  const regex = i18n.language === 'ru' ? ruRegex : enRegex;

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    event.currentTarget.value = event.currentTarget.value.replace(regex, '');
    onChange(event.target.value);
  };

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
  );
};

export default TextField;
