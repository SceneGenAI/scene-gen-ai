import './BurgerMenu.css';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useTheme, Theme } from '../../contexts/ThemeProvider';

const BurgerMenu: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const changeLanguage = () => {
    const newLang = i18n.language === 'en' ? 'ru' : 'en';
    i18n.changeLanguage(newLang);
  };

  return (
    <div className="burger-menu">
      <div className={`burger-icon ${isOpen ? 'open' : ''}`} onClick={toggleMenu}>
        <div className="burger-line"></div>
        <div className="burger-line"></div>
        <div className="burger-line"></div>
      </div>
      <nav className={`burger-content-menu ${isOpen ? 'open' : ''}`}>
        <div className="burger-content">
          <div className="burger-container burger-top-container">
            <div className="burger-container-line">
              <button onClick={changeLanguage} className="underlined language-button">
                {t('Language')}
              </button>
            </div>
            <div className="burger-container-line burger-theme" onClick={toggleTheme}>
              {theme === Theme.LIGHT ? (
                <img src="/icons/MoonIcon.svg" alt="moon-icon" className="burger-theme-icon" />
              ) : (
                <img src="/icons/SunIcon.svg" alt="sun-icon" className="burger-theme-icon" />
              )}
            </div>
          </div>
          <div className="burger-container">
            <div className="burger-container-line">
              <Link to="/log-in" className="underlined">
                {t('Log in')}
              </Link>
            </div>
            <div className="burger-container-line">
              <Link to="/sign-up" className="burger-sign-in-button">
                <p>{t('Sign up')}</p>
              </Link>
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default BurgerMenu;
