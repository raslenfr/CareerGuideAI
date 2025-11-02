"use client"

import { useState, useEffect } from "react"
import { useNavigate, Link } from "react-router-dom"
import { FiMail, FiArrowLeft, FiCheckCircle } from "react-icons/fi"
import { toast } from "react-toastify"
import { useAuth } from "../hooks/useAuth"
import "./Auth.css"

const VerifyEmail = () => {
  const [code, setCode] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [canResend, setCanResend] = useState(true)
  const [countdown, setCountdown] = useState(0)
  const [userEmail, setUserEmail] = useState("")
  const { user, updateUser } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    // Get user info from sessionStorage (from signup or login redirect)
    const unverifiedUser = sessionStorage.getItem('unverified_user')
    const verificationToken = localStorage.getItem('verification_token')
    
    if (unverifiedUser) {
      const userData = JSON.parse(unverifiedUser)
      setUserEmail(userData.email)
    } else if (user) {
      setUserEmail(user.email)
    }

    // If no token and no user, redirect to login
    if (!verificationToken && !user) {
      toast.error("Please sign up first")
      navigate("/login")
      return
    }

    // If already verified, redirect to login
    if (user && user.is_verified) {
      toast.success("Email already verified! Please log in.")
      navigate("/login")
      return
    }
    
    // Show message that code was sent during signup
    toast.info("Verification code sent to your email", { autoClose: 3000 })
  }, [])

  useEffect(() => {
    // Countdown timer for resend button
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    } else {
      setCanResend(true)
    }
  }, [countdown])

  const handleSendCode = async () => {
    if (!canResend) return

    setIsSending(true)
    try {
      // Get token from localStorage or auth context
      const token = localStorage.getItem('verification_token') || localStorage.getItem('jwt_token')
      
      const response = await fetch("/api/auth/send-verification", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      })
      
      const data = await response.json()
      
      if (data.success) {
        toast.success("New verification code sent to your email!")
        setCanResend(false)
        setCountdown(60) // 60 seconds cooldown
      } else {
        toast.error(data.error || "Failed to send verification code")
      }
    } catch (error) {
      console.error("Send verification error:", error)
      toast.error("Failed to send verification code. Please try again.")
    } finally {
      setIsSending(false)
    }
  }

  const handleVerify = async (e) => {
    e.preventDefault()

    if (code.length !== 6) {
      toast.error("Please enter a valid 6-digit code")
      return
    }

    setIsLoading(true)

    try {
      // Get token from localStorage
      const token = localStorage.getItem('verification_token') || localStorage.getItem('jwt_token')
      
      const response = await fetch("/api/auth/verify-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ code })
      })
      
      const data = await response.json()

      if (data.success) {
        toast.success("Email verified successfully! 🎉")
        
        // Clear temporary data
        localStorage.removeItem('verification_token')
        sessionStorage.removeItem('unverified_user')
        
        // Redirect to login page
        setTimeout(() => {
          toast.info("Please log in with your verified account")
          navigate("/login")
        }, 2000)
      } else {
        toast.error(data.error || "Verification failed. Please check your code.")
      }
    } catch (error) {
      console.error("Verification error:", error)
      toast.error("Verification failed. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCodeChange = (e) => {
    const value = e.target.value.replace(/\D/g, "").slice(0, 6)
    setCode(value)
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <Link to="/login" className="back-link">
              <FiArrowLeft /> Back to Login
            </Link>
            <div className="verification-icon">
              <FiMail size={48} color="#4CAF50" />
            </div>
            <h1>Verify Your Email</h1>
            <p>
              We've sent a 6-digit verification code to <strong>{userEmail}</strong>
            </p>
          </div>

          <form className="auth-form" onSubmit={handleVerify}>
            <div className="form-group">
              <label htmlFor="code">Verification Code</label>
              <div className="input-wrapper">
                <FiCheckCircle className="input-icon" />
                <input
                  type="text"
                  id="code"
                  placeholder="000000"
                  value={code}
                  onChange={handleCodeChange}
                  maxLength="6"
                  className="verification-input"
                  autoComplete="off"
                  autoFocus
                  required
                />
              </div>
              <small className="form-hint">Enter the 6-digit code from your email</small>
            </div>

            <button
              type="submit"
              className={`auth-button ${isLoading ? "loading" : ""}`}
              disabled={isLoading || code.length !== 6}
            >
              {isLoading ? "Verifying..." : "Verify Email"}
            </button>
          </form>

          <div className="auth-divider">
            <span>Didn't receive the code?</span>
          </div>

          <div className="resend-section">
            <button
              onClick={handleSendCode}
              className={`resend-button ${!canResend || isSending ? "disabled" : ""}`}
              disabled={!canResend || isSending}
            >
              {isSending ? "Sending..." : canResend ? "Resend Code" : `Resend in ${countdown}s`}
            </button>
          </div>

          <div className="auth-footer">
            <p style={{ fontSize: '0.875rem', color: '#718096', textAlign: 'center' }}>
              Check your spam folder if you don't see the email
            </p>
          </div>
        </div>
      </div>

      <div className="auth-background">
        <div className="auth-content">
          <h2>Secure Your Account</h2>
          <p>Email verification is required to activate your account and access all features.</p>
          <div className="auth-features">
            <div className="auth-feature">
              <div className="feature-icon">
                <FiCheckCircle />
              </div>
              <div className="feature-text">
                <h3>Account Security</h3>
                <p>Protect your account from unauthorized access</p>
              </div>
            </div>
            <div className="auth-feature">
              <div className="feature-icon">
                <FiMail />
              </div>
              <div className="feature-text">
                <h3>Stay Connected</h3>
                <p>Receive important updates and notifications</p>
              </div>
            </div>
          </div>
          <p style={{ marginTop: '1.5rem', fontSize: '0.9rem', opacity: 0.8 }}>
            This one-time verification ensures your email belongs to you.
          </p>
        </div>
      </div>
    </div>
  )
}

export default VerifyEmail

