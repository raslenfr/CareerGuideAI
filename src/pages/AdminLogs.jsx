"use client"

import { useState, useEffect } from "react"
import { FiClock, FiUser, FiActivity } from "react-icons/fi"
import { toast } from "react-toastify"
import "./AdminLogs.css"

const AdminLogs = () => {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch("/api/admin/logs", {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })

      const data = await response.json()
      if (data.success) {
        setLogs(data.logs)
      } else {
        toast.error("Failed to load audit logs")
      }
    } catch (error) {
      console.error("Error fetching logs:", error)
      toast.error("Failed to load audit logs")
    } finally {
      setLoading(false)
    }
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString(),
    }
  }

  if (loading) {
    return (
      <div className="admin-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading audit logs...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Audit Logs</h1>
        <p>Track all administrative actions performed on the platform</p>
      </div>

      <div className="logs-container">
        {logs.length === 0 ? (
          <div className="no-logs">
            <FiActivity size={48} color="#a0aec0" />
            <p>No audit logs available yet</p>
          </div>
        ) : (
          <div className="logs-list">
            {logs.map((log) => {
              const { date, time } = formatTimestamp(log.timestamp)
              return (
                <div key={log.id} className="log-item">
                  <div className="log-icon">
                    <FiActivity />
                  </div>
                  <div className="log-content">
                    <div className="log-header">
                      <h4 className="log-action">{log.action.replace(/_/g, " ").toUpperCase()}</h4>
                      <span className="log-timestamp">
                        <FiClock size={14} />
                        {date} at {time}
                      </span>
                    </div>
                    <div className="log-details">
                      <p className="log-admin">
                        <FiUser size={14} />
                        Admin ID: {log.admin_id}
                      </p>
                      {log.target_user_id && (
                        <p className="log-target">Target User ID: {log.target_user_id}</p>
                      )}
                      {log.details && <p className="log-description">{log.details}</p>}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {logs.length > 0 && (
        <div className="logs-summary">
          <p>
            Showing <strong>{logs.length}</strong> audit log entries
          </p>
        </div>
      )}
    </div>
  )
}

export default AdminLogs


