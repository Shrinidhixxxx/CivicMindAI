# Create the SLM (Small Language Model) module
slm_module_code = '''"""
SLM (Small Language Model Interface) Module for CivicMindAI
Handles general chit-chat and fallback responses using OpenAI API or local models.
"""

import os
from typing import Dict, Any, Optional
import logging
from datetime import datetime
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class SLMModule:
    """
    Small Language Model interface that handles general conversation,
    chitchat, and fallback responses when other modules can't answer.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the SLM module.
        
        Args:
            api_key (str, optional): OpenAI API key (can be set via env variable)
            model (str): Model name to use (default: gpt-3.5-turbo)
        """
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        # Setup OpenAI client if available
        if OPENAI_AVAILABLE and self.api_key:
            try:
                openai.api_key = self.api_key
                self.client_available = True
            except Exception as e:
                self.client_available = False
                print(f"Warning: OpenAI client setup failed: {e}")
        else:
            self.client_available = False
            if not OPENAI_AVAILABLE:
                print("Warning: OpenAI package not installed. Using fallback responses.")
            else:
                print("Warning: No OpenAI API key provided. Using fallback responses.")
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Fallback responses for when API is not available
        self.fallback_responses = self._initialize_fallback_responses()
    
    def _initialize_fallback_responses(self) -> Dict[str, str]:
        """Initialize predefined fallback responses for common queries."""
        return {
            'greeting': "Hello! I'm CivicMindAI, your Chennai civic assistant. I can help you with civic services, government procedures, emergency contacts, and more. What can I assist you with today?",
            
            'who_are_you': "I'm CivicMindAI, an AI-powered civic assistant specifically designed to help Chennai residents with civic issues. I use advanced AI technologies like RAG, KAG, and CAG to provide accurate and up-to-date information about municipal services, government procedures, and civic amenities.",
            
            'capabilities': "I can help you with:\\n• Emergency contact numbers\\n• Civic service procedures (water, tax, certificates)\\n• Government office information\\n• Municipal service complaints\\n• Zone-specific contacts\\n• Latest civic updates and guidelines",
            
            'thanks': "You're welcome! I'm here to help Chennai residents with civic issues anytime. Feel free to ask if you have more questions about municipal services, government procedures, or civic amenities.",
            
            'goodbye': "Goodbye! Thank you for using CivicMindAI. Remember, I'm always here to help with your Chennai civic needs. Have a great day!",
            
            'help': "I'm your Chennai civic assistant! You can ask me about:\\n• Emergency numbers (fire, police, ambulance)\\n• Water supply issues and CMWSSB services\\n• Property tax payment procedures\\n• Garbage collection schedules\\n• Birth/death certificate applications\\n• Municipal office contacts\\n• And much more civic information!",
            
            'how_it_works': "I use four advanced AI technologies:\\n🔍 **RAG**: Searches official documents and web sources\\n🧠 **KAG**: Uses knowledge graphs for step-by-step procedures\\n⚡ **CAG**: Provides instant answers from cached information\\n🤖 **SLM**: Handles general conversation (that's me!)\\n\\nI automatically choose the best method based on your question type.",
            
            'about_chennai': "Chennai, the capital of Tamil Nadu, is served by several civic bodies:\\n• Greater Chennai Corporation (GCC) - Municipal services\\n• CMWSSB - Water supply and sewerage\\n• TANGEDCO - Electricity\\n• Tamil Nadu Police - Law and order\\n\\nI can help you interact with all these services efficiently!",
            
            'feedback': "I appreciate your feedback! While I can't store it permanently, your input helps me understand how to better assist Chennai residents. If you have specific suggestions about civic services, I recommend contacting the relevant departments directly using the contact numbers I can provide.",
            
            'default': "I understand you're asking about something civic-related, but I need more specific information to help you properly. Could you please ask about:\\n• A specific civic service (water, tax, certificates)\\n• An emergency contact number\\n• A government procedure\\n• A municipal office contact\\n\\nWhat exactly can I help you with today?"
        }
    
    def classify_query_type(self, query: str) -> str:
        """
        Classify the type of query to provide appropriate fallback response.
        
        Args:
            query (str): User query
            
        Returns:
            str: Query type classification
        """
        query_lower = query.lower()
        
        # Greeting patterns
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return 'greeting'
        
        # Identity questions
        if any(phrase in query_lower for phrase in ['who are you', 'what are you', 'tell me about yourself', 'introduce yourself']):
            return 'who_are_you'
        
        # Capability questions
        if any(phrase in query_lower for phrase in ['what can you do', 'your capabilities', 'what do you help with', 'services']):
            return 'capabilities'
        
        # Thank you messages
        if any(word in query_lower for word in ['thank', 'thanks', 'appreciate']):
            return 'thanks'
        
        # Goodbye messages
        if any(word in query_lower for word in ['bye', 'goodbye', 'see you', 'exit', 'quit']):
            return 'goodbye'
        
        # Help requests
        if any(word in query_lower for word in ['help', 'assist', 'support', 'guide']):
            return 'help'
        
        # How it works
        if any(phrase in query_lower for phrase in ['how do you work', 'how does this work', 'explain your system']):
            return 'how_it_works'
        
        # About Chennai
        if any(phrase in query_lower for phrase in ['about chennai', 'chennai city', 'tell me about chennai']):
            return 'about_chennai'
        
        # Feedback
        if any(word in query_lower for word in ['feedback', 'suggestion', 'improve', 'better']):
            return 'feedback'
        
        return 'default'
    
    def generate_openai_response(self, query: str) -> Optional[str]:
        """
        Generate response using OpenAI API.
        
        Args:
            query (str): User query
            
        Returns:
            str: Generated response or None if failed
        """
        if not self.client_available:
            return None
        
        try:
            # System prompt for CivicMindAI context
            system_prompt = """You are CivicMindAI, a helpful civic assistant for Chennai residents. 
            You specialize in Chennai civic services, municipal procedures, and government information.
            Keep responses friendly, informative, and focused on civic matters.
            If asked about specific civic procedures or contacts, suggest the user ask for those specifically
            so you can provide accurate information from your specialized modules."""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return None
    
    def get_response(self, query: str) -> Dict[str, Any]:
        """
        Get SLM response for general queries and chitchat.
        
        Args:
            query (str): User query
            
        Returns:
            Dict containing response data
        """
        try:
            # Try OpenAI API first if available
            if self.client_available:
                openai_response = self.generate_openai_response(query)
                if openai_response:
                    return {
                        'success': True,
                        'data': {
                            'response': openai_response,
                            'method': 'OpenAI API',
                            'model': self.model
                        },
                        'source': 'SLM',
                        'query': query,
                        'timestamp': datetime.now().isoformat(),
                        'message': f'Response generated using {self.model}'
                    }
            
            # Fallback to predefined responses
            query_type = self.classify_query_type(query)
            fallback_response = self.fallback_responses.get(query_type, self.fallback_responses['default'])
            
            return {
                'success': True,
                'data': {
                    'response': fallback_response,
                    'method': 'Fallback Response',
                    'query_type': query_type
                },
                'source': 'SLM',
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'message': f'Fallback response for query type: {query_type}'
            }
            
        except Exception as e:
            self.logger.error(f"Error in SLM response: {str(e)}")
            return {
                'success': False,
                'data': None,
                'source': 'SLM',
                'error': str(e)
            }
    
    def format_response(self, response_data: Dict[str, Any]) -> str:
        """
        Format the SLM response into user-friendly text.
        
        Args:
            response_data (Dict): Response data from get_response()
            
        Returns:
            str: Formatted response text
        """
        if not response_data['success']:
            return "I apologize, but I'm having trouble processing your request right now. Please try asking about specific civic services, and I'll do my best to help!"
        
        data = response_data['data']
        response_text = data['response']
        
        # Add method indicator
        if data['method'] == 'OpenAI API':
            footer = f"\\n\\n💬 *Response generated via {data['model']} at {datetime.now().strftime('%H:%M:%S')}*"
        else:
            footer = f"\\n\\n🤖 *Predefined response for {data['query_type']} query*"
        
        return response_text + footer

# Example usage and testing
if __name__ == "__main__":
    # Initialize SLM module
    slm = SLMModule()
    
    # Test queries
    test_queries = [
        "Hello, who are you?",
        "What can you help me with?",
        "How do you work?",
        "Tell me about Chennai",
        "Thank you for your help",
        "This is a random question about something unrelated"
    ]
    
    print("💬 Testing SLM Module\\n" + "="*50)
    
    for query in test_queries:
        print(f"\\n**Query:** {query}")
        response = slm.get_response(query)
        formatted = slm.format_response(response)
        print(f"**Response:** {formatted}")
        print("-" * 50)
'''

with open('CivicMindAI/slm_module.py', 'w') as f:
    f.write(slm_module_code)

print("✅ SLM (Small Language Model Interface) module created!")
print("Features implemented:")
print("  • OpenAI API integration with fallback")
print("  • Query type classification")
print("  • Predefined fallback responses")
print("  • Conversational context awareness")
print("  • Chennai civic-focused responses")
print("  • Error handling and logging")
print("  • Response formatting with method indicators")