/**
 * Test Results Modal
 * Displays detailed test results after stopping recording
 */

import { FiX, FiCheckCircle, FiAlertTriangle, FiXCircle, FiClock, FiActivity } from 'react-icons/fi';
import './TestResultsModal.css';

const TestResultsModal = ({ report, onClose }) => {
  if (!report) return null;

  const getStatusIcon = (status) => {
    switch (status) {
      case 'PASS':
        return <FiCheckCircle className="status-icon pass" />;
      case 'WARNING':
        return <FiAlertTriangle className="status-icon warning" />;
      case 'FAIL':
        return <FiXCircle className="status-icon fail" />;
      default:
        return <FiActivity className="status-icon" />;
    }
  };

  const getStatusClass = (status) => {
    return status?.toLowerCase() || 'unknown';
  };

  const aiTypeNames = {
    chatbot: 'Chatbot AI',
    career_suggester: 'Career Suggester AI',
    course_recommender: 'Course Recommender AI',
  };

  // Handle backdrop click
  const handleBackdropClick = (e) => {
    if (e.target.className.includes('modal-backdrop')) {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="test-results-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <h2>Test Results</h2>
          <button className="close-btn" onClick={onClose} title="Close">
            <FiX />
          </button>
        </div>

        {/* Content */}
        <div className="modal-content">
          {/* Overall Results */}
          <div className="result-section overall-section">
            <div className={`overall-status ${getStatusClass(report.status)}`}>
              {getStatusIcon(report.status)}
              <div className="overall-info">
                <h3>Overall Status: {report.status}</h3>
                <div className="overall-score">{report.overall_score?.toFixed(1)}/100</div>
              </div>
            </div>

            <div className="summary-grid">
              <div className="summary-item">
                <span className="summary-label">Total Interactions</span>
                <span className="summary-value">{report.summary?.total_interactions || 0}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Duration</span>
                <span className="summary-value">{report.duration_seconds?.toFixed(1)}s</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">AI Types Tested</span>
                <span className="summary-value">{report.summary?.ai_types_tested?.length || 0}</span>
              </div>
            </div>
          </div>

          {/* Per-AI Results */}
          {report.ai_reports && Object.keys(report.ai_reports).length > 0 && (
            <div className="result-section ai-results-section">
              <h3>AI Performance Breakdown</h3>
              {Object.entries(report.ai_reports).map(([aiType, aiReport]) => (
                <div key={aiType} className="ai-result-card">
                  <div className="ai-result-header">
                    <div className="ai-info">
                      <h4>{aiTypeNames[aiType] || aiType}</h4>
                      <span className={`ai-status ${getStatusClass(aiReport.status)}`}>
                        {getStatusIcon(aiReport.status)}
                        {aiReport.status}
                      </span>
                    </div>
                    <div className="ai-score">{aiReport.score?.toFixed(1)}/100</div>
                  </div>

                  <div className="ai-result-details">
                    <div className="detail-item">
                      <FiActivity />
                      <span>{aiReport.total_interactions} interactions</span>
                    </div>
                    <div className="detail-item">
                      <FiClock />
                      <span>Avg: {aiReport.avg_response_time_ms?.toFixed(0)}ms</span>
                    </div>
                  </div>

                  {/* Issues */}
                  {aiReport.issues && aiReport.issues.length > 0 && (
                    <div className="issues-list">
                      <h5>Issues Found:</h5>
                      {aiReport.issues.map((issue, idx) => (
                        <div key={idx} className={`issue-item ${issue.severity.toLowerCase()}`}>
                          <span className="issue-severity">{issue.severity}</span>
                          <span className="issue-desc">{issue.description}</span>
                          <span className="issue-details">{issue.details}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Quality Scores */}
                  {aiReport.quality_scores && aiReport.quality_scores.length > 0 && (
                    <div className="quality-scores">
                      <h5>Individual Scores:</h5>
                      <div className="score-bars">
                        {aiReport.quality_scores.map((score, idx) => (
                          <div key={idx} className="score-bar-item">
                            <span className="score-label">#{idx + 1}</span>
                            <div className="score-bar-wrapper">
                              <div
                                className={`score-bar ${score >= 70 ? 'good' : score >= 50 ? 'warning' : 'poor'}`}
                                style={{ width: `${score}%` }}
                              ></div>
                            </div>
                            <span className="score-value">{score}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Test Details */}
          <div className="result-section test-details-section">
            <h3>Test Information</h3>
            <div className="test-info-grid">
              <div className="info-item">
                <span className="info-label">Test ID:</span>
                <span className="info-value">{report.test_id}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Started:</span>
                <span className="info-value">{new Date(report.summary?.started_at).toLocaleString()}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Stopped:</span>
                <span className="info-value">{new Date(report.summary?.stopped_at).toLocaleString()}</span>
              </div>
              {report.report_file && (
                <div className="info-item">
                  <span className="info-label">Report File:</span>
                  <span className="info-value">{report.report_file}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="modal-footer">
          <button className="btn-primary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default TestResultsModal;

