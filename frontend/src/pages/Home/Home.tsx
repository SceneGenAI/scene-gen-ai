import React from 'react'
import './Home.css'
import { Link } from 'react-router-dom'

const Home: React.FC = () => {
  return (
    <div className="home">
      <div className="text-container">
        <p className="text-container-header">Онлайн генератор сцен</p>
        <p className="text-container-description">Сгенерируйте сцену для своего товара</p>
      </div>
      <div className="button-container">
        <Link to="/generate" className="begin-button">
          <p>Начать</p>
        </Link>
      </div>
      <div className="images-container">
        <img src="./src/assets/swing-before.png" alt="swing-before" className="img-show" />
        <img src="./src/components/icons/Arrow.svg" alt="arrow" className="arrow" />
        <img src="./src/assets/swing-after.png" alt="swing-after" className="img-show" />
      </div>
    </div>
  )
}

export default Home
