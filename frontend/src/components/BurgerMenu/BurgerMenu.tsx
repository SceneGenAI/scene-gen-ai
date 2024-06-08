import React, { useState } from 'react'
import './BurgerMenu.css'
import { Link } from 'react-router-dom'

const BurgerMenu: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)

  const toggleMenu = () => {
    setIsOpen(!isOpen)
  }

  return (
    <div className="burger-menu">
      <div className={`burger-icon ${isOpen ? 'open' : ''}`} onClick={toggleMenu}>
        <div className="line"></div>
        <div className="line"></div>
        <div className="line"></div>
      </div>
      <nav className={`menu ${isOpen ? 'open' : ''}`}>
        <div className="content">
          <div className="theme-language-container container">
            <div className="line">
              <div className="item">
                <p>
                  <Link to="/generate">Ru</Link>
                </p>
              </div>
            </div>
            <div className="line">
              <div className="item">
                <img
                  src="./src/components/icons/MoonIcon.svg"
                  alt="moon-icon"
                  className="moon-icon"
                />
              </div>
            </div>
          </div>
          <div className="sign-conotainer container">
            <div className="line">
              <div className="item">
                <p>Sign In</p>
              </div>
            </div>
            <div className="line">
              <div className="item">
                <div className="sign-in-button">
                  <p>Sign Up</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </div>
  )
}

export default BurgerMenu
