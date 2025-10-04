# Create the main Streamlit application
main_app_code = '''"""
CivicMindAI - Main Streamlit Application
Chennai Civic Assistant Chatbot with Multi-Modal AI Integration
"""

import streamlit as st
import time
from datetime import datetime
import json
import os
from typing import Dict, Any, List

# Import the agent controller
try:
    from agent_controller import AgentController
    CONTROLLER_AVAILABLE = True
except ImportError as e:
    CONTROLLER_AVAILABLE = False
    print(f"Warning: Could not import AgentController: {e}")

# Configure Streamlit page
st.set_page_config(
    page_title="CivicMindAI - Chennai Civic Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2980b9;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #1976d2;
        margin-left: 2rem;
    }
    
    .bot-message {
        background-color: #f8f9fa;
        border-left-color: #2980b9;
        margin-right: 2rem;
    }
    
    .module-tag {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .tag-rag { background-color: #e8f5e8; color: #2e7d32; }
    .tag-kag { background-color: #fff3e0; color: #f57c00; }
    .tag-cag { background-color: #f3e5f5; color: #7b1fa2; }
    .tag-slm { background-color: #e1f5fe; color: #0277bd; }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #4caf50;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 3px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #2980b9;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    .feedback-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2980b9;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CivicMindAIApp:
    """Main Streamlit application class for CivicMindAI."""
    
    def __init__(self):
        """Initialize the application."""
        self.initialize_session_state()
        
        # Initialize controller if available
        if CONTROLLER_AVAILABLE:
            if 'controller' not in st.session_state:
                with st.spinner("🤖 Initializing CivicMindAI..."):
                    try:
                        st.session_state.controller = AgentController()
                        st.session_state.controller_status = "Ready"
                    except Exception as e:
                        st.session_state.controller = None
                        st.session_state.controller_status = f"Error: {str(e)}"
        else:
            st.session_state.controller = None
            st.session_state.controller_status = "Controller not available"
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'query_count' not in st.session_state:
            st.session_state.query_count = 0
        
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.now()
        
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = []
    
    def render_header(self):
        """Render the application header."""
        st.markdown("""
        <div class="main-header">
            <h1>🏛️ CivicMindAI</h1>
            <h3>Your AI Civic Assistant for Chennai</h3>
            <p>Powered by RAG • KAG • CAG • SLM Technologies</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with system information and controls."""
        with st.sidebar:
            st.header("🤖 System Status")
            
            # Controller Status
            if st.session_state.controller:
                st.success("✅ CivicMindAI Ready")
                status = st.session_state.controller.get_module_status()
                
                st.subheader("AI Modules")
                for module, info in status['modules'].items():
                    icon = "✅" if info['available'] else "❌"
                    st.write(f"{icon} **{module}**: {info['description']}")
                
                st.metric("Available Modules", f"{status['total_available']}/4")
            else:
                st.error("❌ Controller Unavailable")
                st.write(st.session_state.controller_status)
            
            # Session Statistics
            st.subheader("📊 Session Stats")
            st.metric("Queries Processed", st.session_state.query_count)
            st.metric("Messages", len(st.session_state.messages))
            
            session_duration = datetime.now() - st.session_state.session_start
            st.metric("Session Duration", f"{session_duration.seconds // 60}m {session_duration.seconds % 60}s")
            
            # Controls
            st.subheader("🛠️ Controls")
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.session_state.query_count = 0
                st.rerun()
            
            if st.button("🔄 Reset Session", type="secondary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            # Help Section
            st.subheader("💡 Quick Help")
            st.info("""
            **Try asking about:**
            • Emergency contacts
            • Water supply issues  
            • Property tax procedures
            • Garbage collection
            • Birth/death certificates
            • Municipal office contacts
            """)
            
            # About Section
            with st.expander("ℹ️ About CivicMindAI"):
                st.write("""
                CivicMindAI is an advanced AI assistant designed specifically for Chennai residents.
                
                **Technologies Used:**
                - **RAG**: Retrieval-Augmented Generation for latest information
                - **KAG**: Knowledge-Augmented Generation for procedures
                - **CAG**: Cache-Augmented Generation for instant responses
                - **SLM**: Small Language Model for conversation
                
                **Data Sources:**
                - Chennai Corporation documents
                - CMWSSB guidelines
                - Government portals
                - Real-time web updates
                """)
    
    def get_module_tag_html(self, module: str) -> str:
        """Generate HTML for module tag."""
        tag_classes = {
            'RAG': 'tag-rag',
            'KAG': 'tag-kag', 
            'CAG': 'tag-cag',
            'SLM': 'tag-slm'
        }
        
        tag_class = tag_classes.get(module, 'tag-slm')
        return f'<span class="module-tag {tag_class}">{module}</span>'
    
    def render_message(self, message: Dict[str, Any], is_user: bool = False):
        """Render a chat message."""
        if is_user:
            with st.container():
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.container():
                # Module tag
                module_tag = ""
                if 'module' in message:
                    module_tag = self.get_module_tag_html(message['module'])
                
                # Response time
                response_time = ""
                if 'response_time' in message:
                    response_time = f"<small style='color: #666;'>⏱️ {message['response_time']}ms</small>"
                
                st.markdown(f"""
                <div class="chat-message bot-message">
                    {module_tag}
                    <strong>CivicMindAI:</strong><br>
                    {message['content']}
                    <br><br>
                    {response_time}
                </div>
                """, unsafe_allow_html=True)
                
                # Feedback buttons (simplified for demo)
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("👍", key=f"like_{len(st.session_state.messages)}_{message.get('timestamp', 0)}"):
                        st.session_state.feedback_data.append({
                            'message_id': len(st.session_state.messages),
                            'feedback': 'positive',
                            'timestamp': datetime.now().isoformat()
                        })
                        st.success("Thank you for your feedback!")
                
                with col2:
                    if st.button("👎", key=f"dislike_{len(st.session_state.messages)}_{message.get('timestamp', 0)}"):
                        st.session_state.feedback_data.append({
                            'message_id': len(st.session_state.messages),
                            'feedback': 'negative', 
                            'timestamp': datetime.now().isoformat()
                        })
                        st.info("Thank you for your feedback!")
    
    def show_typing_indicator(self):
        """Show typing indicator while processing."""
        st.markdown("""
        <div class="typing-indicator">
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            <span>CivicMindAI is analyzing your query...</span>
        </div>
        """, unsafe_allow_html=True)
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process user query and return response."""
        if not st.session_state.controller:
            return {
                'content': "I apologize, but the AI system is currently unavailable. Please try again later.",
                'module': 'ERROR',
                'timestamp': datetime.now().isoformat(),
                'response_time': 0
            }
        
        try:
            start_time = time.time()
            
            # Route query through controller
            controller_response = st.session_state.controller.route_query(query)
            
            end_time = time.time()
            response_time = int((end_time - start_time) * 1000)  # Convert to milliseconds
            
            return {
                'content': controller_response['response_text'],
                'module': controller_response['selected_module'],
                'timestamp': controller_response['timestamp'],
                'response_time': response_time,
                'routing_info': controller_response.get('routing_analysis', {}),
                'success': controller_response['success']
            }
            
        except Exception as e:
            return {
                'content': f"I encountered an error processing your request: {str(e)}",
                'module': 'ERROR',
                'timestamp': datetime.now().isoformat(),
                'response_time': 0
            }
    
    def run(self):
        """Run the main application."""
        self.render_header()
        self.render_sidebar()
        
        # Main chat interface
        st.header("💬 Chat Interface")
        
        # Display chat messages
        for message in st.session_state.messages:
            if message['role'] == 'user':
                self.render_message(message, is_user=True)
            else:
                self.render_message(message, is_user=False)
        
        # Chat input
        with st.container():
            query = st.chat_input("Ask me about Chennai civic services...")
            
            if query:
                # Add user message
                user_message = {
                    'role': 'user',
                    'content': query,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.messages.append(user_message)
                
                # Show typing indicator
                typing_placeholder = st.empty()
                with typing_placeholder:
                    self.show_typing_indicator()
                
                # Process query
                response = self.process_query(query)
                
                # Remove typing indicator
                typing_placeholder.empty()
                
                # Add bot response
                bot_message = {
                    'role': 'assistant',
                    'content': response['content'],
                    'module': response['module'],
                    'timestamp': response['timestamp'],
                    'response_time': response.get('response_time', 0)
                }
                st.session_state.messages.append(bot_message)
                
                # Update query count
                st.session_state.query_count += 1
                
                # Rerun to update the display
                st.rerun()
        
        # Welcome message for new users
        if len(st.session_state.messages) == 0:
            st.info("""
            👋 **Welcome to CivicMindAI!**
            
            I'm your Chennai civic assistant powered by advanced AI technologies. I can help you with:
            
            • 🚨 Emergency contact numbers
            • 💧 Water supply and CMWSSB services  
            • 💰 Property tax procedures and payments
            • 🗑️ Garbage collection schedules
            • 📄 Birth/death certificates
            • 🏛️ Municipal office information
            • And much more!
            
            **Try asking:** "Fire emergency number" or "How to pay property tax online?"
            """)

# Application entry point
def main():
    """Main application entry point."""
    try:
        app = CivicMindAIApp()
        app.run()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.info("Please refresh the page or contact support.")

if __name__ == "__main__":
    main()
'''

with open('CivicMindAI/main.py', 'w') as f:
    f.write(main_app_code)

print("✅ Main Streamlit application created!")
print("\nApplication features:")
print("  • Beautiful chat interface with message bubbles")
print("  • Real-time module routing indicators")
print("  • Session statistics and system status")
print("  • Typing indicators and response time tracking")
print("  • Feedback system for user ratings")
print("  • Responsive design with custom CSS")
print("  • Comprehensive error handling")
print("  • Welcome message and help system")
print("  • Chat history management")
print("  • Module status monitoring")