import './Gallery.css'
import React from 'react';
import { useTheme, Theme } from '../../contexts/ThemeProvider';
import RippleSpinner from '../../components/RippleSpinner/RippleSpinner';

interface GalleryProps {
  images: string[];
  loading: boolean;
}

const Gallery: React.FC<GalleryProps> = ({ images, loading }) => {
  const { theme } = useTheme();

  return (
    <div className="gallery">
      {images.length === 0 ? (
        <div className="gallery-loader-container">
          <RippleSpinner />
        </div>
      ) : (
        <div className="gallery-image-display-container">
          {loading ? (
            <div className="loading-container">
              <RippleSpinner />
            </div>
          ) : (<div></div>)}
          
          {images.map((image, index) => (
            <div className="gallery-image-container" key={index}>
              <a
                href={`data:image/png;base64,${image}`}
                download={`gallery_${index + 1}.png`}
              >
                <img
                  src={`data:image/png;base64,${image}`}
                  alt={`Collage ${index + 1}`}
                  className="gallery-image"
                />
              </a>
              {theme === Theme.LIGHT ? (
                <img
                  src="./src/components/icons/DownloadLight.svg"
                  alt={`download ${index + 1}`}
                  className="gallery-download-icon"
                />
              ) : (
                <img
                  src="./src/components/icons/DownloadDark.svg"
                  alt={`download ${index + 1}`}
                  className="gallery-download-icon"
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Gallery;
