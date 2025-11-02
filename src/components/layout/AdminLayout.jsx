"use client"

import { Link, useLocation, useNavigate } from "react-router-dom"
import { FiHome, FiUsers, FiBarChart2, FiFileText, FiLogOut, FiMenu, FiX, FiAlertTriangle } from "react-icons/fi"
import { useState } from "react"
import { useAuth } from "../../hooks/useAuth"
import "./AdminLayout.css"

const AdminLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    navigate("/login")
  }

  const navItems = [
    { path: "/admin/dashboard", icon: <FiHome />, label: "Dashboard" },
    { path: "/admin/users", icon: <FiUsers />, label: "Users" },
    { path: "/admin/fraud", icon: <FiAlertTriangle />, label: "Fraud Detection" },
    { path: "/admin/stats", icon: <FiBarChart2 />, label: "Statistics" },
    { path: "/admin/logs", icon: <FiFileText />, label: "Audit Logs" },
  ]

  return (
    <div className="admin-layout">
      {/* Sidebar */}
      <aside className={`admin-sidebar ${sidebarOpen ? "open" : "closed"}`}>
        <div className="sidebar-header">
          <h2>Admin Panel</h2>
          <button className="sidebar-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? "active" : ""}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            {sidebarOpen && (
              <>
                <p className="user-name">{user?.name || "Admin"}</p>
                <p className="user-email">{user?.email}</p>
              </>
            )}
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            <FiLogOut />
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`admin-main ${sidebarOpen ? "sidebar-open" : "sidebar-closed"}`}>
        <div className="admin-content">{children}</div>
      </main>
    </div>
  )
}

export default AdminLayout


