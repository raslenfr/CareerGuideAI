"use client"

import { useState, useEffect } from "react"
import { FiUsers, FiUserCheck, FiUserX, FiTrendingUp } from "react-icons/fi"
import { toast } from "react-toastify"
import "./AdminDashboard.css"

const AdminStats = () => {
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
          <p>Loading statistics...</p>
        </div>
      </div>
    )
  }

  const verificationRate = stats?.total > 0 ? ((stats.verified / stats.total) * 100).toFixed(1) : 0

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Statistics</h1>
        <p>Detailed platform statistics and analytics</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" }}>
            <FiUsers />
          </div>
          <div className="stat-content">
            <h3>Total Users</h3>
            <p className="stat-value">{stats?.total || 0}</p>
            <small style={{ color: "#718096" }}>All registered users</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)" }}>
            <FiUserCheck />
          </div>
          <div className="stat-content">
            <h3>Verified Users</h3>
            <p className="stat-value">{stats?.verified || 0}</p>
            <small style={{ color: "#718096" }}>{verificationRate}% of total</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)" }}>
            <FiUserX />
          </div>
          <div className="stat-content">
            <h3>Unverified Users</h3>
            <p className="stat-value">{stats?.unverified || 0}</p>
            <small style={{ color: "#718096" }}>{(100 - verificationRate).toFixed(1)}% of total</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)" }}>
            <FiTrendingUp />
          </div>
          <div className="stat-content">
            <h3>Verification Rate</h3>
            <p className="stat-value">{verificationRate}%</p>
            <small style={{ color: "#718096" }}>Email verification success</small>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-card" style={{ gridColumn: "1 / -1" }}>
          <h3>User Distribution by Role</h3>
          <div className="role-breakdown">
            <div className="role-item">
              <span className="role-label">Admins</span>
              <div className="role-bar-container">
                <div
                  className="role-bar"
                  style={{
                    width: `${stats?.by_role && stats.total > 0 ? (stats.by_role.admin / stats.total) * 100 : 0}%`,
                    background: "#667eea",
                  }}
                >
                  {stats?.by_role && stats.total > 0 && ((stats.by_role.admin / stats.total) * 100).toFixed(1)}%
                </div>
              </div>
              <span className="role-count">{stats?.by_role?.admin || 0} users</span>
            </div>

            <div className="role-item">
              <span className="role-label">Students</span>
              <div className="role-bar-container">
                <div
                  className="role-bar"
                  style={{
                    width: `${stats?.by_role && stats.total > 0 ? (stats.by_role.student / stats.total) * 100 : 0}%`,
                    background: "#4facfe",
                  }}
                >
                  {stats?.by_role && stats.total > 0 && ((stats.by_role.student / stats.total) * 100).toFixed(1)}%
                </div>
              </div>
              <span className="role-count">{stats?.by_role?.student || 0} users</span>
            </div>
          </div>
        </div>
      </div>

      <div className="stats-details">
        <h3>Detailed Breakdown</h3>
        <div className="details-grid">
          <div className="detail-item">
            <span className="detail-label">Total Registrations:</span>
            <span className="detail-value">{stats?.total || 0}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Verified Accounts:</span>
            <span className="detail-value">{stats?.verified || 0}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Pending Verification:</span>
            <span className="detail-value">{stats?.unverified || 0}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Admin Accounts:</span>
            <span className="detail-value">{stats?.by_role?.admin || 0}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Student Accounts:</span>
            <span className="detail-value">{stats?.by_role?.student || 0}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Verification Success Rate:</span>
            <span className="detail-value">{verificationRate}%</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminStats


