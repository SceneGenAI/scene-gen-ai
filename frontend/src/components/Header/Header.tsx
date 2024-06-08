import React from 'react'
import './Header.css'
import { Link } from 'react-router-dom'
import BurgerMenu from '../BurgerMenu/BurgerMenu'

const Header: React.FC = () => {
  return (
    <header className="header">
      <BurgerMenu />
      <div className="nav">
        <div className="header-section header-left">
          <Link to="/">SceneGenAI</Link>
        </div>
        <div className="header-section header-center">
          <div className="header-item">
            <Link to="/collage" className="underlined">
              Ru
            </Link>
          </div>
          <div className="header-item">
            <img src="./src/components/icons/MoonIcon.svg" alt="moon-icon" className="moon-icon" />
          </div>
        </div>
        <div className="header-section header-right">
          <div className="header-item">
            <Link to="/sign-in" className="underlined">
              Sign In
            </Link>
          </div>
          <div className="header-item">
            <Link to="/sign-up" className="sign-up-button">
              <p>Sign Up</p>
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
