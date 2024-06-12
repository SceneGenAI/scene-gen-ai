import './ToggleButton.css';
import React, { useState } from 'react';

interface ToggleButtonProps {
  onSelect: (value: number) => void;
  label: string;
}

const ToggleButton: React.FC<ToggleButtonProps> = ({ onSelect, label }) => {
  const [selectedValue, setSelectedValue] = useState<number>(1);

  const handleToggle = (value: number) => {
    setSelectedValue(value);
    onSelect(value);
  };

  return (
    <div className="toggle-group">
      <div className="toggle-group-label">{label}</div>
      <button
        onClick={() => handleToggle(1)}
        className={`toggle-button ${selectedValue === 1 ? ' active' : ''}`}
      >
        1
      </button>
      <button
        onClick={() => handleToggle(2)}
        className={`toggle-button ${selectedValue === 2 ? ' active' : ''}`}
      >
        2
      </button>
      <button
        onClick={() => handleToggle(4)}
        className={`toggle-button ${selectedValue === 4 ? ' active' : ''}`}
      >
        4
      </button>
    </div>
  );
};

export default ToggleButton;
