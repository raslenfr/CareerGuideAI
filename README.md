# 🎓 CareerGuide AI - Frontend System

A modern React frontend application that provides an intuitive interface for career guidance, course recommendations, and AI-powered career advice. Built with React and Vite, featuring a responsive design tailored for the Tunisian market.

## 🏗️ Project Structure

<table>
<thead>
<tr>
<th>Folder/File</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Frontend/</strong></td>
<td>Folder</td>
<td>Root frontend directory</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>src/</strong></td>
<td>Folder</td>
<td>Source code directory</td>
</tr>
<tr>
<td style="padding-left: 60px;">App.jsx</td>
<td>File</td>
<td>Main React application component</td>
</tr>
<tr>
<td style="padding-left: 60px;">main.jsx</td>
<td>File</td>
<td>Application entry point</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>components/</strong></td>
<td>Folder</td>
<td>React components organized by feature</td>
</tr>
<tr>
<td style="padding-left: 90px;"><strong>common/</strong></td>
<td>Folder</td>
<td>Shared components</td>
</tr>
<tr>
<td style="padding-left: 120px;">Header.jsx</td>
<td>File</td>
<td>Header with navigation and test controls</td>
</tr>
<tr>
<td style="padding-left: 120px;">Footer.jsx</td>
<td>File</td>
<td>Footer component</td>
</tr>
<tr>
<td style="padding-left: 120px;">TestStatusIndicator.jsx</td>
<td>File</td>
<td>Recording status indicator</td>
</tr>
<tr>
<td style="padding-left: 120px;">TestResultsModal.jsx</td>
<td>File</td>
<td>Detailed test results popup</td>
</tr>
<tr>
<td style="padding-left: 90px;"><strong>chatbot/</strong></td>
<td>Folder</td>
<td>Chatbot interface components</td>
</tr>
<tr>
<td style="padding-left: 120px;">ChatWindow.jsx</td>
<td>File</td>
<td>Main chat interface</td>
</tr>
<tr>
<td style="padding-left: 120px;">ChatMessage.jsx</td>
<td>File</td>
<td>Individual message bubbles</td>
</tr>
<tr>
<td style="padding-left: 120px;">ChatSidebar.jsx</td>
<td>File</td>
<td>Conversation history sidebar</td>
</tr>
<tr>
<td style="padding-left: 90px;"><strong>suggester/</strong></td>
<td>Folder</td>
<td>Career assessment components</td>
</tr>
<tr>
<td style="padding-left: 120px;">SuggesterSidebar.jsx</td>
<td>File</td>
<td>Career assessment session history</td>
</tr>
<tr>
<td style="padding-left: 90px;"><strong>layout/</strong></td>
<td>Folder</td>
<td>Layout components</td>
</tr>
<tr>
<td style="padding-left: 120px;">MainLayout.jsx</td>
<td>File</td>
<td>App layout wrapper</td>
</tr>
<tr>
<td style="padding-left: 90px;"><strong>onboarding/</strong></td>
<td>Folder</td>
<td>User onboarding components</td>
</tr>
<tr>
<td style="padding-left: 120px;">GuideTour.jsx</td>
<td>File</td>
<td>User onboarding tour</td>
</tr>
<tr>
<td style="padding-left: 90px;"><strong>admin/</strong></td>
<td>Folder</td>
<td>Admin interface components</td>
</tr>
<tr>
<td style="padding-left: 120px;">AdminDashboard.jsx</td>
<td>File</td>
<td>Admin main dashboard</td>
</tr>
<tr>
<td style="padding-left: 120px;">UserManagement.jsx</td>
<td>File</td>
<td>User management interface</td>
</tr>
<tr>
<td style="padding-left: 120px;">FraudDetection.jsx</td>
<td>File</td>
<td>Fraud review interface</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>pages/</strong></td>
<td>Folder</td>
<td>Application pages/routes</td>
</tr>
<tr>
<td style="padding-left: 90px;">Home.jsx</td>
<td>File</td>
<td>Landing page</td>
</tr>
<tr>
<td style="padding-left: 90px;">Login.jsx</td>
<td>File</td>
<td>Login page</td>
</tr>
<tr>
<td style="padding-left: 90px;">Signup.jsx</td>
<td>File</td>
<td>Registration page</td>
</tr>
<tr>
<td style="padding-left: 90px;">Dashboard.jsx</td>
<td>File</td>
<td>User dashboard</td>
</tr>
<tr>
<td style="padding-left: 90px;">Chatbot.jsx</td>
<td>File</td>
<td>Chatbot page</td>
</tr>
<tr>
<td style="padding-left: 90px;">CareerSuggester.jsx</td>
<td>File</td>
<td>Career assessment page</td>
</tr>
<tr>
<td style="padding-left: 90px;">CourseRecommender.jsx</td>
<td>File</td>
<td>Course search page</td>
</tr>
<tr>
<td style="padding-left: 90px;">Admin.jsx</td>
<td>File</td>
<td>Admin interface page</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>context/</strong></td>
<td>Folder</td>
<td>React context providers</td>
</tr>
<tr>
<td style="padding-left: 90px;">AuthContext.jsx</td>
<td>File</td>
<td>Authentication state management</td>
</tr>
<tr>
<td style="padding-left: 90px;">TestContext.jsx</td>
<td>File</td>
<td>Testing mode state management</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>services/</strong></td>
<td>Folder</td>
<td>API service layer</td>
</tr>
<tr>
<td style="padding-left: 90px;">api.js</td>
<td>File</td>
<td>API integration layer</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>hooks/</strong></td>
<td>Folder</td>
<td>Custom React hooks</td>
</tr>
<tr>
<td style="padding-left: 90px;">useAuth.js</td>
<td>File</td>
<td>Authentication hook</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>styles/</strong></td>
<td>Folder</td>
<td>Styling files</td>
</tr>
<tr>
<td style="padding-left: 90px;">globals.css</td>
<td>File</td>
<td>Global styles</td>
</tr>
<tr>
<td style="padding-left: 60px;"><strong>utils/</strong></td>
<td>Folder</td>
<td>Utility functions</td>
</tr>
<tr>
<td style="padding-left: 90px;">constants.js</td>
<td>File</td>
<td>Application constants</td>
</tr>
<tr>
<td style="padding-left: 30px;"><strong>public/</strong></td>
<td>Folder</td>
<td>Static assets</td>
</tr>
<tr>
<td style="padding-left: 60px;">R.png</td>
<td>File</td>
<td>Custom logo</td>
</tr>
<tr>
<td style="padding-left: 60px;">raslen_teacher.png</td>
<td>File</td>
<td>Auth page background</td>
</tr>
<tr>
<td style="padding-left: 60px;">vite.svg</td>
<td>File</td>
<td>Vite logo</td>
</tr>
<tr>
<td style="padding-left: 30px;">package.json</td>
<td>File</td>
<td>Project dependencies and scripts</td>
</tr>
<tr>
<td style="padding-left: 30px;">vite.config.js</td>
<td>File</td>
<td>Vite configuration</td>
</tr>
<tr>
<td style="padding-left: 30px;">index.html</td>
<td>File</td>
<td>HTML template</td>
</tr>
</tbody>
</table>

## ✨ Features

<table>
<thead>
<tr>
<th>Category</th>
<th>Feature</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="5"><strong>Core User Features</strong></td>
<td>🤖 AI Career Chatbot</td>
<td>Interactive chat interface with real-time AI responses</td>
</tr>
<tr>
<td>📋 Career Assessment</td>
<td>11-question guided assessment for personalized career paths</td>
</tr>
<tr>
<td>🔍 Course Recommender</td>
<td>Survey-based course recommendations with filtering options</td>
</tr>
<tr>
<td>💾 Chat History</td>
<td>Save and manage conversation history with ChatGPT-style sidebar</td>
</tr>
<tr>
<td>💼 Session Management</td>
<td>Save and revisit career assessment sessions</td>
</tr>
<tr>
<td rowspan="5"><strong>User Experience</strong></td>
<td>🎨 Modern UI/UX</td>
<td>Clean, responsive design with smooth animations</td>
</tr>
<tr>
<td>📱 Mobile Responsive</td>
<td>Optimized for all device sizes</td>
</tr>
<tr>
<td>🌍 Tunisia-Localized</td>
<td>Content tailored for Tunisian career market</td>
</tr>
<tr>
<td>🎭 Guided Tour</td>
<td>Interactive onboarding for new users</td>
</tr>
<tr>
<td>🔔 Toast Notifications</td>
<td>Real-time feedback for user actions</td>
</tr>
<tr>
<td rowspan="5"><strong>Admin Interface</strong></td>
<td>👥 User Management</td>
<td>Comprehensive user administration panel</td>
</tr>
<tr>
<td>📊 Platform Analytics</td>
<td>Dashboard with user statistics and insights</td>
</tr>
<tr>
<td>🛡️ Fraud Detection</td>
<td>Review and manage suspicious user accounts</td>
</tr>
<tr>
<td>📝 Audit Logs</td>
<td>View administrative action history</td>
</tr>
<tr>
<td>🔍 User Search</td>
<td>Advanced search and filtering capabilities</td>
</tr>
<tr>
<td rowspan="5"><strong>AI Testing Features</strong></td>
<td>🎛️ Test Mode Toggle</td>
<td>Enable/disable testing mode from header</td>
</tr>
<tr>
<td>⏺️ Recording Controls</td>
<td>Start/stop AI interaction recording</td>
</tr>
<tr>
<td>📊 Real-time Results</td>
<td>Live test results with performance metrics</td>
</tr>
<tr>
<td>📈 Visual Analytics</td>
<td>Charts and scores for AI performance</td>
</tr>
<tr>
<td>📄 Report Generation</td>
<td>Detailed test reports with recommendations</td>
</tr>
</tbody>
</table>

## 🚀 Setup Instructions

<table>
<thead>
<tr>
<th>Step</th>
<th>Command</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Navigate to Frontend</td>
<td><code>cd course-recommendation-main/Frontend</code></td>
<td>Enter frontend directory</td>
</tr>
<tr>
<td>2. Install Dependencies</td>
<td><code>npm install</code></td>
<td>Install all Node.js dependencies</td>
</tr>
<tr>
<td>3. Environment Setup</td>
<td>Create <code>.env</code> file (optional)</td>
<td>Configure environment settings</td>
</tr>
<tr>
<td>4. Start Development</td>
<td><code>npm run dev</code></td>
<td>Start Vite development server</td>
</tr>
<tr>
<td>5. Build for Production</td>
<td><code>npm run build</code></td>
<td>Create optimized production build</td>
</tr>
<tr>
<td>6. Preview Build</td>
<td><code>npm run preview</code></td>
<td>Preview production build locally</td>
</tr>
</tbody>
</table>

### Environment Variables (.env)
<table>
<thead>
<tr>
<th>Variable</th>
<th>Description</th>
<th>Default</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>VITE_API_BASE_URL</code></td>
<td>Backend API base URL</td>
<td><code>http://localhost:5000</code></td>
</tr>
</tbody>
</table>

## 📦 Dependencies

<table>
<thead>
<tr>
<th>Package</th>
<th>Version</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>react</code></td>
<td>^18.2.0</td>
<td>Frontend framework</td>
</tr>
<tr>
<td><code>react-dom</code></td>
<td>^18.2.0</td>
<td>React DOM rendering</td>
</tr>
<tr>
<td><code>react-router-dom</code></td>
<td>^6.x</td>
<td>Client-side routing</td>
</tr>
<tr>
<td><code>react-icons</code></td>
<td>^4.x</td>
<td>Comprehensive icon library</td>
</tr>
<tr>
<td><code>react-toastify</code></td>
<td>^9.x</td>
<td>Toast notifications</td>
</tr>
<tr>
<td><code>vite</code></td>
<td>^4.x</td>
<td>Build tool and dev server</td>
</tr>
</tbody>
</table>

## 🎯 Component Overview

<table>
<thead>
<tr>
<th>Component</th>
<th>Location</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Pages</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;">Home</td>
<td><code>src/pages/Home.jsx</code></td>
<td>Landing page with feature overview</td>
</tr>
<tr>
<td style="padding-left: 30px;">Login/Signup</td>
<td><code>src/pages/Login.jsx</code><br><code>src/pages/Signup.jsx</code></td>
<td>Authentication pages</td>
</tr>
<tr>
<td style="padding-left: 30px;">Dashboard</td>
<td><code>src/pages/Dashboard.jsx</code></td>
<td>User dashboard with quick access</td>
</tr>
<tr>
<td style="padding-left: 30px;">Chatbot</td>
<td><code>src/pages/Chatbot.jsx</code></td>
<td>AI career advisor interface</td>
</tr>
<tr>
<td style="padding-left: 30px;">CareerSuggester</td>
<td><code>src/pages/CareerSuggester.jsx</code></td>
<td>Career assessment wizard</td>
</tr>
<tr>
<td style="padding-left: 30px;">CourseRecommender</td>
<td><code>src/pages/CourseRecommender.jsx</code></td>
<td>Course search and recommendations</td>
</tr>
<tr>
<td style="padding-left: 30px;">Admin</td>
<td><code>src/pages/Admin.jsx</code></td>
<td>Administrative interface</td>
</tr>
<tr>
<td><strong>Key Components</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;">ChatWindow</td>
<td><code>src/components/chatbot/ChatWindow.jsx</code></td>
<td>Main chat interface with message history</td>
</tr>
<tr>
<td style="padding-left: 30px;">ChatSidebar</td>
<td><code>src/components/chatbot/ChatSidebar.jsx</code></td>
<td>Conversation history management</td>
</tr>
<tr>
<td style="padding-left: 30px;">TestStatusIndicator</td>
<td><code>src/components/common/TestStatusIndicator.jsx</code></td>
<td>Visual test recording status</td>
</tr>
<tr>
<td style="padding-left: 30px;">TestResultsModal</td>
<td><code>src/components/common/TestResultsModal.jsx</code></td>
<td>Detailed test analysis</td>
</tr>
<tr>
<td style="padding-left: 30px;">AdminDashboard</td>
<td><code>src/components/admin/AdminDashboard.jsx</code></td>
<td>Admin statistics and overview</td>
</tr>
<tr>
<td style="padding-left: 30px;">UserManagement</td>
<td><code>src/components/admin/UserManagement.jsx</code></td>
<td>User administration panel</td>
</tr>
<tr>
<td style="padding-left: 30px;">FraudDetection</td>
<td><code>src/components/admin/FraudDetection.jsx</code></td>
<td>Suspicious account review</td>
</tr>
<tr>
<td><strong>Context Providers</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;">AuthContext</td>
<td><code>src/context/AuthContext.jsx</code></td>
<td>Manages user authentication state</td>
</tr>
<tr>
<td style="padding-left: 30px;">TestContext</td>
<td><code>src/context/TestContext.jsx</code></td>
<td>Handles AI testing mode and recording</td>
</tr>
</tbody>
</table>

## 🔌 API Integration

<table>
<thead>
<tr>
<th>Service Method</th>
<th>Endpoint</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Authentication</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>login(credentials)</code></td>
<td><code>POST /api/auth/login</code></td>
<td>User authentication</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>signup(userData)</code></td>
<td><code>POST /api/auth/signup</code></td>
<td>User registration</td>
</tr>
<tr>
<td><strong>Chatbot</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>sendMessage(messageData)</code></td>
<td><code>POST /api/chatbot/message</code></td>
<td>Send chat message to AI</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>getConversations()</code></td>
<td><code>GET /api/chatbot/conversations</code></td>
<td>Retrieve user's chat history</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>saveConversation(conversationData)</code></td>
<td><code>POST /api/chatbot/save-conversation</code></td>
<td>Save chat conversation</td>
</tr>
<tr>
<td><strong>Career Suggester</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>startAssessment()</code></td>
<td><code>GET /api/suggester/start</code></td>
<td>Start new career assessment</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>submitAnswer(answerData)</code></td>
<td><code>POST /api/suggester/answer</code></td>
<td>Submit assessment answer</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>getSessions()</code></td>
<td><code>GET /api/suggester/sessions</code></td>
<td>Retrieve saved sessions</td>
</tr>
<tr>
<td><strong>Admin</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>getUsers(params)</code></td>
<td><code>GET /api/admin/users</code></td>
<td>Retrieve user list with filtering</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>updateUser(userId, data)</code></td>
<td><code>PUT /api/admin/users/{userId}</code></td>
<td>Update user information</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>getFraudQueue()</code></td>
<td><code>GET /api/admin/fraud/queue</code></td>
<td>Retrieve suspicious accounts</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>reviewUser(reviewData)</code></td>
<td><code>POST /api/admin/fraud/review</code></td>
<td>Review and take action on user</td>
</tr>
<tr>
<td><strong>Testing</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>startRecording()</code></td>
<td><code>POST /api/tests/start-recording</code></td>
<td>Start AI test recording session</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>stopRecording(sessionId)</code></td>
<td><code>POST /api/tests/stop-recording</code></td>
<td>Stop recording and generate report</td>
</tr>
<tr>
<td style="padding-left: 30px;"><code>logInteraction(interactionData)</code></td>
<td><code>POST /api/tests/log-interaction</code></td>
<td>Log AI interaction for testing</td>
</tr>
</tbody>
</table>

## 🧪 AI Testing Interface

<table>
<thead>
<tr>
<th>Step</th>
<th>Action</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Toggle "Test Mode" in header</td>
<td>Enable testing features (admin users only)</td>
</tr>
<tr>
<td>2</td>
<td>Click "Start Recording" button</td>
<td>Begin capturing AI interactions</td>
</tr>
<tr>
<td>3</td>
<td>Use AI Features normally</td>
<td>Interactions with chatbot, career suggester, or course recommender are recorded</td>
</tr>
<tr>
<td>4</td>
<td>Click "Stop Recording"</td>
<td>Generate comprehensive test report</td>
</tr>
<tr>
<td>5</td>
<td>View Results in Modal</td>
<td>Detailed analysis with scores and recommendations</td>
</tr>
</tbody>
</table>

### Test Results Display
<table>
<thead>
<tr>
<th>Metric</th>
<th>Description</th>
<th>Format</th>
</tr>
</thead>
<tbody>
<tr>
<td>Overall Score</td>
<td>Composite AI performance rating</td>
<td>0-100 scale</td>
</tr>
<tr>
<td>Component Breakdown</td>
<td>Individual AI system performance</td>
<td>Percentage scores</td>
</tr>
<tr>
<td>Response Times</td>
<td>Performance timing metrics</td>
<td>Milliseconds</td>
</tr>
<tr>
<td>Quality Assessment</td>
<td>Issue identification and analysis</td>
<td>Descriptive feedback</td>
</tr>
<tr>
<td>Recommendations</td>
<td>Improvement suggestions</td>
<td>Actionable items</td>
</tr>
</tbody>
</table>

## 🛡️ Admin Interface Features

<table>
<thead>
<tr>
<th>Feature</th>
<th>Component</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>User Management</strong></td>
<td><code>UserManagement.jsx</code></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;">User List</td>
<td>Data table</td>
<td>Paginated user listing with search</td>
</tr>
<tr>
<td style="padding-left: 30px;">User Details</td>
<td>Detail view</td>
<td>Comprehensive user information display</td>
</tr>
<tr>
<td style="padding-left: 30px;">Role Management</td>
<td>Toggle controls</td>
<td>Admin/student role assignment</td>
</tr>
<tr>
<td style="padding-left: 30px;">Email Verification</td>
<td>Action buttons</td>
<td>Manual verification capability</td>
</tr>
<tr>
<td style="padding-left: 30px;">Account Actions</td>
<td>Action menu</td>
<td>Update and delete operations</td>
</tr>
<tr>
<td><strong>Fraud Detection</strong></td>
<td><code>FraudDetection.jsx</code></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;">Risk Scoring</td>
<td>Visual indicators</td>
<td>Color-coded risk levels (0.0-1.0)</td>
</tr>
<tr>
<td style="padding-left: 30px;">Review Queue</td>
<td>Priority list</td>
<td>Prioritized suspicious accounts</td>
</tr>
<tr>
<td style="padding-left: 30px;">Action System</td>
<td>Button group</td>
<td>Verify, block, or clear flags</td>
</tr>
<tr>
<td style="padding-left: 30px;">Fraud Statistics</td>
<td>Dashboard cards</td>
<td>Platform security insights</td>
</tr>
<tr>
<td><strong>Platform Analytics</strong></td>
<td><code>AdminDashboard.jsx</code></td>
<td></td>
</tr>
<tr>
<td style="padding-left: 30px;">User Statistics</td>
<td>Metrics cards</td>
<td>Total users, verification rates</td>
</tr>
<tr>
<td style="padding-left: 30px;">Growth Metrics</td>
<td>Charts</td>
<td>Platform adoption trends</td>
</tr>
<tr>
<td style="padding-left: 30px;">Role Distribution</td>
<td>Pie chart</td>
<td>Admin vs student breakdown</td>
</tr>
<tr>
<td style="padding-left: 30px;">Activity Monitoring</td>
<td>Activity feed</td>
<td>User engagement metrics</td>
</tr>
</tbody>
</table>

## 📱 Responsive Design

<table>
<thead>
<tr>
<th>Breakpoint</th>
<th>Device Type</th>
<th>Features</th>
</tr>
</thead>
<tbody>
<tr>
<td>< 768px</td>
<td>Mobile</td>
<td>Touch-friendly interface, optimized navigation, collapsible menus</td>
</tr>
<tr>
<td>768px - 1024px</td>
<td>Tablet</td>
<td>Adaptive layouts, medium-sized components, optimized tables</td>
</tr>
<tr>
<td>> 1024px</td>
<td>Desktop</td>
<td>Full feature set, multi-column layouts, advanced interactions</td>
</tr>
</tbody>
</table>

### Mobile-First Features
<table>
<thead>
<tr>
<th>Feature</th>
<th>Mobile Implementation</th>
<th>Benefit</th>
</tr>
</thead>
<tbody>
<tr>
<td>Touch Interface</td>
<td>Larger touch targets, swipe gestures</td>
<td>Easy mobile navigation</td>
</tr>
<tr>
<td>Navigation</td>
<td>Hamburger menu, bottom navigation</td>
<td>Space-efficient mobile layout</td>
</tr>
<tr>
<td>Data Tables</td>
<td>Horizontal scroll, card-based layouts</td>
<td>Readable data on small screens</td>
</tr>
<tr>
<td>Component Layouts</td>
<td>Stacked columns, collapsible sections</td>
<td>Optimal use of screen space</td>
</tr>
</tbody>
</table>

## 🌍 Tunisia Localization

<table>
<thead>
<tr>
<th>Feature</th>
<th>Localization</th>
<th>User Benefit</th>
</tr>
</thead>
<tbody>
<tr>
<td>Career Paths</td>
<td>Tunisia-specific job market data</td>
<td>Relevant local career opportunities</td>
</tr>
<tr>
<td>Educational Recommendations</td>
<td>Local universities and training centers</td>
<td>Accessible education options in Tunisia</td>
</tr>
<tr>
<td>Industry Focus</td>
<td>Tunisia economic sectors and growth areas</td>
<td>Regional industry alignment</td>
</tr>
<tr>
<td>Salary Information</td>
<td>Local market rates and expectations</td>
<td>Realistic career expectation setting</td>
</tr>
<tr>
<td>Certification Guidance</td>
<td>Local certification bodies and requirements</td>
<td>Recognized qualifications in Tunisia</td>
</tr>
<tr>
<td>Cultural Context</td>
<td>Tunisia-specific examples and scenarios</td>
<td>Relatable career advice</td>
</tr>
</tbody>
</table>

## 🚀 Deployment

<table>
<thead>
<tr>
<th>Platform</th>
<th>Build Command</th>
<th>Output Directory</th>
</tr>
</thead>
<tbody>
<tr>
<td>Vercel</td>
<td><code>npm run build</code></td>
<td><code>dist/</code></td>
</tr>
<tr>
<td>Netlify</td>
<td><code>npm run build</code></td>
<td><code>dist/</code></td>
</tr>
<tr>
<td>Traditional Hosting</td>
<td><code>npm run build</code></td>
<td><code>dist/</code></td>
</tr>
</tbody>
</table>

### Deployment Steps
<table>
<thead>
<tr>
<th>Step</th>
<th>Action</th>
<th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Run build command</td>
<td><code>npm run build</code></td>
</tr>
<tr>
<td>2</td>
<td>Upload build output</td>
<td>Upload <code>dist/</code> contents to web server</td>
</tr>
<tr>
<td>3</td>
<td>Configure redirects</td>
<td>Set up client-side routing support</td>
</tr>
<tr>
<td>4</td>
<td>Verify API connectivity</td>
<td>Ensure backend API is accessible</td>
</tr>
</tbody>
</table>

## 🔧 Development Scripts

<table>
<thead>
<tr>
<th>Script</th>
<th>Command</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td>Development Server</td>
<td><code>npm run dev</code></td>
<td>Start Vite development server with hot reload</td>
</tr>
<tr>
<td>Production Build</td>
<td><code>npm run build</code></td>
<td>Create optimized production build</td>
</tr>
<tr>
<td>Preview Build</td>
<td><code>npm run preview</code></td>
<td>Preview production build locally</td>
</tr>
<tr>
<td>Linting</td>
<td><code>npm run lint</code></td>
<td>Run ESLint for code quality</td>
</tr>
</tbody>
</table>

## 🎨 Design System

<table>
<thead>
<tr>
<th>Element</th>
<th>Implementation</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td>Global Styles</td>
<td><code>src/styles/globals.css</code></td>
<td>Base styling and CSS custom properties</td>
</tr>
<tr>
<td>Component Styles</td>
<td>CSS Modules</td>
<td>Component-specific styling</td>
</tr>
<tr>
<td>Layout System</td>
<td>CSS Grid & Flexbox</td>
<td>Responsive layout foundation</td>
</tr>
<tr>
<td>Color Palette</td>
<td>CSS Custom Properties</td>
<td>Consistent theming across application</td>
</tr>
<tr>
<td>Typography Scale</td>
<td>Modular scale system</td>
<td>Consistent text hierarchy</td>
</tr>
<tr>
<td>Spacing System</td>
<td>Consistent spacing units</td>
<td>Visual rhythm and alignment</td>
</tr>
</tbody>
</table>

---

**Built with ❤️ for the Tunisian tech community**
