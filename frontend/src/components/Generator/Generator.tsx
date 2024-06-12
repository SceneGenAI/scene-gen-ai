import './Generator.css'
import React from 'react';
import DropButton from '../../components/DropButton/DropButton';
import GeneratorForm from '../../components/GeneratorForm/GeneratorForm';

interface DropdownOption {
  value: number
  label: string
}

interface GenerateProps {
  imageFile: File | null;
  backgroundOptions: DropdownOption[];
  styleOptions: { value: number; label: string }[];
  responsePropsReceived: boolean;
  getProps: (files: FileList) => Promise<void>;
  getImages: (background: string, style: string) => Promise<void>;
}

const Generator: React.FC<GenerateProps> = ({
  imageFile,
  backgroundOptions,
  styleOptions,
  responsePropsReceived,
  getProps,
  getImages,
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
        />
      </div>
    </div>
  );
};

export default Generator;
