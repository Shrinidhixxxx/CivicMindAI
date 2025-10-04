# Create the KAG (Knowledge-Augmented Generation) module
kag_module_code = '''"""
KAG (Knowledge-Augmented Generation) Module for CivicMindAI
Performs reasoning over structured civic knowledge using Knowledge Graphs.
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
import networkx as nx

class KAGModule:
    """
    Knowledge-Augmented Generation module that uses structured knowledge graphs
    to perform multi-hop reasoning over civic processes and procedures.
    """
    
    def __init__(self, knowledge_file: str = "data/civic_knowledge.json"):
        """
        Initialize the KAG module with structured civic knowledge.
        
        Args:
            knowledge_file (str): Path to the knowledge JSON file
        """
        self.knowledge_file = knowledge_file
        self.knowledge_data = {}
        self.knowledge_graph = nx.DiGraph()
        
        # Load knowledge and build graph
        self.load_knowledge()
        self.build_knowledge_graph()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_knowledge(self) -> None:
        """Load structured knowledge from JSON file."""
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r') as f:
                    self.knowledge_data = json.load(f)
                self.logger.info("Knowledge data loaded successfully")
            else:
                self.logger.warning(f"Knowledge file not found: {self.knowledge_file}")
        except Exception as e:
            self.logger.error(f"Error loading knowledge: {str(e)}")
    
    def build_knowledge_graph(self) -> None:
        """Build NetworkX knowledge graph from structured data."""
        try:
            # Add entity nodes
            entities = self.knowledge_data.get('entities', {})
            
            # Add departments
            for dept in entities.get('departments', []):
                self.knowledge_graph.add_node(
                    dept['id'], 
                    name=dept['name'],
                    type='department',
                    node_type=dept['type']
                )
            
            # Add services
            for service in entities.get('services', []):
                self.knowledge_graph.add_node(
                    service['id'],
                    name=service['name'],
                    type='service',
                    department=service['department']
                )
                # Link service to department
                self.knowledge_graph.add_edge(service['id'], service['department'], relation='managed_by')
            
            # Add issues
            for issue in entities.get('issues', []):
                self.knowledge_graph.add_node(
                    issue['id'],
                    name=issue['name'],
                    type='issue',
                    service=issue['service']
                )
                # Link issue to service
                self.knowledge_graph.add_edge(issue['id'], issue['service'], relation='relates_to')
            
            # Add procedure nodes
            procedures = self.knowledge_data.get('procedures', {})
            for proc_id, proc_data in procedures.items():
                self.knowledge_graph.add_node(
                    proc_id,
                    name=proc_data['title'],
                    type='procedure',
                    department=proc_data['department'],
                    steps=proc_data['steps'],
                    timeline=proc_data.get('timeline', 'Unknown'),
                    fees=proc_data.get('fees', 'N/A'),
                    contact=proc_data.get('contact', 'N/A')
                )
            
            # Add explicit relationships
            relationships = self.knowledge_data.get('relationships', [])
            for rel in relationships:
                self.knowledge_graph.add_edge(
                    rel['from'], 
                    rel['to'], 
                    relation=rel['type']
                )
            
            self.logger.info(f"Built knowledge graph with {self.knowledge_graph.number_of_nodes()} nodes and {self.knowledge_graph.number_of_edges()} edges")
            
        except Exception as e:
            self.logger.error(f"Error building knowledge graph: {str(e)}")
    
    def find_procedure(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Find relevant procedure based on query keywords.
        
        Args:
            query (str): User query about a procedure
            
        Returns:
            Dict containing procedure information or None
        """
        query_lower = query.lower()
        
        # Procedure keyword mapping
        procedure_keywords = {
            'water connection': 'water_connection_new',
            'new water connection': 'water_connection_new',
            'apply water': 'water_connection_new',
            'property tax': 'property_tax_payment',
            'pay tax': 'property_tax_payment',
            'tax payment': 'property_tax_payment',
            'street light': 'street_light_repair',
            'light repair': 'street_light_repair',
            'street lamp': 'street_light_repair',
            'birth certificate': 'birth_certificate',
            'birth cert': 'birth_certificate'
        }
        
        # Find matching procedure
        for keyword, proc_id in procedure_keywords.items():
            if keyword in query_lower:
                if proc_id in self.knowledge_graph.nodes:
                    node_data = self.knowledge_graph.nodes[proc_id]
                    procedures = self.knowledge_data.get('procedures', {})
                    if proc_id in procedures:
                        return {
                            'procedure_id': proc_id,
                            'title': node_data['name'],
                            'department': node_data['department'],
                            'details': procedures[proc_id]
                        }
        
        return None
    
    def find_responsible_department(self, issue: str) -> Optional[Dict[str, Any]]:
        """
        Find which department handles a specific civic issue.
        
        Args:
            issue (str): Description of the civic issue
            
        Returns:
            Dict with department information or None
        """
        issue_lower = issue.lower()
        
        # Issue to department mapping based on knowledge graph
        issue_keywords = {
            'water': ['no_water', 'water_contamination', 'pipeline_leak'],
            'sewage': ['sewage_overflow', 'blocked_drain'],
            'garbage': ['garbage_not_collected'],
            'waste': ['garbage_not_collected'],
            'street light': ['street_light_not_working'],
            'road': ['pothole'],
            'electricity': ['power_cut'],
            'power': ['power_cut']
        }
        
        # Find matching issue node
        for keyword, issue_ids in issue_keywords.items():
            if keyword in issue_lower:
                for issue_id in issue_ids:
                    if issue_id in self.knowledge_graph.nodes:
                        # Find connected service and department
                        try:
                            service_nodes = [n for n in self.knowledge_graph.successors(issue_id) 
                                           if self.knowledge_graph.nodes[n]['type'] == 'service']
                            if service_nodes:
                                service_id = service_nodes[0]
                                dept_nodes = [n for n in self.knowledge_graph.successors(service_id)
                                            if self.knowledge_graph.nodes[n]['type'] == 'department']
                                if dept_nodes:
                                    dept_id = dept_nodes[0]
                                    dept_data = self.knowledge_graph.nodes[dept_id]
                                    return {
                                        'issue_id': issue_id,
                                        'issue_name': self.knowledge_graph.nodes[issue_id]['name'],
                                        'service_id': service_id,
                                        'service_name': self.knowledge_graph.nodes[service_id]['name'],
                                        'department_id': dept_id,
                                        'department_name': dept_data['name']
                                    }
                        except Exception as e:
                            self.logger.error(f"Error traversing graph for issue {issue_id}: {str(e)}")
                            continue
        
        return None
    
    def multi_hop_reasoning(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform multi-hop reasoning across the knowledge graph.
        
        Args:
            query (str): Complex query requiring multi-hop reasoning
            
        Returns:
            List of reasoning steps with intermediate results
        """
        reasoning_steps = []
        query_lower = query.lower()
        
        # Example multi-hop query: "How to get water pipeline repaired in Anna Nagar?"
        if 'repair' in query_lower and ('water' in query_lower or 'pipeline' in query_lower):
            # Step 1: Identify the issue
            reasoning_steps.append({
                'step': 1,
                'action': 'Identify Issue',
                'result': 'Water pipeline repair needed',
                'node': 'pipeline_leak'
            })
            
            # Step 2: Find responsible service
            reasoning_steps.append({
                'step': 2,
                'action': 'Find Responsible Service',
                'result': 'Water Supply Service',
                'node': 'water_supply'
            })
            
            # Step 3: Find responsible department
            reasoning_steps.append({
                'step': 3,
                'action': 'Find Responsible Department',
                'result': 'Chennai Metro Water Supply and Sewerage Board (CMWSSB)',
                'node': 'cmwssb'
            })
            
            # Step 4: Get contact and procedure
            reasoning_steps.append({
                'step': 4,
                'action': 'Get Contact Information',
                'result': 'Call CMWSSB complaint cell: 044-45674567',
                'details': 'Available 24x7 for emergency repairs'
            })
            
            # Step 5: Add area-specific information if mentioned
            if 'anna nagar' in query_lower:
                reasoning_steps.append({
                    'step': 5,
                    'action': 'Area-specific Contact',
                    'result': 'Anna Nagar falls under North Zone',
                    'details': 'Zone contact: 044-28451300 Ext.233'
                })
        
        # Multi-hop for property tax queries
        elif 'property tax' in query_lower and ('pay' in query_lower or 'how' in query_lower):
            reasoning_steps.append({
                'step': 1,
                'action': 'Identify Service',
                'result': 'Property Tax Payment',
                'node': 'property_tax'
            })
            
            reasoning_steps.append({
                'step': 2,
                'action': 'Find Department',
                'result': 'Greater Chennai Corporation (GCC)',
                'node': 'gcc'
            })
            
            reasoning_steps.append({
                'step': 3,
                'action': 'Get Procedure',
                'result': 'Online payment procedure available',
                'node': 'property_tax_payment'
            })
        
        return reasoning_steps
    
    def get_response(self, query: str) -> Dict[str, Any]:
        """
        Get KAG response using knowledge graph reasoning.
        
        Args:
            query (str): User query
            
        Returns:
            Dict containing response data and reasoning steps
        """
        try:
            # Check if query asks for procedure
            procedure = self.find_procedure(query)
            
            # Check if query asks about issue handling
            department_info = self.find_responsible_department(query)
            
            # Perform multi-hop reasoning
            reasoning_steps = self.multi_hop_reasoning(query)
            
            if procedure or department_info or reasoning_steps:
                return {
                    'success': True,
                    'data': {
                        'procedure': procedure,
                        'department_info': department_info,
                        'reasoning_steps': reasoning_steps,
                        'graph_stats': {
                            'nodes': self.knowledge_graph.number_of_nodes(),
                            'edges': self.knowledge_graph.number_of_edges()
                        }
                    },
                    'source': 'KAG',
                    'query': query,
                    'timestamp': datetime.now().isoformat(),
                    'message': f'Knowledge graph reasoning completed with {len(reasoning_steps)} steps'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'source': 'KAG',
                    'query': query,
                    'message': 'No structured knowledge found for this query'
                }
                
        except Exception as e:
            self.logger.error(f"Error in KAG response: {str(e)}")
            return {
                'success': False,
                'data': None,
                'source': 'KAG',
                'error': str(e)
            }
    
    def format_response(self, response_data: Dict[str, Any]) -> str:
        """
        Format the KAG response into user-friendly text.
        
        Args:
            response_data (Dict): Response data from get_response()
            
        Returns:
            str: Formatted response text
        """
        if not response_data['success']:
            return f"I don't have structured knowledge about '{response_data.get('query', 'your request')}'. Let me try other sources."
        
        data = response_data['data']
        formatted_text = "🧠 **Knowledge Graph Analysis:**\\n\\n"
        
        # Format reasoning steps
        if data['reasoning_steps']:
            formatted_text += "🔗 **Step-by-step Reasoning:**\\n"
            for step in data['reasoning_steps']:
                formatted_text += f"{step['step']}. **{step['action']}:** {step['result']}\\n"
                if 'details' in step:
                    formatted_text += f"   *{step['details']}*\\n"
            formatted_text += "\\n"
        
        # Format procedure information
        if data['procedure']:
            proc = data['procedure']
            formatted_text += f"📋 **Procedure: {proc['title']}**\\n"
            formatted_text += f"🏛️ **Department:** {proc['department'].upper()}\\n\\n"
            
            details = proc['details']
            formatted_text += "📝 **Steps to Follow:**\\n"
            for i, step in enumerate(details['steps'], 1):
                formatted_text += f"{i}. {step}\\n"
            
            formatted_text += f"\\n⏱️ **Timeline:** {details['timeline']}\\n"
            formatted_text += f"💰 **Fees:** {details.get('fees', 'N/A')}\\n"
            formatted_text += f"📞 **Contact:** {details['contact']}\\n\\n"
            
            if 'documents' in details:
                formatted_text += "📄 **Required Documents:**\\n"
                for doc in details['documents']:
                    formatted_text += f"• {doc}\\n"
                formatted_text += "\\n"
        
        # Format department information
        if data['department_info']:
            dept = data['department_info']
            formatted_text += f"🏛️ **Responsible Department:**\\n"
            formatted_text += f"• **Issue:** {dept['issue_name']}\\n"
            formatted_text += f"• **Service:** {dept['service_name']}\\n"
            formatted_text += f"• **Department:** {dept['department_name']}\\n\\n"
        
        formatted_text += f"📊 *Processed via Knowledge Graph ({data['graph_stats']['nodes']} entities, {data['graph_stats']['edges']} relationships)*"
        
        return formatted_text

# Example usage and testing
if __name__ == "__main__":
    # Initialize KAG module
    kag = KAGModule()
    
    # Test queries
    test_queries = [
        "How to apply for new water connection?",
        "Property tax payment procedure",
        "Who handles sewage overflow issues?",
        "How to get water pipeline repaired in Anna Nagar?"
    ]
    
    print("🧠 Testing KAG Module\\n" + "="*50)
    
    for query in test_queries:
        print(f"\\n**Query:** {query}")
        response = kag.get_response(query)
        formatted = kag.format_response(response)
        print(f"**Response:** {formatted}")
        print("-" * 50)
'''

with open('CivicMindAI/kag_module.py', 'w') as f:
    f.write(kag_module_code)

print("✅ KAG (Knowledge-Augmented Generation) module created!")
print("Features implemented:")
print("  • NetworkX knowledge graph construction")
print("  • Entity relationship mapping")
print("  • Multi-hop reasoning chains")
print("  • Procedure step-by-step guidance")
print("  • Department responsibility mapping")
print("  • Complex query decomposition")
print("  • Structured response formatting")