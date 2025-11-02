import { useState, useEffect, forwardRef, useImperativeHandle } from "react"
import { FiPlus, FiTrash2, FiClock } from "react-icons/fi"
import { getSuggesterSessions, deleteSuggesterSession } from "../../services/api"
import { toast } from "react-toastify"
import "./SuggesterSidebar.css"

const SuggesterSidebar = forwardRef(
  ({ userId, currentSessionId, onSelectSession, onNewSession, isCollapsed, onToggleCollapse }, ref) => {
    const [sessions, setSessions] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
      if (userId) {
        loadSessions()
      }
    }, [userId])

    const loadSessions = async () => {
      setIsLoading(true)
      try {
        const response = await getSuggesterSessions(userId)
        if (response.success) {
          setSessions(response.sessions || [])
        } else {
          console.error("Failed to load sessions:", response.error)
        }
      } catch (error) {
        console.error("Error loading sessions:", error)
      } finally {
        setIsLoading(false)
      }
    }

    // Expose loadSessions method to parent component
    useImperativeHandle(
      ref,
      () => ({
        loadSessions,
      }),
      []
    )

    const handleDeleteSession = async (sessionId, event) => {
      event.stopPropagation()

      if (!window.confirm("Are you sure you want to delete this session?")) {
        return
      }

      try {
        const response = await deleteSuggesterSession(sessionId, userId)
        if (response.success) {
          toast.success("Session deleted successfully")
          setSessions(sessions.filter((s) => s.session_id !== sessionId))

          // If deleting current session, trigger new session
          if (sessionId === currentSessionId) {
            onNewSession()
          }
        } else {
          toast.error(response.error || "Failed to delete session")
        }
      } catch (error) {
        console.error("Error deleting session:", error)
        toast.error("Failed to delete session")
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      if (diffDays === 1) return "Today"
      if (diffDays === 2) return "Yesterday"
      if (diffDays <= 7) return `${diffDays - 1} days ago`

      return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
    }

    if (isCollapsed) {
      return (
        <div className="suggester-sidebar collapsed">
          <button className="toggle-sidebar-btn" onClick={onToggleCollapse} title="Expand sidebar">
            <FiClock />
          </button>
        </div>
      )
    }

    return (
      <div className="suggester-sidebar">
        <div className="sidebar-header">
          <h3>Saved Sessions</h3>
          <div className="header-actions">
            <button className="toggle-sidebar-btn" onClick={onToggleCollapse} title="Collapse sidebar">
              ×
            </button>
          </div>
        </div>

        <button className="new-session-btn" onClick={onNewSession}>
          <FiPlus />
          <span>New Session</span>
        </button>

        <div className="sessions-list">
          {isLoading ? (
            <div className="sidebar-loading">Loading...</div>
          ) : sessions.length === 0 ? (
            <div className="no-sessions">
              <p>No saved sessions yet</p>
              <small>Complete a career path assessment to save a session</small>
            </div>
          ) : (
            sessions.map((session) => (
              <div
                key={session.session_id}
                className={`session-item ${session.session_id === currentSessionId ? "active" : ""}`}
                onClick={() => onSelectSession(session.session_id)}
              >
                <div className="session-content">
                  <div className="session-title">{session.session_title || "Untitled Session"}</div>
                  <div className="session-date">{formatDate(session.created_at)}</div>
                </div>
                <button
                  className="delete-session-btn"
                  onClick={(e) => handleDeleteSession(session.session_id, e)}
                  title="Delete session"
                >
                  <FiTrash2 />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    )
  }
)

SuggesterSidebar.displayName = "SuggesterSidebar"

export default SuggesterSidebar

