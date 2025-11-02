"use client"

import { useState, useEffect, forwardRef, useImperativeHandle } from "react"
import { FiPlus, FiMessageSquare, FiTrash2, FiChevronLeft, FiChevronRight } from "react-icons/fi"
import { getChatConversations, deleteChatConversation } from "../../services/api"
import { toast } from "react-toastify"
import "./ChatSidebar.css"

const ChatSidebar = forwardRef(
  ({ userId, currentConversationId, onSelectConversation, onNewChat, isCollapsed, onToggleCollapse }, ref) => {
    const [conversations, setConversations] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
      if (userId) {
        loadConversations()
      }
    }, [userId])

    const loadConversations = async () => {
      setIsLoading(true)
      try {
        const response = await getChatConversations(userId)
        if (response.success) {
          setConversations(response.conversations || [])
        } else {
          console.error("Failed to load conversations:", response.error)
        }
      } catch (error) {
        console.error("Error loading conversations:", error)
      } finally {
        setIsLoading(false)
      }
    }

    // Expose loadConversations method to parent component
    useImperativeHandle(ref, () => ({
      loadConversations,
    }), [])

  const handleDeleteConversation = async (conversationId, e) => {
    e.stopPropagation()
    if (!window.confirm("Are you sure you want to delete this conversation?")) {
      return
    }

    try {
      const response = await deleteChatConversation(conversationId, userId)
      if (response.success) {
        toast.success("Conversation deleted")
        setConversations(conversations.filter((c) => c.conversation_id !== conversationId))
        if (currentConversationId === conversationId) {
          onNewChat()
        }
      } else {
        toast.error(response.error || "Failed to delete conversation")
      }
    } catch (error) {
      toast.error("Error deleting conversation")
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return ""
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return "Today"
    if (diffDays === 1) return "Yesterday"
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString()
  }

  if (isCollapsed) {
    return (
      <div className="chat-sidebar collapsed">
        <button className="toggle-sidebar-btn" onClick={onToggleCollapse} title="Show sidebar">
          <FiChevronRight />
        </button>
      </div>
    )
  }

  return (
    <div className="chat-sidebar">
      <div className="sidebar-header">
        <button className="new-chat-btn" onClick={onNewChat}>
          <FiPlus /> New Chat
        </button>
        <button className="toggle-sidebar-btn" onClick={onToggleCollapse} title="Hide sidebar">
          <FiChevronLeft />
        </button>
      </div>

      <div className="sidebar-content">
        {isLoading ? (
          <div className="sidebar-loading">Loading conversations...</div>
        ) : conversations.length === 0 ? (
          <div className="sidebar-empty">
            <FiMessageSquare />
            <p>No conversations yet</p>
            <span>Start a new chat to begin</span>
          </div>
        ) : (
          <div className="conversation-list">
            {conversations.map((conv) => (
              <div
                key={conv.conversation_id}
                className={`conversation-item ${conv.conversation_id === currentConversationId ? "active" : ""}`}
                onClick={() => onSelectConversation(conv.conversation_id)}
              >
                <div className="conversation-header">
                  <FiMessageSquare className="conversation-icon" />
                  <span className="conversation-title">{conv.title || "Untitled Chat"}</span>
                </div>
                <div className="conversation-meta">
                  <span className="conversation-date">{formatDate(conv.created_at)}</span>
                  <span className="conversation-count">{conv.message_count} messages</span>
                </div>
                <button
                  className="delete-conversation-btn"
                  onClick={(e) => handleDeleteConversation(conv.conversation_id, e)}
                  title="Delete conversation"
                >
                  <FiTrash2 />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
    )
  }
)

ChatSidebar.displayName = "ChatSidebar"

export default ChatSidebar

