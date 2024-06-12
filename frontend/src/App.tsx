import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header/Header';
import Home from './pages/Home/Home';
import Generate from './pages/Generate/Generate';

const App: React.FC = () => {
  return (
    <Router>
      <Header />
      <div className="header-box"></div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/generate" element={<Generate />} />
        {/* <Route path="/log-in" element={<LogIn />} />
        <Route path="/sign-up" element={<SignUp />} /> */}
      </Routes>
    </Router>
  );
};

export default App;
