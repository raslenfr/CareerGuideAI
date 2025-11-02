"use client"

import { useState } from "react"
import { FiX, FiArrowRight, FiArrowLeft } from "react-icons/fi"
import "./GuideTour.css"

const GuideTour = ({ onClose }) => {
  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    {
      title: "Welcome to CareerGuide AI",
      description: "Let's take a quick tour to help you get started with our platform.",
      image: "/tour-welcome.svg",
    },
    {
      title: "AI Career Chat",
      description: "Ask our AI assistant any career-related questions and get personalized guidance.",
      image: "/tour-chat.svg",
    },
    {
      title: "Career Suggester",
      description:
        "Answer a few questions about your interests and skills to discover career paths that match your profile.",
      image: "/tour-suggester.svg",
    },
    {
      title: "Course Recommender",
      description:
        "Find the perfect courses and learning resources to help you acquire the skills you need for your desired career.",
      image: "/tour-courses.svg",
    },
    {
      title: "You're All Set!",
      description: "Start exploring the platform and take the first step towards your ideal career path.",
      image: "/tour-complete.svg",
    },
  ]

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      onClose()
    }
  }

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  return (
    <div className="guide-tour-overlay">
      <div className="guide-tour">
        <button className="close-tour" onClick={onClose}>
          <FiX />
        </button>

        <div className="tour-content">
          <div className="tour-image">
            <img src={steps[currentStep].image || "/placeholder.svg"} alt={steps[currentStep].title} />
          </div>

          <div className="tour-text">
            <h2>{steps[currentStep].title}</h2>
            <p>{steps[currentStep].description}</p>
          </div>
        </div>

        <div className="tour-progress">
          <div className="progress-dots">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`progress-dot ${index === currentStep ? "active" : ""}`}
                onClick={() => setCurrentStep(index)}
              />
            ))}
          </div>

          <div className="tour-buttons">
            {currentStep > 0 && (
              <button className="tour-button prev" onClick={handlePrev}>
                <FiArrowLeft />
                Previous
              </button>
            )}

            <button className="tour-button next" onClick={handleNext}>
              {currentStep < steps.length - 1 ? "Next" : "Get Started"}
              {currentStep < steps.length - 1 ? <FiArrowRight /> : null}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GuideTour
