"use client"

import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { FiUser, FiMail, FiLock, FiEye, FiEyeOff, FiArrowLeft, FiShield } from "react-icons/fi"
import { toast } from "react-toastify"
import { useAuth } from "../hooks/useAuth"
import "./Auth.css"

const Signup = () => {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [role, setRole] = useState("student")
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!name || !email || !password || !confirmPassword) {
      toast.error("Please fill in all fields")
      return
    }

    if (password !== confirmPassword) {
      toast.error("Passwords do not match")
      return
    }

    if (password.length < 6) {
      toast.error("Password must be at least 6 characters long")
      return
    }

    setIsLoading(true)

    try {
      // Make API call to signup endpoint
      const response = await fetch("/api/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          name, 
          email, 
          password,
          username: username || email.split('@')[0],
          role: role
        }),
      })

      const data = await response.json()

      if (data.success) {
        // Testing mode: no verification, go to login
        toast.success("Account created successfully! Please sign in.")
        setTimeout(() => {
          navigate("/login")
        }, 1000)
      } else {
        toast.error(data.error || "Registration failed. Please try again.")
      }
    } catch (error) {
      console.error("Signup error:", error)
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
            <h1>Create Your Account</h1>
            <p>Sign up to start your career journey</p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <div className="input-wrapper">
                <FiUser className="input-icon" />
                <input
                  type="text"
                  id="name"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <div className="input-wrapper">
                <FiMail className="input-icon" />
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
              <label htmlFor="username">Username (optional)</label>
              <div className="input-wrapper">
                <FiUser className="input-icon" />
                <input
                  type="text"
                  id="username"
                  placeholder="Choose a username (optional)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="role">Account Type</label>
              <div className="input-wrapper">
                <FiShield className="input-icon" />
                <select
                  id="role"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  required
                >
                  <option value="student">Student Account</option>
                  <option value="admin">Admin Account</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-wrapper">
                <FiLock className="input-icon" />
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  placeholder="Create a password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button type="button" className="password-toggle" onClick={() => setShowPassword(!showPassword)}>
                  {showPassword ? <FiEyeOff /> : <FiEye />}
                </button>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <div className="input-wrapper">
                <FiLock className="input-icon" />
                <input
                  type={showPassword ? "text" : "password"}
                  id="confirmPassword"
                  placeholder="Confirm your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-options">
              <div className="remember-me">
                <input type="checkbox" id="terms" required />
                <label htmlFor="terms">
                  I agree to the <Link to="/terms">Terms of Service</Link> and <Link to="/privacy">Privacy Policy</Link>
                </label>
              </div>
            </div>

            <button type="submit" className={`auth-button ${isLoading ? "loading" : ""}`} disabled={isLoading}>
              {isLoading ? "Creating Account..." : "Create Account"}
            </button>
          </form>

          <div className="auth-divider">
            <span>OR</span>
          </div>

          <div className="social-auth">
            <button className="social-button google">
              <img src="/google-icon.svg" alt="Google" />
              Sign up with Google
            </button>
            <button className="social-button linkedin">
              <img src="/linkedin-icon.svg" alt="LinkedIn" />
              Sign up with LinkedIn
            </button>
          </div>

          <div className="auth-footer">
            <p>
              Already have an account? <Link to="/login">Sign In</Link>
            </p>
          </div>
        </div>
      </div>

      <div className="auth-background">
        <div className="auth-content">
          <h2>Begin Your Career Transformation</h2>
          <p>
            Join thousands of professionals who have discovered their ideal career path with our AI-powered guidance
            platform.
          </p>
          <div className="auth-features">
            <div className="auth-feature">
              <div className="feature-icon">
                <FiUser />
              </div>
              <div className="feature-text">
                <h3>Personalized Recommendations</h3>
                <p>Get career and course suggestions tailored to your unique profile</p>
              </div>
            </div>
            <div className="auth-feature">
              <div className="feature-icon">
                <FiUser />
              </div>
              <div className="feature-text">
                <h3>AI-Powered Guidance</h3>
                <p>Access intelligent career advice whenever you need it</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Signup
