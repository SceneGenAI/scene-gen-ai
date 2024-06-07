import React from 'react'
import './Header.css'
import { Link } from 'react-router-dom'
import BurgerMenu from '../BurgerMenu/BurgerMenu'

// const pages = [
//   {
//     name: 'SceneGenAI',
//     link: '/'
//   },
//   {
//     name: 'Sign In',
//     link: '/signin'
//   },
//   {
//     name: 'Sign Up',
//     link: '/signUp'
//   },
//   {
//     name: 'History',
//     link: '/history'
//   },
//   {
//     name: 'profile',
//     link: '/profile'
//   }
// ]

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
            <p>
              <Link to="/generate">Ru</Link>
            </p>
          </div>
          <div className="header-item">
            <img src="./src/components/icons/temp.svg" alt="moon-icon" className="moon-icon" />
          </div>
        </div>
        <div className="header-section header-right">
          <div className="header-item">
            <p>Sign In</p>
          </div>
          <div className="header-item">
            <div className="sign-in-button">
              <p>Sign Up</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
