import './Generator.css';
import React from 'react';
import DropButton from '../../components/DropButton/DropButton';
import GeneratorForm from '../../components/GeneratorForm/GeneratorForm';

interface DropdownOption {
  value: number;
  label: string;
}

interface GenerateProps {
  imageFile: File | null;
  backgroundOptions: { [key: string]: DropdownOption[] };
  styleOptions: { [key: string]: DropdownOption[] };
  responsePropsReceived: boolean;
  getProps: (files: FileList) => Promise<void>;
  getImages: (background: string, style: string, number_images: number) => Promise<void>;
  setNumberImagesOption: React.Dispatch<React.SetStateAction<number>>;
  numberImages: number;
  loading: boolean;
}

const Generator: React.FC<GenerateProps> = ({
  imageFile,
  backgroundOptions,
  styleOptions,
  responsePropsReceived,
  getProps,
  getImages,
  setNumberImagesOption,
  numberImages,
  loading,
}) => {
  return (
    <div className="generator">
      <div className="generator-fixed">
        <div className="generator-image-display-container">
          {imageFile && (
            <img
              src={URL.createObjectURL(imageFile)}
              alt="Uploaded Preview"
              className="generator-image-preview"
            />
          )}
        </div>
        <div className="generator-button-container">
          <DropButton onImageUpload={getProps} />
        </div>
        <GeneratorForm
          backgroundOptions={backgroundOptions}
          styleOptions={styleOptions}
          responsePropsReceived={responsePropsReceived}
          imageFile={imageFile}
          getImages={getImages}
          setNumberImagesOption={setNumberImagesOption}
          numberImages={numberImages}
          loading={loading}
        />
      </div>
    </div>
  );
};

export default Generator;
