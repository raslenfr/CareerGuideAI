"use client"

import { useState } from "react"
import { FiBookOpen, FiSearch, FiFilter, FiStar, FiClock, FiDollarSign, FiLoader, FiAlertCircle } from "react-icons/fi"
import { startRecommendation, submitRecommenderSurvey } from "../services/api"
import { useTest } from "../context/TestContext"
import { toast } from "react-toastify"
import "./CourseRecommender.css"

const CourseRecommender = () => {
  const { isTestMode, isRecording, logInteraction } = useTest()
  const [searchKeywords, setSearchKeywords] = useState("")
  const [searchLocation, setSearchLocation] = useState("Tunisia")
  const [isSearching, setIsSearching] = useState(false)
  const [searchComplete, setSearchComplete] = useState(false)
  const [requestId, setRequestId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [recommendations, setRecommendations] = useState([])
  const [showRecommendations, setShowRecommendations] = useState(false)
  const [error, setError] = useState(null)
  const [connectionError, setConnectionError] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()

    if (!searchKeywords.trim()) {
      toast.warning("Please enter keywords to search for courses.")
      return
    }

    setIsSearching(true)
    setError(null)
    setConnectionError(false)

    try {
      const response = await startRecommendation(searchKeywords, searchLocation)

      if (response.success) {
        setRequestId(response.request_id)
        setQuestions(response.questions)
        setSearchComplete(true)

        // Initialize answers object with empty values
        const initialAnswers = {}
        response.questions.forEach((q) => {
          initialAnswers[q.id] = ""
        })
        setAnswers(initialAnswers)

        if (response.questions.length === 0) {
          toast.info("No questions available for this search. Please try different keywords.")
        }
      } else {
        setError(response.error || "Failed to start recommendation process.")
        if (response.error && response.error.includes("Network error")) {
          setConnectionError(true)
          toast.error("Connection error. Please check if the backend server is running.")
        } else {
          toast.error(response.error || "Failed to start recommendation process.")
        }
      }
    } catch (error) {
      console.error("Error starting recommendation:", error)
      setError("Network error. Please try again later.")
      setConnectionError(true)
      toast.error("Network error. Please check if the backend server is running.")
    } finally {
      setIsSearching(false)
    }
  }

  const handleAnswerChange = (questionId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }))
  }

  const handleSubmitSurvey = async () => {
    // Check if all questions are answered
    const unansweredQuestions = questions.filter((q) => !answers[q.id])

    if (unansweredQuestions.length > 0) {
      toast.warning("Please answer all questions before submitting.")
      return
    }

    setIsSubmitting(true)
    setError(null)

    try {
      const startTime = Date.now()
      const response = await submitRecommenderSurvey(requestId, answers)
      const responseTime = Date.now() - startTime

      if (response.success) {
        setRecommendations(response.recommendations)
        setShowRecommendations(true)
        window.scrollTo(0, 0)

        // Log interaction if test mode is active and recording
        if (isTestMode && isRecording) {
          logInteraction({
            keywords: searchKeywords,
            location: searchLocation,
            survey_answers: answers,
            courses: response.recommendations,
            response_time_ms: responseTime,
            total_recommendations: response.recommendations.length,
          })
        }
      } else {
        setError(response.error || "Failed to get recommendations.")
        if (response.error && response.error.includes("Network error")) {
          setConnectionError(true)
          toast.error("Connection error. Please check if the backend server is running.")
        } else {
          toast.error(response.error || "Failed to get recommendations.")
        }
      }
    } catch (error) {
      console.error("Error submitting survey:", error)
      setError("Network error. Please try again later.")
      setConnectionError(true)
      toast.error("Network error. Please check if the backend server is running.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleReset = () => {
    setSearchKeywords("")
    setSearchLocation("Tunisia")
    setSearchComplete(false)
    setRequestId(null)
    setQuestions([])
    setAnswers({})
    setRecommendations([])
    setShowRecommendations(false)
    setError(null)
    setConnectionError(false)
  }

  if (error) {
    return (
      <div className="course-recommender-page">
        <div className="page-header">
          <div className="header-icon">
            <FiBookOpen />
          </div>
          <div className="header-content">
            <h1>Course Finder</h1>
            <p>Discover the perfect courses to help you acquire the skills you need</p>
          </div>
        </div>

        <div className="recommender-error">
          <FiAlertCircle className="error-icon" />
          <h2>Oops! Something went wrong</h2>
          <p>{error}</p>
          {connectionError && (
            <div className="connection-error-message">
              <p>It looks like there might be an issue connecting to the backend server.</p>
              <p>Please make sure the Flask server is running on port 5000.</p>
            </div>
          )}
          <button onClick={handleReset} className="restart-button">
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="course-recommender-page">
      <div className="page-header">
        <div className="header-icon">
          <FiBookOpen />
        </div>
        <div className="header-content">
          <h1>Course Finder</h1>
          <p>Discover the perfect courses to help you acquire the skills you need</p>
        </div>
      </div>

      <div className="recommender-container">
        {!searchComplete ? (
          <div className="search-section">
            <div className="search-card">
              <h2>What would you like to learn?</h2>
              <p>Enter keywords related to skills, technologies, or career paths you're interested in</p>

              <form onSubmit={handleSearch} className="search-form">
                <div className="search-input-group">
                  <FiSearch className="search-icon" />
                  <input
                    type="text"
                    placeholder="e.g., Python, Data Science, Web Development"
                    value={searchKeywords}
                    onChange={(e) => setSearchKeywords(e.target.value)}
                    disabled={isSearching}
                  />
                </div>

                <div className="search-input-group">
                  <FiFilter className="search-icon" />
                  <select
                    value={searchLocation}
                    onChange={(e) => setSearchLocation(e.target.value)}
                    disabled={isSearching}
                  >
                    <option value="Tunisia">Tunisia</option>
                    <option value="Remote">Remote Only</option>
                    <option value="Global">Global</option>
                  </select>
                </div>

                <button type="submit" className="search-button" disabled={isSearching || !searchKeywords.trim()}>
                  {isSearching ? (
                    <>
                      <FiLoader className="spin" /> Searching...
                    </>
                  ) : (
                    "Find Courses"
                  )}
                </button>
              </form>

              <div className="popular-searches">
                <h3>Popular Searches</h3>
                <div className="search-tags">
                  <button onClick={() => setSearchKeywords("Python Programming")}>Python Programming</button>
                  <button onClick={() => setSearchKeywords("Data Science")}>Data Science</button>
                  <button onClick={() => setSearchKeywords("Web Development")}>Web Development</button>
                  <button onClick={() => setSearchKeywords("Machine Learning")}>Machine Learning</button>
                  <button onClick={() => setSearchKeywords("UX Design")}>UX Design</button>
                </div>
              </div>
            </div>
          </div>
        ) : !showRecommendations ? (
          <div className="survey-section">
            <div className="survey-header">
              <h2>Help Us Find the Perfect Courses for You</h2>
              <p>Answer a few questions about your preferences and experience level</p>
            </div>

            <div className="survey-questions">
              {questions.map((question, index) => (
                <div className="question-item" key={question.id}>
                  <h3>Question {index + 1}</h3>
                  <p>{question.text}</p>

                  {question.text.includes("Rate") || question.text.includes("1=") ? (
                    <div className="rating-input">
                      {[1, 2, 3, 4, 5].map((value) => (
                        <label key={value} className={answers[question.id] == value ? "selected" : ""}>
                          <input
                            type="radio"
                            name={question.id}
                            value={value}
                            checked={answers[question.id] == value}
                            onChange={() => handleAnswerChange(question.id, value)}
                          />
                          {value}
                        </label>
                      ))}
                    </div>
                  ) : question.text.includes("Yes/No") ? (
                    <div className="yes-no-input">
                      <label className={answers[question.id] === "Yes" ? "selected" : ""}>
                        <input
                          type="radio"
                          name={question.id}
                          value="Yes"
                          checked={answers[question.id] === "Yes"}
                          onChange={() => handleAnswerChange(question.id, "Yes")}
                        />
                        Yes
                      </label>
                      <label className={answers[question.id] === "No" ? "selected" : ""}>
                        <input
                          type="radio"
                          name={question.id}
                          value="No"
                          checked={answers[question.id] === "No"}
                          onChange={() => handleAnswerChange(question.id, "No")}
                        />
                        No
                      </label>
                      <label className={answers[question.id] === "Learning" ? "selected" : ""}>
                        <input
                          type="radio"
                          name={question.id}
                          value="Learning"
                          checked={answers[question.id] === "Learning"}
                          onChange={() => handleAnswerChange(question.id, "Learning")}
                        />
                        Learning
                      </label>
                    </div>
                  ) : (
                    <input
                      type="text"
                      value={answers[question.id] || ""}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                      placeholder="Type your answer here..."
                    />
                  )}
                </div>
              ))}
            </div>

            <div className="survey-actions">
              <button className="back-button" onClick={handleReset}>
                Back to Search
              </button>
              <button className="submit-button" onClick={handleSubmitSurvey} disabled={isSubmitting}>
                {isSubmitting ? (
                  <>
                    <FiLoader className="spin" /> Finding Courses...
                  </>
                ) : (
                  "Get Recommendations"
                )}
              </button>
            </div>
          </div>
        ) : (
          <div className="recommendations-section">
            <div className="recommendations-header">
              <h2>Recommended Courses for You</h2>
              <p>Based on your preferences and experience level</p>
            </div>

            <div className="course-filters">
              <button className="filter-button active">All Courses</button>
              <button className="filter-button">Beginner Friendly</button>
              <button className="filter-button">Advanced</button>
              <button className="filter-button">Free Courses</button>
            </div>

            <div className="course-list">
              {recommendations.length > 0 ? (
                recommendations.map((course, index) => (
                  <div className="course-card" key={index}>
                    <div className="course-header">
                      <h3>{course.title}</h3>
                      <div className="match-score">
                        <span>{Math.round(course.match_score * 100)}%</span> Match
                      </div>
                    </div>

                    <div className="course-provider">
                      <img src="/placeholder.svg?height=30&width=30" alt={course.company} />
                      <span>{course.company}</span>
                    </div>

                    <p className="course-description">{course.description}</p>

                    <div className="course-details">
                      <div className="detail-item">
                        <FiStar />
                        <span>4.8 (2,345 reviews)</span>
                      </div>
                      <div className="detail-item">
                        <FiClock />
                        <span>6 weeks</span>
                      </div>
                      <div className="detail-item">
                        <FiDollarSign />
                        <span>₹4,999</span>
                      </div>
                    </div>

                    <div className="course-skills">
                      <h4>Skills you'll gain:</h4>
                      <div className="skill-tags">
                        {course.skills.split(",").map((skill, i) => (
                          <span key={i} className="skill-tag">
                            {skill.trim()}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="course-match">
                      <h4>Why this is a good match:</h4>
                      <p>{course.reason}</p>
                    </div>

                    <div className="course-actions">
                      <button className="enroll-button">View Course</button>
                      <button className="save-button">Save for Later</button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-courses">
                  <h3>No courses found</h3>
                  <p>We couldn't find any courses matching your criteria. Try adjusting your search or preferences.</p>
                  <button className="restart-button" onClick={handleReset}>
                    Start a New Search
                  </button>
                </div>
              )}
            </div>

            <div className="recommendations-actions">
              <button className="restart-button" onClick={handleReset}>
                Start a New Search
              </button>
              <button className="save-button">Save These Recommendations</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default CourseRecommender
