"use client"

import { useState, useEffect } from "react"
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { AuthProvider } from "./context/AuthContext"
import { TestProvider } from "./context/TestContext"
import { ToastContainer } from "react-toastify"
import "react-toastify/dist/ReactToastify.css"

// Layouts
import MainLayout from "./components/layout/MainLayout"
import AdminLayout from "./components/layout/AdminLayout"

// Pages
import Home from "./pages/Home"
import Login from "./pages/Login"
import Signup from "./pages/Signup"
import VerifyEmail from "./pages/VerifyEmail"
import Dashboard from "./pages/Dashboard"
import Chatbot from "./pages/Chatbot"
import CareerSuggester from "./pages/CareerSuggester"
import CourseRecommender from "./pages/CourseRecommender"
import NotFound from "./pages/NotFound"

// Admin Pages
import AdminDashboard from "./pages/AdminDashboard"
import AdminUsers from "./pages/AdminUsers"
import AdminStats from "./pages/AdminStats"
import AdminLogs from "./pages/AdminLogs"
import AdminFraud from "./pages/AdminFraud"

// Components
import GuideTour from "./components/onboarding/GuideTour"
import { useAuth } from "./hooks/useAuth"

// Auth Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading)
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    )

  if (!user) return <Navigate to="/login" replace />

  return children
}

// Admin Route Component
const AdminRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading)
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    )

  if (!user) return <Navigate to="/login" replace />
  
  if (user.role !== "admin") return <Navigate to="/dashboard" replace />

  return children
}

function App() {
  const [showTour, setShowTour] = useState(false)
  const [backendStatus, setBackendStatus] = useState("checking")

  useEffect(() => {
    // Check if it's the user's first visit
    const hasVisitedBefore = localStorage.getItem("hasVisitedBefore")
    if (!hasVisitedBefore) {
      setShowTour(true)
      localStorage.setItem("hasVisitedBefore", "true")
    }

    // Check if backend is running
    const checkBackendStatus = async () => {
      try {
        // Call the backend health check endpoint directly (not through proxy)
        const response = await fetch("http://localhost:5000/")
        if (response.ok) {
          setBackendStatus("connected")
        } else {
          setBackendStatus("error")
        }
      } catch (error) {
        console.error("Backend connection error:", error)
        setBackendStatus("error")
      }
    }

    checkBackendStatus()
  }, [])

  return (
    <AuthProvider>
      <Router>
        <TestProvider>
          <ToastContainer position="top-right" autoClose={3000} />
          {showTour && <GuideTour onClose={() => setShowTour(false)} />}

        {backendStatus === "error" && (
          <div className="backend-status-alert">
            <p>
              <strong>Backend Connection Error:</strong> Unable to connect to the Flask server. Please make sure it's
              running on port 5000.
            </p>
          </div>
        )}

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/verify-email"
            element={
              <ProtectedRoute>
                <VerifyEmail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <Dashboard />
                </MainLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/chatbot"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <Chatbot />
                </MainLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/career-suggester"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <CareerSuggester />
                </MainLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/course-recommender"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <CourseRecommender />
                </MainLayout>
              </ProtectedRoute>
            }
          />
          
          {/* Admin Routes */}
          <Route
            path="/admin/dashboard"
            element={
              <AdminRoute>
                <AdminLayout>
                  <AdminDashboard />
                </AdminLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/users"
            element={
              <AdminRoute>
                <AdminLayout>
                  <AdminUsers />
                </AdminLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/fraud"
            element={
              <AdminRoute>
                <AdminLayout>
                  <AdminFraud />
                </AdminLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/stats"
            element={
              <AdminRoute>
                <AdminLayout>
                  <AdminStats />
                </AdminLayout>
              </AdminRoute>
            }
          />
          <Route
            path="/admin/logs"
            element={
              <AdminRoute>
                <AdminLayout>
                  <AdminLogs />
                </AdminLayout>
              </AdminRoute>
            }
          />
          
          <Route path="*" element={<NotFound />} />
        </Routes>
        </TestProvider>
      </Router>
    </AuthProvider>
  )
}

export default App
