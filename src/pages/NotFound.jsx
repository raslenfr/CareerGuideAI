"use client"

import { Link } from "react-router-dom"
import { FiHome, FiArrowLeft } from "react-icons/fi"
import "./NotFound.css"

const NotFound = () => {
  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>The page you are looking for doesn't exist or has been moved.</p>
        <div className="not-found-actions">
          <Link to="/" className="home-button">
            <FiHome /> Go to Home
          </Link>
          <button onClick={() => window.history.back()} className="back-button">
            <FiArrowLeft /> Go Back
          </button>
        </div>
      </div>
    </div>
  )
}

export default NotFound

