/**
 * Test Status Indicator
 * Shows when test recording is active and displays current AI type
 */

import { useTest } from '../../context/TestContext';
import { FiActivity, FiMessageSquare, FiCompass, FiBook } from 'react-icons/fi';
import './TestStatusIndicator.css';

const TestStatusIndicator = () => {
  const { isTestMode, isRecording, currentAiType, interactionCount } = useTest();

  // Don't show anything if test mode is off
  if (!isTestMode) {
    return null;
  }

  // Map AI types to display names and icons
  const aiTypeInfo = {
    chatbot: { name: 'Chatbot AI', icon: FiMessageSquare, color: '#3b82f6' },
    career_suggester: { name: 'Career Suggester AI', icon: FiCompass, color: '#8b5cf6' },
    course_recommender: { name: 'Course Recommender AI', icon: FiBook, color: '#f59e0b' },
  };

  const currentInfo = currentAiType ? aiTypeInfo[currentAiType] : null;
  const Icon = currentInfo?.icon || FiActivity;

  return (
    <div className={`test-status-indicator ${isRecording ? 'recording' : ''}`}>
      {isRecording ? (
        <>
          <div className="recording-pulse" style={{ backgroundColor: '#ef4444' }}></div>
          <Icon style={{ color: currentInfo?.color || '#64748b' }} />
          <span className="status-text">
            Recording {currentInfo ? currentInfo.name : 'AI'} 
            <span className="interaction-count"> ({interactionCount})</span>
          </span>
        </>
      ) : (
        <>
          <FiActivity style={{ color: '#22c55e' }} />
          <span className="status-text">
            Test Mode Active {currentInfo && `- ${currentInfo.name} Detected`}
          </span>
        </>
      )}
    </div>
  );
};

export default TestStatusIndicator;

