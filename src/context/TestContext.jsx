/**
 * Test Context
 * Manages frontend-integrated AI testing state and recording
 */

import { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import TestResultsModal from '../components/common/TestResultsModal';

const TestContext = createContext();

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Map routes to AI types
const ROUTE_TO_AI_TYPE = {
  '/chatbot': 'chatbot',
  '/career-suggester': 'career_suggester',
  '/course-recommender': 'course_recommender',
};

export const TestProvider = ({ children }) => {
  const [isTestMode, setIsTestMode] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [currentAiType, setCurrentAiType] = useState(null);
  const [interactionCount, setInteractionCount] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [modalReport, setModalReport] = useState(null);
  const location = useLocation();

  // Automatically detect AI type based on current route
  useEffect(() => {
    const aiType = ROUTE_TO_AI_TYPE[location.pathname];
    if (aiType) {
      setCurrentAiType(aiType);
    } else {
      setCurrentAiType(null);
    }
  }, [location.pathname]);

  // Toggle test mode
  const toggleTestMode = useCallback(() => {
    const newMode = !isTestMode;
    setIsTestMode(newMode);
    
    // If turning off test mode while recording, stop recording
    if (!newMode && isRecording) {
      stopRecording();
    }
    
    toast.info(newMode ? '🧪 Test Mode Enabled' : 'Test Mode Disabled');
  }, [isTestMode, isRecording]);

  // Start test recording
  const startRecording = useCallback(async (userId = null) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tests/start-recording`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId }),
      });

      const data = await response.json();

      if (data.success) {
        setSessionId(data.session_id);
        setIsRecording(true);
        setInteractionCount(0);
        toast.success('🔴 Recording Started');
        return { success: true, session_id: data.session_id };
      } else {
        toast.error('Failed to start recording: ' + (data.error || 'Unknown error'));
        return { success: false, error: data.error };
      }
    } catch (error) {
      console.error('Error starting recording:', error);
      toast.error('Network error starting recording');
      return { success: false, error: error.message };
    }
  }, []);

  // Log an AI interaction
  const logInteraction = useCallback(async (interactionData) => {
    if (!isRecording || !sessionId || !currentAiType) {
      return { success: false, error: 'Not recording or no AI type detected' };
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/tests/log-interaction`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          ai_type: currentAiType,
          interaction: interactionData,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setInteractionCount(data.total_interactions);
        return { success: true };
      } else {
        console.error('Failed to log interaction:', data.error);
        return { success: false, error: data.error };
      }
    } catch (error) {
      console.error('Error logging interaction:', error);
      return { success: false, error: error.message };
    }
  }, [isRecording, sessionId, currentAiType]);

  // Stop recording and generate report
  const stopRecording = useCallback(async () => {
    if (!sessionId) {
      toast.warning('No active recording session');
      return { success: false, error: 'No session' };
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/tests/stop-recording`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId }),
      });

      const data = await response.json();

      if (data.success) {
        const report = data.report;
        setIsRecording(false);
        setSessionId(null);
        setInteractionCount(0);
        
        // Show detailed modal with report
        setModalReport(report);
        setShowModal(true);
        
        return { success: true, report: report };
      } else {
        toast.error('Failed to stop recording: ' + (data.error || 'Unknown error'));
        return { success: false, error: data.error };
      }
    } catch (error) {
      console.error('Error stopping recording:', error);
      toast.error('Network error stopping recording');
      return { success: false, error: error.message };
    }
  }, [sessionId]);

  // Close modal
  const closeModal = useCallback(() => {
    setShowModal(false);
    setModalReport(null);
  }, []);

  const value = {
    isTestMode,
    isRecording,
    sessionId,
    currentAiType,
    interactionCount,
    toggleTestMode,
    startRecording,
    stopRecording,
    logInteraction,
    closeModal,
  };

  return (
    <TestContext.Provider value={value}>
      {children}
      {showModal && <TestResultsModal report={modalReport} onClose={closeModal} />}
    </TestContext.Provider>
  );
};

export const useTest = () => {
  const context = useContext(TestContext);
  if (context === undefined) {
    throw new Error('useTest must be used within a TestProvider');
  }
  return context;
};

export default TestContext;

