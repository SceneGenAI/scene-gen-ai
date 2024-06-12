import './Header.css'
import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useTheme, Theme } from '../../contexts/ThemeProvider'
import BurgerMenu from '../BurgerMenu/BurgerMenu'

const Header: React.FC = () => {
  const { t, i18n } = useTranslation()
  const { theme, toggleTheme } = useTheme()

  const changeLanguage = () => {
    const newLang = i18n.language === 'en' ? 'ru' : 'en'
    i18n.changeLanguage(newLang)
  }

  return (
    <header className="header">
      <BurgerMenu />
      <div className="header-nav">
        <div className="header-section header-left">
          <Link to="/">SceneGenAI</Link>
        </div>
        <div className="header-section header-center">
          <div className="header-item">
            <button onClick={changeLanguage} className="underlined language-button">
              {t('Language')}
            </button>
          </div>
          <div className="header-item" onClick={toggleTheme}>
            {theme === Theme.LIGHT ? (
              <img src="/icons/MoonIcon.svg" alt="moon-icon" className="theme-icon" />
            ) : (
              <img src="/icons/SunIcon.svg" alt="sun-icon" className="theme-icon" />
            )}
          </div>
        </div>
        <div className="header-section header-right">
          <div className="header-item">
            <Link to="/log-in" className="underlined">
              {t('Log in')}
            </Link>
          </div>
          <div className="header-item">
            <Link to="/sign-up" className="sign-up-button">
              <p>{t('Sign up')}</p>
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
