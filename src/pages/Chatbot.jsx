"use client"

import { useState, useEffect, useRef } from "react"
import { FiMessageCircle, FiHelpCircle, FiSave, FiCheck } from "react-icons/fi"
import ChatWindow from "../components/chatbot/ChatWindow"
import ChatSidebar from "../components/chatbot/ChatSidebar"
import { useAuth } from "../hooks/useAuth"
import { getChatConversation, saveConversation } from "../services/api"
import { toast } from "react-toastify"
import "./Chatbot.css"

const Chatbot = () => {
  const { user } = useAuth()
  const [showTips, setShowTips] = useState(true)
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi there! I'm Raslen Ferchichi, your AI Career Guide. How can I help with your career questions today?",
    },
  ])
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [isSaved, setIsSaved] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const sidebarRef = useRef(null)
  const hasUnsavedChangesRef = useRef(false)

  const sampleQuestions = [
    "What skills should I develop to transition from teaching to instructional design?",
    "How can I prepare for a career in data science if I have a background in marketing?",
    "What certifications are most valuable for a career in cybersecurity?",
    "How do I create a portfolio for UX design with no professional experience?",
    "What's the career outlook for AI specialists in Tunisia over the next 5 years?",
  ]

  // Track when messages change (unsaved changes)
  useEffect(() => {
    // Only track unsaved changes for conversations with actual user messages
    const hasUserMessages = messages.some((msg) => msg.role === "user")
    hasUnsavedChangesRef.current = hasUserMessages && !isSaved
  }, [messages, isSaved])

  // Auto-save on component unmount (navigation away)
  useEffect(() => {
    return () => {
      if (hasUnsavedChangesRef.current && user?.id) {
        // Save conversation before unmounting
        saveChatToDatabase(true)
      }
    }
  }, [])

  // Save conversation to database
  const saveChatToDatabase = async (isSilent = false) => {
    if (!user?.id) {
      if (!isSilent) toast.error("You must be logged in to save conversations")
      return
    }

    // Filter out system/welcome messages, only save actual conversation
    const conversationMessages = messages.filter((msg, index) => {
      // Skip the first assistant message if it's the welcome message
      if (index === 0 && msg.role === "assistant") return false
      return true
    })

    if (conversationMessages.length < 2) {
      if (!isSilent) toast.warning("Need at least one message exchange to save")
      return
    }

    setIsSaving(true)

    try {
      const response = await saveConversation(user.id, conversationMessages, currentConversationId)

      if (response.success) {
        setIsSaved(true)
        setCurrentConversationId(response.conversation_id)
        hasUnsavedChangesRef.current = false

        if (!isSilent) {
          // Show different message for update vs new save
          const isUpdate = response.is_update || false
          const successMessage = isUpdate ? "Chat updated successfully!" : "Chat saved successfully!"
          toast.success(successMessage)
          
          // Refresh sidebar to show updated/new conversation
          if (sidebarRef.current) {
            sidebarRef.current.loadConversations()
          }
        }
      } else {
        if (!isSilent) {
          toast.error(response.error || "Failed to save conversation")
        }
      }
    } catch (error) {
      console.error("Error saving conversation:", error)
      if (!isSilent) toast.error("Error saving conversation")
    } finally {
      setIsSaving(false)
    }
  }

  // Handler to load a conversation
  const handleSelectConversation = async (conversationId) => {
    try {
      const response = await getChatConversation(conversationId, user?.id)
      if (response.success && response.conversation) {
        setMessages(response.conversation.history)
        setCurrentConversationId(conversationId)
        setIsSaved(true) // Loaded conversations are already saved
        hasUnsavedChangesRef.current = false
      } else {
        toast.error("Failed to load conversation")
      }
    } catch (error) {
      console.error("Error loading conversation:", error)
      toast.error("Error loading conversation")
    }
  }

  // Handler to start a new chat
  const handleNewChat = () => {
    setMessages([
      {
        role: "assistant",
        content: "Hi there! I'm Raslen Ferchichi, your AI Career Guide. How can I help with your career questions today?",
      },
    ])
    setCurrentConversationId(null)
    setIsSaved(false)
    hasUnsavedChangesRef.current = false
  }

  // Handler when messages change
  const handleMessagesChange = (newMessages) => {
    setMessages(newMessages)
    setIsSaved(false) // Mark as unsaved when new messages are added
  }

  // Function to handle clicking on a suggested prompt
  const handleSampleQuestionClick = (question) => {
    // This function is used in the right sidebar
    // The actual handler is in ChatWindow component
    if (window.handleSuggestedPrompt) {
      window.handleSuggestedPrompt(question)
    }
  }

  // Check if there are messages to save
  const hasMessagesToSave = messages.some((msg) => msg.role === "user")

  return (
    <div className="chatbot-page">
      <div className="page-header">
        <div className="header-icon">
          <FiMessageCircle />
        </div>
        <div className="header-content">
          <h1>Career Guide Chat</h1>
          <p>Ask any questions about career paths, skills, education, or job market trends</p>
        </div>
        {user && (
          <button
            className={`save-chat-btn ${isSaved ? "saved" : ""}`}
            onClick={() => saveChatToDatabase(false)}
            disabled={isSaving || isSaved || !hasMessagesToSave}
            title={isSaved ? "Chat up to date" : currentConversationId ? "Update this chat" : "Save this chat"}
          >
            {isSaving ? (
              <>
                <FiSave className="spin" />
                {currentConversationId ? "Updating..." : "Saving..."}
              </>
            ) : isSaved ? (
              <>
                <FiCheck />
                Saved
              </>
            ) : (
              <>
                <FiSave />
                {currentConversationId ? "Update Chat" : "Save Chat"}
              </>
            )}
          </button>
        )}
      </div>

      <div className="chatbot-container with-history">
        {user && (
          <ChatSidebar
            ref={sidebarRef}
            userId={user.id}
            currentConversationId={currentConversationId}
            onSelectConversation={handleSelectConversation}
            onNewChat={handleNewChat}
            isCollapsed={isSidebarCollapsed}
            onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          />
        )}

        <div className="chat-main">
          <ChatWindow
            userId={user?.id}
            conversationId={currentConversationId}
            onConversationIdChange={setCurrentConversationId}
            messages={messages}
            onMessagesChange={handleMessagesChange}
          />

          {showTips && (
            <div className="chat-tips">
              <div className="tips-header">
                <h3>
                  <FiHelpCircle />
                  Tips for Better Conversations
                </h3>
                <button onClick={() => setShowTips(false)}>Hide</button>
              </div>
              <ul>
                <li>Be specific about your background, skills, and goals</li>
                <li>Ask about specific industries or roles you're interested in</li>
                <li>Inquire about skills, certifications, or education needed for specific careers</li>
                <li>Ask for advice on career transitions or upskilling</li>
              </ul>
            </div>
          )}
        </div>

        <div className="chat-sidebar-right">
          <div className="sample-questions">
            <h3>Try Asking</h3>
            <ul>
              {sampleQuestions.map((question, index) => (
                <li key={index}>
                  <button onClick={() => handleSampleQuestionClick(question)}>{question}</button>
                </li>
              ))}
            </ul>
          </div>

          <div className="chat-info">
            <h3>About This Chatbot</h3>
            <p>
              Our AI Career Guide is trained on career data and job market trends in Tunisia. It can provide guidance on
              career paths, skill development, education options, and job market insights.
            </p>
            <p>
              While our AI provides valuable information, consider consulting with human career counselors for
              personalized guidance.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Chatbot
