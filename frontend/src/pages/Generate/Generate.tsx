import './Generate.css';
import React, { useState } from 'react';
import Gallery from '../../components/Gallery/Gallery';
import Generator from '../../components/Generator/Generator';

interface DropdownOption {
  value: number;
  label: string;
}

const Generate: React.FC = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [backgroundOptions, setBackgroundOptions] = useState<DropdownOption[]>([]);
  const [responsePropsReceived, setResponsePropsReceived] = useState<boolean>(false);
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [numberImagesOption, setNumberImagesOption] = useState<number>(1);

  const styleOptions = [
    { value: 0, label: 'Minimalism' },
    { value: 1, label: 'Modern' },
    { value: 2, label: 'Classic' },
  ];

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
        setBackgroundOptions(data);
        setResponsePropsReceived(true);
      } else {
        console.error('Failed to fetch dropdown options');
        // setImageFile(null)
      }
    } catch (error) {
      console.error('Error fetching dropdown options:', error);
      // setImageFile(null)
    }
  };

  const getImages = async (background: string, style: string) => {
    const sendRequest = async () => {
      setLoading(true);
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
      } finally {
        setLoading(false);
      }
      return null;
    };

    const promises = [];
    for (let i = 0; i < numberImagesOption; i++) {
      promises.push(sendRequest());
    }

    const imagesResult = await Promise.all(promises);
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
      />
      <Gallery images={images} loading={loading} />
    </div>
  );
};

export default Generate;
