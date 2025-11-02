"use client"

import { useEffect } from "react"
import { Link } from "react-router-dom"
import {
  FiArrowRight,
  FiMessageSquare,
  FiCompass,
  FiBookOpen,
  FiUsers,
  FiCheck,
  FiBarChart2,
  FiAward,
  FiTrendingUp,
} from "react-icons/fi"
import Header from "../components/common/Header"
import Footer from "../components/common/Footer"
import "./Home.css"

const Home = () => {
  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-in")
        }
      })
    }, observerOptions)

    const elements = document.querySelectorAll(".animate")
    elements.forEach((el) => observer.observe(el))

    return () => {
      elements.forEach((el) => observer.unobserve(el))
    }
  }, [])

  return (
    <div className="home-page">
      <Header />

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <span className="hero-eyebrow animate">AI-Powered Career Guidance</span>
          <h1 className="hero-title animate">
            Discover Your <span className="highlight">Perfect</span> Career Path
          </h1>
          <p className="hero-subtitle animate">
            Navigate career transitions, find the right courses, and build essential skills with personalized AI
            guidance tailored to your unique profile and goals.
          </p>
          <div className="hero-cta animate">
            <Link to="/signup" className="primary-btn">
              Get Started <FiArrowRight />
            </Link>
            <Link to="/chatbot" className="secondary-btn">
              Try the Chatbot
            </Link>
          </div>
          <div className="hero-stats animate">
            <div className="hero-stat">
              <span className="stat-number">10k+</span>
              <span className="stat-label">Active Users</span>
            </div>
            <div className="hero-stat">
              <span className="stat-number">95%</span>
              <span className="stat-label">Success Rate</span>
            </div>
            <div className="hero-stat">
              <span className="stat-number">500+</span>
              <span className="stat-label">Career Paths</span>
            </div>
          </div>
        </div>
        <div className="hero-image animate">
          <div className="hero-image-wrapper">
            <img src="/hero-image.svg" alt="Career guidance illustration" />
            <div className="hero-floating-element hero-element-1">
              <FiBarChart2 />
              <span>Data Analysis</span>
            </div>
            <div className="hero-floating-element hero-element-2">
              <FiAward />
              <span>Certifications</span>
            </div>
            <div className="hero-floating-element hero-element-3">
              <FiTrendingUp />
              <span>Career Growth</span>
            </div>
          </div>
        </div>
      </section>

      {/* Trusted By Section */}
      <section className="trusted-section">
        <div className="trusted-container">
          <h2 className="trusted-title">Trusted by leading organizations</h2>
          <div className="trusted-logos">
            <div className="trusted-logo">
              <img src="/placeholder.svg?height=40&width=120" alt="Company 1" />
            </div>
            <div className="trusted-logo">
              <img src="/placeholder.svg?height=40&width=120" alt="Company 2" />
            </div>
            <div className="trusted-logo">
              <img src="/placeholder.svg?height=40&width=120" alt="Company 3" />
            </div>
            <div className="trusted-logo">
              <img src="/placeholder.svg?height=40&width=120" alt="Company 4" />
            </div>
            <div className="trusted-logo">
              <img src="/placeholder.svg?height=40&width=120" alt="Company 5" />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="section-header animate">
            <span className="section-eyebrow">Our Platform</span>
            <h2>How We Help You Succeed</h2>
            <p>Our AI-powered platform offers personalized guidance for every stage of your career journey</p>
          </div>

          <div className="features-grid">
            <div className="feature-card animate">
              <div className="feature-icon">
                <FiMessageSquare />
              </div>
              <div className="feature-content">
                <h3>AI Career Chat</h3>
                <p>Get instant answers to all your career questions from our intelligent chatbot assistant</p>
                <Link to="/chatbot" className="feature-link">
                  Try it now <FiArrowRight />
                </Link>
              </div>
            </div>

            <div className="feature-card animate">
              <div className="feature-icon">
                <FiCompass />
              </div>
              <div className="feature-content">
                <h3>Career Suggester</h3>
                <p>
                  Discover career paths that match your skills, interests, and goals through personalized
                  recommendations
                </p>
                <Link to="/career-suggester" className="feature-link">
                  Explore careers <FiArrowRight />
                </Link>
              </div>
            </div>

            <div className="feature-card animate">
              <div className="feature-icon">
                <FiBookOpen />
              </div>
              <div className="feature-content">
                <h3>Course Finder</h3>
                <p>Find the perfect courses and learning resources to help you acquire the skills you need</p>
                <Link to="/course-recommender" className="feature-link">
                  Find courses <FiArrowRight />
                </Link>
              </div>
            </div>

            <div className="feature-card animate">
              <div className="feature-icon">
                <FiUsers />
              </div>
              <div className="feature-content">
                <h3>Community Support</h3>
                <p>Connect with others on similar career paths and learn from their experiences</p>
                <Link to="/signup" className="feature-link">
                  Join community <FiArrowRight />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <div className="container">
          <div className="section-header animate">
            <span className="section-eyebrow">Simple Process</span>
            <h2>How It Works</h2>
            <p>Three simple steps to transform your career journey</p>
          </div>

          <div className="steps-container">
            <div className="step animate">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Share Your Background</h3>
                <p>Tell us about your education, skills, interests, and career goals</p>
                <ul className="step-list">
                  <li>
                    <FiCheck /> Educational background
                  </li>
                  <li>
                    <FiCheck /> Current skills and experience
                  </li>
                  <li>
                    <FiCheck /> Career interests and aspirations
                  </li>
                </ul>
              </div>
              <div className="step-image">
                <img src="/placeholder.svg?height=200&width=300" alt="Share your background" />
              </div>
            </div>

            <div className="step animate">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Get Personalized Recommendations</h3>
                <p>Our AI analyzes your profile to suggest optimal career paths and courses</p>
                <ul className="step-list">
                  <li>
                    <FiCheck /> AI-powered career matching
                  </li>
                  <li>
                    <FiCheck /> Tailored course recommendations
                  </li>
                  <li>
                    <FiCheck /> Skill gap analysis
                  </li>
                </ul>
              </div>
              <div className="step-image">
                <img src="/placeholder.svg?height=200&width=300" alt="Get personalized recommendations" />
              </div>
            </div>

            <div className="step animate">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Take Action</h3>
                <p>Follow your customized roadmap with detailed guidance every step of the way</p>
                <ul className="step-list">
                  <li>
                    <FiCheck /> Clear action steps
                  </li>
                  <li>
                    <FiCheck /> Progress tracking
                  </li>
                  <li>
                    <FiCheck /> Ongoing support and adjustments
                  </li>
                </ul>
              </div>
              <div className="step-image">
                <img src="/placeholder.svg?height=200&width=300" alt="Take action" />
              </div>
            </div>
          </div>

          <div className="cta-container animate">
            <Link to="/signup" className="primary-btn">
              Start Your Journey <FiArrowRight />
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header animate">
            <span className="section-eyebrow">Success Stories</span>
            <h2>Hear From Our Users</h2>
            <p>Real stories from people who transformed their careers with our guidance</p>
          </div>

          <div className="testimonials-grid">
            <div className="testimonial-card animate">
              <div className="testimonial-rating">
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
              </div>
              <div className="testimonial-content">
                <p>
                  "After 10 years as a teacher, I wanted to transition to tech. The Career Suggester helped me identify
                  UX design as a perfect fit for my skills, and recommended courses that got me job-ready in 6 months."
                </p>
              </div>
              <div className="testimonial-author">
                <img src="/placeholder.svg?height=60&width=60" alt="Priya S." className="author-image" />
                <div className="author-info">
                  <h4>Priya S.</h4>
                  <p>Teacher → UX Designer</p>
                </div>
              </div>
            </div>

            <div className="testimonial-card animate">
              <div className="testimonial-rating">
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
              </div>
              <div className="testimonial-content">
                <p>
                  "The AI chatbot helped me understand exactly what skills I needed to develop for a data science role.
                  The personalized learning path saved me months of figuring things out on my own."
                </p>
              </div>
              <div className="testimonial-author">
                <img src="/placeholder.svg?height=60&width=60" alt="Rahul M." className="author-image" />
                <div className="author-info">
                  <h4>Rahul M.</h4>
                  <p>Marketing Analyst → Data Scientist</p>
                </div>
              </div>
            </div>

            <div className="testimonial-card animate">
              <div className="testimonial-rating">
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
              </div>
              <div className="testimonial-content">
                <p>
                  "As a mid-career professional, I was skeptical about changing industries. The Course Finder
                  recommended specialized certifications that helped me leverage my existing experience while building
                  new skills."
                </p>
              </div>
              <div className="testimonial-author">
                <img src="/placeholder.svg?height=60&width=60" alt="Ananya K." className="author-image" />
                <div className="author-info">
                  <h4>Ananya K.</h4>
                  <p>Finance Manager → FinTech Consultant</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-highlight-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-highlight animate">
              <span className="stat-number">95%</span>
              <span className="stat-description">of users find relevant career paths within 2 weeks</span>
            </div>
            <div className="stat-highlight animate">
              <span className="stat-number">78%</span>
              <span className="stat-description">successfully transition to new careers within 12 months</span>
            </div>
            <div className="stat-highlight animate">
              <span className="stat-number">25k+</span>
              <span className="stat-description">courses recommended to match user skills and goals</span>
            </div>
            <div className="stat-highlight animate">
              <span className="stat-number">40%</span>
              <span className="stat-description">average salary increase after career transition</span>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="faq-section">
        <div className="container">
          <div className="section-header animate">
            <span className="section-eyebrow">Questions & Answers</span>
            <h2>Frequently Asked Questions</h2>
            <p>Find answers to common questions about our platform</p>
          </div>

          <div className="faq-grid">
            <div className="faq-item animate">
              <h3>How does the AI career matching work?</h3>
              <p>
                Our AI analyzes your skills, experience, interests, and goals to identify career paths that align with
                your profile. It uses data from thousands of successful career transitions to provide accurate
                recommendations.
              </p>
            </div>
            <div className="faq-item animate">
              <h3>Is CareerGuide AI free to use?</h3>
              <p>
                We offer a free tier with basic features and premium plans with advanced guidance, unlimited
                recommendations, and personalized coaching. You can start with the free version to explore the platform.
              </p>
            </div>
            <div className="faq-item animate">
              <h3>How accurate are the course recommendations?</h3>
              <p>
                Our course recommendations are based on your skill gaps, learning style, and career goals. We partner
                with leading education providers to ensure high-quality, relevant course suggestions.
              </p>
            </div>
            <div className="faq-item animate">
              <h3>Can I use CareerGuide AI if I'm just starting my career?</h3>
              <p>
                CareerGuide AI is designed for professionals at all stages, from students and recent graduates to
                experienced professionals looking to pivot or advance their careers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content animate">
          <h2>Ready to Find Your Perfect Career Path?</h2>
          <p>Join thousands of professionals who have transformed their careers with our AI-powered guidance</p>
          <div className="cta-buttons">
            <Link to="/signup" className="primary-btn">
              Get Started for Free <FiArrowRight />
            </Link>
            <Link to="/chatbot" className="outline-btn">
              Try the AI Chat
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default Home
