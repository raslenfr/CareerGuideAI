import { useState, useEffect } from "react"
import { toast } from "react-toastify"
import { FiAlertTriangle, FiCheckCircle, FiXCircle, FiRefreshCw, FiEye } from "react-icons/fi"
import "./AdminFraud.css"

const AdminFraud = () => {
  const [stats, setStats] = useState(null)
  const [queue, setQueue] = useState([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState("pending")
  const [reviewingUserId, setReviewingUserId] = useState(null)
  const [selectedUser, setSelectedUser] = useState(null)
  const [reviewNote, setReviewNote] = useState("")

  useEffect(() => {
    fetchStats()
    fetchQueue()
  }, [statusFilter])

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch("/api/admin/fraud/stats", {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      })
      const data = await response.json()
      if (data.success) {
        setStats(data.stats)
      }
    } catch (error) {
      console.error("Error fetching fraud stats:", error)
    }
  }

  const fetchQueue = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch(`/api/admin/fraud/queue?status=${statusFilter}&per_page=50`, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      })
      const data = await response.json()
      if (data.success) {
        setQueue(data.users)
      }
    } catch (error) {
      console.error("Error fetching fraud queue:", error)
      toast.error("Failed to load fraud queue")
    } finally {
      setLoading(false)
    }
  }

  const handleReview = async (userId, action) => {
    if (!reviewNote && action !== "clear") {
      toast.error("Please add a note before reviewing")
      return
    }

    setReviewingUserId(userId)
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch(`/api/admin/fraud/review/${userId}`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ action, note: reviewNote })
      })
      const data = await response.json()
      
      if (data.success) {
        toast.success(data.message)
        setSelectedUser(null)
        setReviewNote("")
        fetchStats()
        fetchQueue()
      } else {
        toast.error(data.error || "Review failed")
      }
    } catch (error) {
      console.error("Error reviewing fraud case:", error)
      toast.error("Failed to review user")
    } finally {
      setReviewingUserId(null)
    }
  }

  const getRiskBadge = (score) => {
    if (!score && score !== 0) return <span className="risk-badge risk-unknown">Unknown</span>
    if (score >= 0.8) return <span className="risk-badge risk-critical">Critical ({(score * 100).toFixed(1)}%)</span>
    if (score >= 0.4) return <span className="risk-badge risk-high">High ({(score * 100).toFixed(1)}%)</span>
    return <span className="risk-badge risk-low">Low ({(score * 100).toFixed(1)}%)</span>
  }

  const getReasonBadge = (reason) => {
    if (!reason) return null
    const badgeClass = reason.includes("block") ? "reason-block" : 
                      reason.includes("review") ? "reason-review" : "reason-other"
    return <span className={`reason-badge ${badgeClass}`}>{reason}</span>
  }

  return (
    <div className="admin-fraud">
      <div className="fraud-header">
        <h1>Fraud Detection</h1>
        <p>ML-powered signup risk monitoring and review queue</p>
      </div>

      {/* Stats Section */}
      {stats && (
        <div className="fraud-stats">
          <div className="stat-card">
            <div className="stat-icon risk-critical">
              <FiAlertTriangle />
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.pending_review}</div>
              <div className="stat-label">Pending Review</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon risk-high">
              <FiAlertTriangle />
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.suspicious_count}</div>
              <div className="stat-label">Total Suspicious</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon risk-low">
              <FiCheckCircle />
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.reviewed_count}</div>
              <div className="stat-label">Reviewed</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">
              <FiRefreshCw />
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.suspicious_percentage}%</div>
              <div className="stat-label">Flagged Rate</div>
            </div>
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="fraud-filters">
        <button 
          className={`filter-btn ${statusFilter === "pending" ? "active" : ""}`}
          onClick={() => setStatusFilter("pending")}
        >
          Pending ({stats?.pending_review || 0})
        </button>
        <button 
          className={`filter-btn ${statusFilter === "reviewed" ? "active" : ""}`}
          onClick={() => setStatusFilter("reviewed")}
        >
          Reviewed ({stats?.reviewed_count || 0})
        </button>
        <button 
          className={`filter-btn ${statusFilter === "all" ? "active" : ""}`}
          onClick={() => setStatusFilter("all")}
        >
          All ({stats?.suspicious_count || 0})
        </button>
      </div>

      {/* Queue Table */}
      <div className="fraud-queue">
        {loading ? (
          <div className="loading">Loading fraud queue...</div>
        ) : queue.length === 0 ? (
          <div className="empty-state">
            <FiCheckCircle size={48} color="#4CAF50" />
            <h3>No suspicious signups</h3>
            <p>All signups look legitimate!</p>
          </div>
        ) : (
          <table className="fraud-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Role</th>
                <th>Risk Score</th>
                <th>Reason</th>
                <th>Signed Up</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {queue.map((user) => (
                <tr key={user.id} className={selectedUser?.id === user.id ? "selected" : ""}>
                  <td>
                    <div className="user-cell">
                      <div className="user-name">{user.name}</div>
                      <div className="user-email">{user.email}</div>
                      <div className="user-username">@{user.username}</div>
                    </div>
                  </td>
                  <td>
                    <span className={`role-badge role-${user.role}`}>{user.role}</span>
                  </td>
                  <td>{getRiskBadge(user.risk_score)}</td>
                  <td>{getReasonBadge(user.fraud_reason)}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>
                    {user.fraud_reviewed_by ? (
                      <span className="status-reviewed">Reviewed</span>
                    ) : (
                      <span className="status-pending">Pending</span>
                    )}
                  </td>
                  <td>
                    <div className="action-buttons">
                      {!user.fraud_reviewed_by && (
                        <>
                          <button
                            className="action-btn btn-view"
                            onClick={() => setSelectedUser(user)}
                            title="View & Review"
                          >
                            <FiEye />
                          </button>
                        </>
                      )}
                      {user.fraud_reviewed_by && (
                        <span className="reviewed-text">
                          Reviewed {user.fraud_review_note && `- ${user.fraud_review_note}`}
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Review Modal */}
      {selectedUser && (
        <div className="review-modal-overlay" onClick={() => setSelectedUser(null)}>
          <div className="review-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Review Fraud Case</h2>
              <button className="modal-close" onClick={() => setSelectedUser(null)}>×</button>
            </div>

            <div className="modal-content">
              <div className="user-details">
                <div className="detail-row">
                  <strong>Name:</strong> {selectedUser.name}
                </div>
                <div className="detail-row">
                  <strong>Email:</strong> {selectedUser.email}
                </div>
                <div className="detail-row">
                  <strong>Username:</strong> @{selectedUser.username}
                </div>
                <div className="detail-row">
                  <strong>Role:</strong> <span className={`role-badge role-${selectedUser.role}`}>{selectedUser.role}</span>
                </div>
                <div className="detail-row">
                  <strong>Risk Score:</strong> {getRiskBadge(selectedUser.risk_score)}
                </div>
                <div className="detail-row">
                  <strong>Fraud Reason:</strong> {getReasonBadge(selectedUser.fraud_reason)}
                </div>
                <div className="detail-row">
                  <strong>Signed Up:</strong> {new Date(selectedUser.created_at).toLocaleString()}
                </div>
                <div className="detail-row">
                  <strong>Fraud Check:</strong> {selectedUser.fraud_checked_at ? new Date(selectedUser.fraud_checked_at).toLocaleString() : "N/A"}
                </div>
              </div>

              <div className="review-actions">
                <h3>Review Note</h3>
                <textarea
                  className="review-textarea"
                  placeholder="Add your review notes..."
                  value={reviewNote}
                  onChange={(e) => setReviewNote(e.target.value)}
                  rows={4}
                />

                <div className="review-buttons">
                  <button
                    className="review-btn btn-verify"
                    onClick={() => handleReview(selectedUser.id, "verify")}
                    disabled={reviewingUserId === selectedUser.id}
                  >
                    <FiCheckCircle /> Verify as Legitimate
                  </button>
                  <button
                    className="review-btn btn-block"
                    onClick={() => handleReview(selectedUser.id, "block")}
                    disabled={reviewingUserId === selectedUser.id}
                  >
                    <FiXCircle /> Block Account
                  </button>
                  <button
                    className="review-btn btn-clear"
                    onClick={() => handleReview(selectedUser.id, "clear")}
                    disabled={reviewingUserId === selectedUser.id}
                  >
                    Clear Flag
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminFraud

