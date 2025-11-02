"use client"

import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../hooks/useAuth"
import Header from "../common/Header"
import Footer from "../common/Footer"
import TestStatusIndicator from "../common/TestStatusIndicator"
import "./MainLayout.css"

const MainLayout = ({ children }) => {
  const { user, loading } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!loading && !user) {
      navigate("/login")
    }
  }, [user, loading, navigate])

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="main-layout">
      <Header />
      <main className="main-content">{children}</main>
      <Footer />
      <TestStatusIndicator />
    </div>
  )
}

export default MainLayout
