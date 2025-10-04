# Create the Agent Controller module
agent_controller_code = '''"""
Agent Controller for CivicMindAI
Intelligent routing agent that decides which AI module (RAG/KAG/CAG/SLM) to use based on query analysis.
"""

import re
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Import all AI modules
from rag_module import RAGModule
from kag_module import KAGModule
from cag_module import CAGModule
from slm_module import SLMModule

class AgentController:
    """
    Central controller that analyzes user queries and routes them to the most appropriate
    AI module (RAG, KAG, CAG, or SLM) for optimal response generation.
    """
    
    def __init__(self):
        """Initialize the agent controller with all AI modules."""
        # Initialize all AI modules
        try:
            self.rag_module = RAGModule()
            self.rag_available = True
        except Exception as e:
            print(f"Warning: RAG module initialization failed: {e}")
            self.rag_available = False
        
        try:
            self.kag_module = KAGModule()
            self.kag_available = True
        except Exception as e:
            print(f"Warning: KAG module initialization failed: {e}")
            self.kag_available = False
        
        try:
            self.cag_module = CAGModule()
            self.cag_available = True
        except Exception as e:
            print(f"Warning: CAG module initialization failed: {e}")
            self.cag_available = False
        
        try:
            self.slm_module = SLMModule()
            self.slm_available = True
        except Exception as e:
            print(f"Warning: SLM module initialization failed: {e}")
            self.slm_available = False
        
        # Query routing patterns
        self.routing_patterns = self._initialize_routing_patterns()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        print("🤖 CivicMindAI Agent Controller initialized successfully!")
        print(f"Available modules: RAG({self.rag_available}), KAG({self.kag_available}), CAG({self.cag_available}), SLM({self.slm_available})")
    
    def _initialize_routing_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize patterns for routing queries to appropriate modules."""
        return {
            'CAG': {
                'keywords': [
                    'helpline', 'contact', 'number', 'phone', 'emergency', 
                    'fire', 'police', 'ambulance', 'hospital',
                    'office hours', 'timing', 'schedule', 'website',
                    'zone contact', 'collector office', 'mayor office'
                ],
                'patterns': [
                    r'\\b(helpline|contact|number|phone)\\b',
                    r'\\b(emergency|fire|police|ambulance)\\b',
                    r'\\b(office hours|timing|schedule)\\b',
                    r'\\b(zone|area)\\s+(contact|number)\\b'
                ],
                'description': 'Static information, contacts, helplines'
            },
            
            'RAG': {
                'keywords': [
                    'latest', 'recent', 'update', 'current', 'new', 'report',
                    'schedule', 'timings', 'rules', 'guidelines', 'notification',
                    '2025', 'october', 'september', 'today'
                ],
                'patterns': [
                    r'\\b(latest|recent|update|current|new)\\b',
                    r'\\b(rules|guidelines|notification)\\s+(2025|2024)\\b',
                    r'\\b(schedule|timing)\\s+(for|of)\\b',
                    r'\\b(what is|show me)\\s+.*(schedule|timing|rule)\\b'
                ],
                'description': 'Recent updates, schedules, document-based info'
            },
            
            'KAG': {
                'keywords': [
                    'how to', 'procedure', 'steps', 'process', 'apply',
                    'get', 'obtain', 'registration', 'application',
                    'who handles', 'responsible', 'department',
                    'repair', 'complaint', 'issue'
                ],
                'patterns': [
                    r'\\b(how to|procedure|steps|process)\\b',
                    r'\\b(apply|get|obtain)\\s+(for|a|an)\\b',
                    r'\\b(who handles|responsible|department)\\b',
                    r'\\b(repair|complaint|issue)\\s+(in|at|for)\\b'
                ],
                'description': 'Procedures, step-by-step guidance, multi-hop reasoning'
            },
            
            'SLM': {
                'keywords': [
                    'hello', 'hi', 'hey', 'who are you', 'what are you',
                    'thank', 'thanks', 'bye', 'goodbye', 'help',
                    'chat', 'talk', 'conversation'
                ],
                'patterns': [
                    r'\\b(hello|hi|hey|good\\s+(morning|afternoon|evening))\\b',
                    r'\\b(who|what)\\s+are\\s+you\\b',
                    r'\\b(thank|thanks|appreciate)\\b',
                    r'\\b(bye|goodbye|see\\s+you)\\b'
                ],
                'description': 'General chat, greetings, identity questions'
            }
        }
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze the user query to determine the best AI module to use.
        
        Args:
            query (str): User query to analyze
            
        Returns:
            Dict containing analysis results and routing decision
        """
        query_lower = query.lower()
        scores = {'CAG': 0, 'RAG': 0, 'KAG': 0, 'SLM': 0}
        matched_patterns = {'CAG': [], 'RAG': [], 'KAG': [], 'SLM': []}
        
        # Score each module based on keyword and pattern matches
        for module, config in self.routing_patterns.items():
            # Keyword matching
            for keyword in config['keywords']:
                if keyword in query_lower:
                    scores[module] += 1
                    matched_patterns[module].append(f"keyword: {keyword}")
            
            # Pattern matching
            for pattern in config['patterns']:
                if re.search(pattern, query_lower):
                    scores[module] += 2  # Patterns get higher weight
                    matched_patterns[module].append(f"pattern: {pattern}")
        
        # Determine the best module
        best_module = max(scores, key=scores.get)
        best_score = scores[best_module]
        
        # If no clear winner, use fallback logic
        if best_score == 0:
            best_module = 'SLM'  # Default fallback
            reason = "No specific patterns matched, using general conversation"
        else:
            reason = f"Highest score ({best_score}) with patterns: {matched_patterns[best_module]}"
        
        return {
            'selected_module': best_module,
            'scores': scores,
            'matched_patterns': matched_patterns,
            'reason': reason,
            'confidence': best_score / max(sum(scores.values()), 1)
        }
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Route query to the appropriate AI module and get response.
        
        Args:
            query (str): User query
            
        Returns:
            Dict containing response from selected module
        """
        # Analyze query to determine routing
        analysis = self.analyze_query(query)
        selected_module = analysis['selected_module']
        
        self.logger.info(f"Routing query to {selected_module}: {analysis['reason']}")
        
        # Route to selected module
        try:
            if selected_module == 'CAG' and self.cag_available:
                response = self.cag_module.get_response(query)
                formatted_response = self.cag_module.format_response(response)
                
            elif selected_module == 'RAG' and self.rag_available:
                response = self.rag_module.get_response(query)
                formatted_response = self.rag_module.format_response(response)
                
            elif selected_module == 'KAG' and self.kag_available:
                response = self.kag_module.get_response(query)
                formatted_response = self.kag_module.format_response(response)
                
            elif selected_module == 'SLM' and self.slm_available:
                response = self.slm_module.get_response(query)
                formatted_response = self.slm_module.format_response(response)
                
            else:
                # Fallback if selected module is not available
                if self.slm_available:
                    response = self.slm_module.get_response(query)
                    formatted_response = self.slm_module.format_response(response)
                    selected_module = 'SLM'
                else:
                    response = {
                        'success': False,
                        'source': 'Controller',
                        'error': 'No modules available'
                    }
                    formatted_response = "I apologize, but I'm currently unable to process your request. Please try again later."
            
            # Add routing information to response
            controller_response = {
                'success': response.get('success', False),
                'response_text': formatted_response,
                'selected_module': selected_module,
                'routing_analysis': analysis,
                'module_response': response,
                'timestamp': datetime.now().isoformat()
            }
            
            return controller_response
            
        except Exception as e:
            self.logger.error(f"Error routing query: {str(e)}")
            return {
                'success': False,
                'response_text': "I encountered an error processing your request. Please try rephrasing your question.",
                'selected_module': selected_module,
                'routing_analysis': analysis,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get status of all AI modules."""
        return {
            'modules': {
                'RAG': {
                    'available': self.rag_available,
                    'description': self.routing_patterns['RAG']['description']
                },
                'KAG': {
                    'available': self.kag_available,
                    'description': self.routing_patterns['KAG']['description']
                },
                'CAG': {
                    'available': self.cag_available,
                    'description': self.routing_patterns['CAG']['description']
                },
                'SLM': {
                    'available': self.slm_available,
                    'description': self.routing_patterns['SLM']['description']
                }
            },
            'total_available': sum([
                self.rag_available, self.kag_available, 
                self.cag_available, self.slm_available
            ]),
            'controller_status': 'Active'
        }
    
    def explain_routing(self, query: str) -> str:
        """
        Explain why a particular module was selected for a query.
        
        Args:
            query (str): User query
            
        Returns:
            str: Explanation of routing decision
        """
        analysis = self.analyze_query(query)
        
        explanation = f"**Query Analysis for:** '{query}'\\n\\n"
        explanation += f"**Selected Module:** {analysis['selected_module']}\\n"
        explanation += f"**Confidence:** {analysis['confidence']:.2%}\\n\\n"
        
        explanation += "**Module Scores:**\\n"
        for module, score in analysis['scores'].items():
            status = "✅" if score > 0 else "❌" 
            explanation += f"{status} {module}: {score} points\\n"
        
        explanation += f"\\n**Reason:** {analysis['reason']}\\n\\n"
        
        explanation += "**Module Capabilities:**\\n"
        for module, config in self.routing_patterns.items():
            explanation += f"• **{module}**: {config['description']}\\n"
        
        return explanation

# Example usage and testing
if __name__ == "__main__":
    # Initialize agent controller
    controller = AgentController()
    
    # Test queries
    test_queries = [
        "Fire emergency contact number",
        "Latest water supply schedule",
        "How to apply for birth certificate?",
        "Hello, who are you?",
        "Property tax payment procedure",
        "Chennai Corporation office hours"
    ]
    
    print("🤖 Testing Agent Controller\\n" + "="*70)
    
    for query in test_queries:
        print(f"\\n**Query:** {query}")
        
        # Get routing explanation
        explanation = controller.explain_routing(query)
        print(f"**Routing Analysis:**\\n{explanation}")
        
        # Get actual response
        response = controller.route_query(query)
        print(f"**Final Response:**\\n{response['response_text']}")
        print(f"**Module Used:** {response['selected_module']}")
        print("-" * 70)
'''

with open('CivicMindAI/agent_controller.py', 'w') as f:
    f.write(agent_controller_code)

print("✅ Agent Controller module created!")
print("Features implemented:")
print("  • Intelligent query analysis and routing")
print("  • Pattern-based module selection")
print("  • Keyword and regex matching")
print("  • Confidence scoring system")
print("  • Fallback mechanism for unavailable modules")
print("  • Comprehensive error handling")
print("  • Module status monitoring")
print("  • Routing explanation for transparency")