import './Home.css'
import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

const Home: React.FC = () => {
  const { t } = useTranslation()

  return (
    <div className="home">
      <div className="home-text-container">
        <p className="home-text-container-header">{t('Scene generator')}</p>
        <p className="home-text-container-description">{t('Generate scene for your product')}</p>
      </div>
      <div className="home-button-container">
        <Link to="/generate" className="home-begin-button">
          <p>{t('Begin')}</p>
        </Link>
      </div>
      <div className="home-images-container">
        <img src="./src/assets/swing-before.png" alt="swing-before" className="home-img-show" />
        <img src="./src/components/icons/Arrow.svg" alt="arrow" className="home-arrow" />
        <img src="./src/assets/swing-after.png" alt="swing-after" className="home-img-show" />
      </div>
    </div>
  )
}

export default Home
