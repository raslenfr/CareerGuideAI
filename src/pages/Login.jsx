"use client"

import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { FiUser, FiLock, FiEye, FiEyeOff, FiArrowLeft, FiShield } from "react-icons/fi"
import { useAuth } from "../hooks/useAuth"
import { toast } from "react-toastify"
import "./Auth.css"

const Login = () => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [role, setRole] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!email || !password) {
      toast.error("Please fill in all fields")
      return
    }

    setIsLoading(true)

    try {
      // Make API call to login endpoint
      const requestBody = { email, password }
      if (role) {
        requestBody.role = role  // Include role if specified
      }
      
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      })

      const data = await response.json()

      if (data.success) {
        // Store JWT token and user data via login function
        login(data.user, data.access_token)
        toast.success(data.message || "Login successful!")
        
        // Redirect based on role
        if (data.user.role === "admin") {
          navigate("/admin/dashboard")
        } else {
          navigate("/dashboard")
        }
      } else {
        // Simple error handling (no verification flow)
        toast.error(data.error || "Login failed. Please check your credentials.")
      }
    } catch (error) {
      console.error("Login error:", error)
      toast.error("Network error. Please check if the backend server is running.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <Link to="/" className="back-link">
              <FiArrowLeft /> Back to Home
            </Link>
            <h1>Welcome Back</h1>
            <p>Sign in to continue your career journey</p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <div className="input-wrapper">
                <FiUser className="input-icon" />
                <input
                  type="email"
                  id="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="role">Account Type (Optional)</label>
              <div className="input-wrapper">
                <FiShield className="input-icon" />
                <select
                  id="role"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                >
                  <option value="">Auto-detect (Recommended)</option>
                  <option value="student">Student Account</option>
                  <option value="admin">Admin Account</option>
                </select>
              </div>
              <small style={{ color: '#718096', fontSize: '0.875rem', marginTop: '0.25rem', display: 'block' }}>
                Only needed if you have both student and admin accounts with the same email
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-wrapper">
                <FiLock className="input-icon" />
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button type="button" className="password-toggle" onClick={() => setShowPassword(!showPassword)}>
                  {showPassword ? <FiEyeOff /> : <FiEye />}
                </button>
              </div>
            </div>

            <div className="form-options">
              <div className="remember-me">
                <input type="checkbox" id="remember" />
                <label htmlFor="remember">Remember me</label>
              </div>
              <Link to="/forgot-password" className="forgot-password">
                Forgot Password?
              </Link>
            </div>

            <button type="submit" className={`auth-button ${isLoading ? "loading" : ""}`} disabled={isLoading}>
              {isLoading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <div className="auth-divider">
            <span>OR</span>
          </div>

          <div className="social-auth">
            <button className="social-button google">
              <img src="/google-icon.svg" alt="Google" />
              Sign in with Google
            </button>
            <button className="social-button linkedin">
              <img src="/linkedin-icon.svg" alt="LinkedIn" />
              Sign in with LinkedIn
            </button>
          </div>

          <div className="auth-footer">
            <p>
              Don't have an account? <Link to="/signup">Sign Up</Link>
            </p>
          </div>
        </div>
      </div>

      <div className="auth-background">
        <div className="auth-content">
          <h2>Unlock Your Career Potential</h2>
          <p>
            Get personalized career guidance, course recommendations, and expert advice tailored to your unique skills
            and goals.
          </p>
          <div className="auth-features">
            <div className="auth-feature">
              <div className="feature-icon">
                <FiUser />
              </div>
              <div className="feature-text">
                <h3>Personalized Guidance</h3>
                <p>AI-powered recommendations based on your profile</p>
              </div>
            </div>
            <div className="auth-feature">
              <div className="feature-icon">
                <FiUser />
              </div>
              <div className="feature-text">
                <h3>Expert Insights</h3>
                <p>Access to industry-specific career advice</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
