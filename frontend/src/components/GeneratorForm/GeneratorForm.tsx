import './GeneratorForm.css';
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Dropdown from '../Dropdown/Dropdown';
import TextField from '../TextField/TextField';
import RingSpinner from '../RingSpinner/RingSpinner';
import ToggleButton from '../ToggleButton/ToggleButton';

interface DropdownOption {
  value: number;
  label: string;
}

interface GeneratorProps {
  backgroundOptions: { [key: string]: DropdownOption[] };
  styleOptions: { [key: string]: DropdownOption[] };
  responsePropsReceived: boolean;
  imageFile: File | null;
  getImages: (background: string, style: string) => void;
  setNumberImagesOption: React.Dispatch<React.SetStateAction<number>>;
  loading: boolean;
}

const GeneratorForm: React.FC<GeneratorProps> = ({
  backgroundOptions,
  styleOptions,
  responsePropsReceived,
  imageFile,
  getImages,
  setNumberImagesOption,
  loading,
}) => {
  const { t } = useTranslation();
  const [backgroundDropdown, setBackgroundDropdown] = useState<number>(0);
  const [styleDropdown, setStyleDropdown] = useState<number>(0);
  const [backgroundText, setBackgroundText] = useState<string>('');
  const [styleText, setStyleText] = useState<string>('');
  const [useTextField, setUseTextField] = useState<boolean>(false);

  const handleGenerate = async () => {
    const background = useTextField
      ? backgroundText
      : backgroundOptions['en'].find((option) => option.value === backgroundDropdown)?.label || '';
    const style = useTextField
      ? styleText
      : styleOptions['en'].find((option) => option.value === styleDropdown)?.label || '';

    await getImages(background, style);
  };

  const handleNumberImagesSelect = (value: number) => {
    setNumberImagesOption(value);
  };

  const toggleInputType = () => {
    setUseTextField(!useTextField);
  };

  return (
    <div
      className={`generator-form-container ${imageFile === null || !responsePropsReceived ? 'no-content' : ''}`}
    >
      {imageFile === null ? (
        <div className="generator-form-message">{t('Upload an image to continue')}</div>
      ) : !responsePropsReceived ? (
        <RingSpinner />
      ) : (
        <div className="generator-form-content">
          <div className="generator-form-input-container">
            {useTextField ? (
              <TextField
                value={backgroundText}
                onChange={setBackgroundText}
                label={t('Background')}
              />
            ) : (
              <Dropdown
                options={backgroundOptions}
                onChange={(value) => setBackgroundDropdown(value)}
                label={t('Background')}
              />
            )}
          </div>
          <div className="generator-form-input-container">
            <div className="generator-form-input-field">
              <ToggleButton onSelect={handleNumberImagesSelect} label={t('Number of images')} />
            </div>
            <div className="generator-form-input-field">
              {useTextField ? (
                <TextField value={styleText} onChange={setStyleText} label={t('Style')} />
              ) : (
                <Dropdown
                  options={styleOptions}
                  onChange={(value) => setStyleDropdown(value)}
                  label={t('Style')}
                />
              )}
            </div>
          </div>
          <button
            className="generator-form-generate-button"
            onClick={handleGenerate}
            disabled={loading}
          >
            {!loading ? t('Generate') : t('Generation')}
          </button>
          <button className="generator-form-toggle-button" onClick={toggleInputType}>
            {useTextField ? t('Back') : t('Not satisfied with the background or style?')}{' '}
          </button>
        </div>
      )}
    </div>
  );
};

export default GeneratorForm;
