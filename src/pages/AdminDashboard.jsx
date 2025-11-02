"use client"

import { useState, useEffect } from "react"
import { FiUsers, FiUserCheck, FiUserX, FiActivity } from "react-icons/fi"
import { toast } from "react-toastify"
import "./AdminDashboard.css"

const AdminDashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch("/api/admin/stats", {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })

      const data = await response.json()
      if (data.success) {
        setStats(data.stats)
      } else {
        toast.error("Failed to load statistics")
      }
    } catch (error) {
      console.error("Error fetching stats:", error)
      toast.error("Failed to load statistics")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="admin-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Admin Dashboard</h1>
        <p>Overview of your platform statistics</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" }}>
            <FiUsers />
          </div>
          <div className="stat-content">
            <h3>Total Users</h3>
            <p className="stat-value">{stats?.total || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)" }}>
            <FiUserCheck />
          </div>
          <div className="stat-content">
            <h3>Verified Users</h3>
            <p className="stat-value">{stats?.verified || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)" }}>
            <FiUserX />
          </div>
          <div className="stat-content">
            <h3>Unverified Users</h3>
            <p className="stat-value">{stats?.unverified || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)" }}>
            <FiActivity />
          </div>
          <div className="stat-content">
            <h3>Active Today</h3>
            <p className="stat-value">{stats?.active_today || 0}</p>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-card">
          <h3>Users by Role</h3>
          <div className="role-breakdown">
            <div className="role-item">
              <span className="role-label">Admins</span>
              <div className="role-bar-container">
                <div
                  className="role-bar"
                  style={{
                    width: `${stats?.by_role ? (stats.by_role.admin / stats.total) * 100 : 0}%`,
                    background: "#667eea",
                  }}
                ></div>
              </div>
              <span className="role-count">{stats?.by_role?.admin || 0}</span>
            </div>

            <div className="role-item">
              <span className="role-label">Students</span>
              <div className="role-bar-container">
                <div
                  className="role-bar"
                  style={{
                    width: `${stats?.by_role ? (stats.by_role.student / stats.total) * 100 : 0}%`,
                    background: "#4facfe",
                  }}
                ></div>
              </div>
              <span className="role-count">{stats?.by_role?.student || 0}</span>
            </div>
          </div>
        </div>

        <div className="chart-card">
          <h3>Verification Status</h3>
          <div className="pie-chart-placeholder">
            <div className="verification-breakdown">
              <div className="verification-item">
                <div className="verification-color" style={{ background: "#43e97b" }}></div>
                <span>Verified: {stats?.verified || 0}</span>
              </div>
              <div className="verification-item">
                <div className="verification-color" style={{ background: "#f5576c" }}></div>
                <span>Unverified: {stats?.unverified || 0}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="action-buttons">
          <a href="/admin/users" className="action-btn">
            <FiUsers />
            <span>Manage Users</span>
          </a>
          <a href="/admin/logs" className="action-btn">
            <FiActivity />
            <span>View Audit Logs</span>
          </a>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard


