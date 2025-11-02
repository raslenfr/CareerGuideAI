"use client"

import { createContext, useState, useEffect } from "react"

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in from localStorage
    const storedUser = localStorage.getItem("user")
    const storedToken = localStorage.getItem("jwt_token")
    
    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser))
    } else {
      // Clear incomplete auth state
      localStorage.removeItem("user")
      localStorage.removeItem("jwt_token")
    }
    setLoading(false)
  }, [])

  const login = (userData, token) => {
    setUser(userData)
    localStorage.setItem("user", JSON.stringify(userData))
    localStorage.setItem("jwt_token", token)
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem("user")
    localStorage.removeItem("jwt_token")
  }

  const register = (userData, token) => {
    setUser(userData)
    localStorage.setItem("user", JSON.stringify(userData))
    localStorage.setItem("jwt_token", token)
  }

  const updateUser = (userData) => {
    setUser(userData)
    localStorage.setItem("user", JSON.stringify(userData))
  }

  const isAuthenticated = () => {
    return !!user && !!localStorage.getItem("jwt_token")
  }

  const isAdmin = () => {
    return user?.role === "admin"
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register, updateUser, isAuthenticated, isAdmin }}>
      {children}
    </AuthContext.Provider>
  )
}
