"use client"

import { useState, useEffect } from "react"
import { FiUser, FiAlertCircle } from "react-icons/fi"
import "./ChatMessage.css"

const ChatMessage = ({ message, isLast }) => {
  const [displayedContent, setDisplayedContent] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const isUser = message.role === "user"
  const isError = message.isError

  useEffect(() => {
    if (isLast && !isUser && !isError) {
      setIsTyping(true)
      let i = 0
      const content = message.content
      const typingInterval = setInterval(() => {
        if (i < content.length) {
          setDisplayedContent(content.substring(0, i + 1))
          i++
        } else {
          clearInterval(typingInterval)
          setIsTyping(false)
        }
      }, 15) // Adjust typing speed here

      return () => clearInterval(typingInterval)
    } else {
      setDisplayedContent(message.content)
    }
  }, [message, isLast, isUser, isError])

  return (
    <div className={`chat-message ${isUser ? "user" : "assistant"} ${isError ? "error" : ""}`}>
      <div className="message-avatar">
        {isUser ? (
          <div className="user-avatar">
            <FiUser />
          </div>
        ) : (
          <div className="assistant-avatar">
            {isError ? <FiAlertCircle /> : <img src="/ai-avatar.svg" alt="AI Assistant" />}
          </div>
        )}
      </div>
      <div className="message-content">
        <div className="message-bubble">
          {isUser ? message.content : displayedContent}
          {isTyping && <span className="cursor"></span>}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
