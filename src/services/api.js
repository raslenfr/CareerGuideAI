// Use relative URLs so requests go through Vite's proxy
const API_BASE_URL = "/api"

// Helper function to get JWT token from localStorage
const getAuthToken = () => {
  return localStorage.getItem("jwt_token")
}

// Helper function to get auth headers with JWT
const getAuthHeaders = () => {
  const token = getAuthToken()
  const headers = {
    "Content-Type": "application/json",
  }
  
  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }
  
  return headers
}

// Helper function for handling API responses
const handleResponse = async (response) => {
  const data = await response.json()
  
  // Handle token expiry - logout user
  if (response.status === 401 && getAuthToken()) {
    localStorage.removeItem("jwt_token")
    localStorage.removeItem("user")
    window.location.href = "/login"
    return Promise.reject("Session expired. Please login again.")
  }
  
  if (!response.ok) {
    const error = (data && data.error) || response.statusText
    return Promise.reject(error)
  }
  return data
}

// Helper function to handle API errors
const handleApiError = (error) => {
  console.error("API Error:", error)
  if (error.message === "Failed to fetch" || error.message === "NetworkError when attempting to fetch resource.") {
    return {
      success: false,
      error: "Network error: Unable to connect to the server. Please check if the backend server is running on port 5000.",
    }
  }
  return {
    success: false,
    error: error.toString(),
  }
}

// Chatbot API (JWT Protected)
export const sendChatMessage = async (message, history = [], userId = null, conversationId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chatbot/message`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        message,
        history,
        user_id: userId,
        conversation_id: conversationId,
      }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const getChatConversations = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chatbot/conversations?user_id=${userId}`, {
      method: "GET",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const getChatConversation = async (conversationId, userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${conversationId}?user_id=${userId}`, {
      method: "GET",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const deleteChatConversation = async (conversationId, userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${conversationId}?user_id=${userId}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const saveConversation = async (userId, messages, conversationId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chatbot/save-conversation`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        user_id: userId,
        messages: messages,
        conversation_id: conversationId,
      }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

// Career Suggester API
export const startSuggestion = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggester/start`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const submitSuggesterAnswer = async (answer, currentQuestionIndex, answersSoFar) => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggester/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        answer,
        current_question_index: currentQuestionIndex,
        answers_so_far: answersSoFar,
      }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const saveSuggesterSession = async (userId, answers, suggestions, sessionId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggester/save-session`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        user_id: userId,
        answers: answers,
        suggestions: suggestions,
        session_id: sessionId,
      }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const getSuggesterSessions = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggester/sessions?user_id=${userId}`, {
      method: "GET",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const getSuggesterSession = async (sessionId, userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggester/sessions/${sessionId}?user_id=${userId}`, {
      method: "GET",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const deleteSuggesterSession = async (sessionId, userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggester/sessions/${sessionId}?user_id=${userId}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

// Course Recommender API
export const startRecommendation = async (keywords, location = "Tunisia") => {
  try {
    const response = await fetch(`${API_BASE_URL}/recommender/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keywords, location }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const submitRecommenderSurvey = async (requestId, answers) => {
  try {
    const response = await fetch(`${API_BASE_URL}/recommender/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ request_id: requestId, answers }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

// Authentication API (JWT)
export const loginUser = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const signupUser = async (name, email, password, username = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        name, 
        email, 
        password,
        username: username || email.split('@')[0],
        role: 'student' // Always student for public signups
      }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const getCurrentUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      method: "GET",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const sendVerificationCode = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/send-verification`, {
      method: "POST",
      headers: getAuthHeaders(),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}

export const verifyEmail = async (code) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/verify-email`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ code }),
    })
    return handleResponse(response)
  } catch (error) {
    return handleApiError(error)
  }
}
