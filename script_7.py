# Create the CAG (Cache-Augmented Generation) module
cag_module_code = '''"""
CAG (Cache-Augmented Generation) Module for CivicMindAI
Provides instant responses for frequently asked civic information using cached data.
"""

import json
import os
from typing import Dict, Any, Optional
import logging

class CAGModule:
    """
    Cache-Augmented Generation module that provides instant responses 
    for static, frequently requested civic information.
    """
    
    def __init__(self, cache_file_path: str = "data/civic_cache.json"):
        """
        Initialize the CAG module with cached civic data.
        
        Args:
            cache_file_path (str): Path to the cache JSON file
        """
        self.cache_file_path = cache_file_path
        self.cache_data = {}
        self.load_cache()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_cache(self) -> None:
        """Load cached data from JSON file."""
        try:
            if os.path.exists(self.cache_file_path):
                with open(self.cache_file_path, 'r') as f:
                    self.cache_data = json.load(f)
                self.logger.info(f"Cache loaded successfully with {len(self.cache_data)} categories")
            else:
                self.logger.warning(f"Cache file not found at {self.cache_file_path}")
        except Exception as e:
            self.logger.error(f"Error loading cache: {str(e)}")
    
    def search_cache(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for information in cached data based on query keywords.
        
        Args:
            query (str): User query to search for
            
        Returns:
            Dict containing cached information or None if not found
        """
        query_lower = query.lower()
        
        # Emergency contact searches
        if any(keyword in query_lower for keyword in ['emergency', 'helpline', 'contact', 'phone', 'number']):
            return self._search_emergency_contacts(query_lower)
        
        # Government office searches
        if any(keyword in query_lower for keyword in ['office', 'collector', 'mayor', 'government']):
            return self._search_government_contacts(query_lower)
        
        # Civic service searches  
        if any(keyword in query_lower for keyword in ['tax', 'certificate', 'license', 'permit']):
            return self._search_civic_services(query_lower)
        
        # Zone-specific searches
        if any(keyword in query_lower for keyword in ['zone', 'area', 'ward', 'anna nagar', 'adyar']):
            return self._search_zone_info(query_lower)
        
        # Quick info searches
        if any(keyword in query_lower for keyword in ['timing', 'hours', 'schedule', 'website']):
            return self._search_quick_info(query_lower)
            
        return None
    
    def _search_emergency_contacts(self, query: str) -> Optional[Dict[str, Any]]:
        """Search emergency contacts based on query."""
        emergency_keywords = {
            'fire': 'fire',
            'police': 'police', 
            'ambulance': 'ambulance',
            'medical': 'ambulance',
            'hospital': 'ambulance',
            'flood': 'flood_helpline',
            'water emergency': 'cmwssb_complaint',
            'electricity': 'electricity_complaint',
            'gas': 'gas_leak',
            'women': 'women_helpline',
            'child': 'child_helpline',
            'corporation': 'chennai_corporation'
        }
        
        emergency_data = self.cache_data.get('emergency_contacts', {})
        
        for keyword, contact_key in emergency_keywords.items():
            if keyword in query:
                if contact_key in emergency_data:
                    return {
                        'type': 'emergency_contact',
                        'service': keyword.title(),
                        'number': emergency_data[contact_key],
                        'availability': '24x7' if contact_key in ['fire', 'police', 'ambulance'] else 'Office hours'
                    }
        
        # Return all emergency contacts if general emergency query
        if 'emergency' in query and 'all' in query:
            return {
                'type': 'all_emergency_contacts',
                'contacts': emergency_data
            }
            
        return None
    
    def _search_government_contacts(self, query: str) -> Optional[Dict[str, Any]]:
        """Search government office contacts."""
        gov_data = self.cache_data.get('government_contacts', {})
        
        gov_keywords = {
            'collector': 'collector_office',
            'mayor': 'mayor_office', 
            'district': 'district_collector',
            'cm': 'cm_cell',
            'chief minister': 'cm_cell',
            'police control': 'tn_police_control'
        }
        
        for keyword, contact_key in gov_keywords.items():
            if keyword in query:
                if contact_key in gov_data:
                    return {
                        'type': 'government_contact',
                        'office': keyword.title(),
                        'number': gov_data[contact_key],
                        'timing': 'Office hours (9:30 AM - 5:30 PM)'
                    }
        
        return None
    
    def _search_civic_services(self, query: str) -> Optional[Dict[str, Any]]:
        """Search civic service helplines."""
        services_data = self.cache_data.get('civic_services_helplines', {})
        
        service_keywords = {
            'property tax': 'property_tax',
            'water tax': 'water_tax',
            'birth certificate': 'birth_certificate',
            'death certificate': 'death_certificate',
            'trade license': 'trade_license',
            'building permit': 'building_permit',
            'marriage': 'marriage_registration'
        }
        
        for keyword, service_key in service_keywords.items():
            if keyword in query:
                if service_key in services_data:
                    return {
                        'type': 'civic_service',
                        'service': keyword.title(),
                        'helpline': services_data[service_key],
                        'timing': 'Office hours'
                    }
        
        return None
    
    def _search_zone_info(self, query: str) -> Optional[Dict[str, Any]]:
        """Search zone-specific contact information."""
        zones_data = self.cache_data.get('zone_contacts', {})
        
        zone_keywords = {
            'north': 'zone_1_north',
            'north east': 'zone_2_north_east', 
            'central': 'zone_3_central',
            'south west': 'zone_4_south_west',
            'south': 'zone_5_south',
            'adyar': 'zone_6_adyar',
            'anna nagar': 'zone_7_anna_nagar',
            'teynampet': 'zone_8_teynampet'
        }
        
        for keyword, zone_key in zone_keywords.items():
            if keyword in query:
                if zone_key in zones_data:
                    return {
                        'type': 'zone_contact',
                        'zone': keyword.title(),
                        'contact': zones_data[zone_key],
                        'services': 'Water supply, complaints, maintenance'
                    }
        
        return None
    
    def _search_quick_info(self, query: str) -> Optional[Dict[str, Any]]:
        """Search quick information like timings, schedules."""
        quick_data = self.cache_data.get('quick_info', {})
        
        info_keywords = {
            'office hours': 'corporation_office_hours',
            'timing': 'corporation_office_hours',
            'water supply': 'water_supply_timings',
            'garbage': 'garbage_collection',
            'tax due': 'property_tax_due_date',
            'website': ['corporation_website', 'cmwssb_website']
        }
        
        for keyword, info_key in info_keywords.items():
            if keyword in query:
                if isinstance(info_key, list):
                    # Multiple websites
                    websites = {k: quick_data.get(k) for k in info_key if k in quick_data}
                    return {
                        'type': 'websites',
                        'websites': websites
                    }
                elif info_key in quick_data:
                    return {
                        'type': 'quick_info',
                        'info_type': keyword.title(),
                        'details': quick_data[info_key]
                    }
        
        return None
    
    def get_response(self, query: str) -> Dict[str, Any]:
        """
        Get cached response for a query.
        
        Args:
            query (str): User query
            
        Returns:
            Dict containing response data and metadata
        """
        try:
            cached_result = self.search_cache(query)
            
            if cached_result:
                return {
                    'success': True,
                    'data': cached_result,
                    'source': 'CAG',
                    'response_time': 'Instant',
                    'message': f'Retrieved from cache: {cached_result["type"]}'
                }
            else:
                return {
                    'success': False,
                    'data': None,
                    'source': 'CAG',
                    'message': 'No cached information found for this query'
                }
                
        except Exception as e:
            self.logger.error(f"Error in CAG response: {str(e)}")
            return {
                'success': False,
                'data': None,
                'source': 'CAG',
                'error': str(e)
            }
    
    def format_response(self, response_data: Dict[str, Any]) -> str:
        """
        Format the cached response into user-friendly text.
        
        Args:
            response_data (Dict): Response data from get_response()
            
        Returns:
            str: Formatted response text
        """
        if not response_data['success']:
            return "I couldn't find that information in my cache. Let me search other sources for you."
        
        data = response_data['data']
        response_type = data.get('type', '')
        
        if response_type == 'emergency_contact':
            return f"🚨 **{data['service']} Emergency**\\n" \\
                   f"📞 **Contact:** {data['number']}\\n" \\
                   f"⏰ **Availability:** {data['availability']}"
        
        elif response_type == 'government_contact':
            return f"🏛️ **{data['office']}**\\n" \\
                   f"📞 **Contact:** {data['number']}\\n" \\
                   f"⏰ **Timing:** {data['timing']}"
        
        elif response_type == 'civic_service':
            return f"📋 **{data['service']}**\\n" \\
                   f"📞 **Helpline:** {data['helpline']}\\n" \\
                   f"⏰ **Timing:** {data['timing']}"
        
        elif response_type == 'zone_contact':
            return f"📍 **{data['zone']} Zone**\\n" \\
                   f"📞 **Contact:** {data['contact']}\\n" \\
                   f"🔧 **Services:** {data['services']}"
        
        elif response_type == 'quick_info':
            return f"ℹ️ **{data['info_type']}**\\n" \\
                   f"📝 **Details:** {data['details']}"
        
        elif response_type == 'websites':
            websites_text = "\\n".join([f"• {name.replace('_', ' ').title()}: {url}" 
                                     for name, url in data['websites'].items()])
            return f"🌐 **Official Websites:**\\n{websites_text}"
        
        elif response_type == 'all_emergency_contacts':
            contacts_text = "\\n".join([f"• {name.replace('_', ' ').title()}: {number}" 
                                      for name, number in data['contacts'].items()])
            return f"🚨 **All Emergency Contacts:**\\n{contacts_text}"
        
        else:
            return f"✅ Information retrieved from cache: {str(data)}"

# Example usage and testing
if __name__ == "__main__":
    # Initialize CAG module
    cag = CAGModule()
    
    # Test queries
    test_queries = [
        "fire emergency number",
        "property tax helpline", 
        "Anna Nagar zone contact",
        "corporation office hours",
        "water supply timing",
        "all emergency contacts"
    ]
    
    print("🧪 Testing CAG Module\\n" + "="*50)
    
    for query in test_queries:
        print(f"\\n**Query:** {query}")
        response = cag.get_response(query)
        formatted = cag.format_response(response)
        print(f"**Response:** {formatted}")
        print("-" * 30)
'''

with open('CivicMindAI/cag_module.py', 'w') as f:
    f.write(cag_module_code)

print("✅ CAG (Cache-Augmented Generation) module created!")
print("Features implemented:")
print("  • Instant cache-based responses")
print("  • Emergency contact lookup")
print("  • Government office information")
print("  • Civic service helplines")
print("  • Zone-specific contacts")
print("  • Quick information retrieval")
print("  • Response formatting and logging")