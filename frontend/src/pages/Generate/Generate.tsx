import './Generate.css';
import React, { useState } from 'react';
import Gallery from '../../components/Gallery/Gallery';
import Generator from '../../components/Generator/Generator';

interface DropdownOption {
  value: number;
  label: string;
}

interface BackgroundOptions {
  [key: string]: DropdownOption[];
}

const Generate: React.FC = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [backgroundOptions, setBackgroundOptions] = useState<BackgroundOptions>({});
  const [responsePropsReceived, setResponsePropsReceived] = useState<boolean>(false);
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [numberImagesOption, setNumberImagesOption] = useState<number>(1);

  const styleOptions = {
    en: [
      { value: 0, label: 'Contemporary' },
      { value: 1, label: 'Minimalistic' },
      { value: 2, label: 'Scandinavian' },
      { value: 3, label: 'Bohemian eclectic' },
      { value: 4, label: 'Traditional elegance' },
      { value: 5, label: 'Urban' },
    ] as DropdownOption[],
    ru: [
      { value: 0, label: 'Современный' },
      { value: 1, label: 'Минималистичный' },
      { value: 2, label: 'Скандинавский' },
      { value: 3, label: 'Богемная эклектика' },
      { value: 4, label: 'Традиционная элегантность' },
      { value: 5, label: 'Городской' },
    ] as DropdownOption[],
  };

  const getProps = async (files: FileList) => {
    const file = files[0];
    setImageFile(files[0]);
    setResponsePropsReceived(false);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/prompt-generation', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();

        const formattedBackgroundOptions: BackgroundOptions = {
          en: data.en.map((option: BackgroundOptions) => ({
            value: option.value,
            label: option.label,
          })),
          ru: data.ru.map((option: BackgroundOptions) => ({
            value: option.value,
            label: option.label,
          })),
        };

        setBackgroundOptions(formattedBackgroundOptions);
        setResponsePropsReceived(true);
      } else {
        console.error('Failed to fetch dropdown options');
        setImageFile(null);
      }
    } catch (error) {
      console.error('Error fetching dropdown options:', error);
      setImageFile(null);
    }
  };

  const getImages = async (background: string, style: string) => {
    const sendRequest = async () => {
      const formData = new FormData();
      formData.append('file', imageFile as File);
      formData.append('background', background);
      formData.append('style', style);

      try {
        const response = await fetch('http://localhost:8000/background-generation', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          return result.image;
        } else {
          console.error('Failed to generate image');
        }
      } catch (error) {
        console.error('Error:', error);
      }
      return null;
    };

    const promises = [];
    for (let i = 0; i < numberImagesOption; i++) {
      promises.push(sendRequest());
    }

    setLoading(true);
    const imagesResult = await Promise.all(promises);
    setLoading(false);
    setImages((prevImages) => [
      ...imagesResult.filter((image): image is string => image !== null),
      ...prevImages,
    ]);
  };

  return (
    <div className="generate">
      <Generator
        imageFile={imageFile}
        backgroundOptions={backgroundOptions}
        styleOptions={styleOptions}
        responsePropsReceived={responsePropsReceived}
        getProps={getProps}
        getImages={getImages}
        setNumberImagesOption={setNumberImagesOption}
        loading={loading}
      />
      <Gallery images={images} loading={loading} />
    </div>
  );
};

export default Generate;
