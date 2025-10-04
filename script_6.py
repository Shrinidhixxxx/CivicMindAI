import os
import shutil

# Remove the existing civic_docs file and create as directory
if os.path.exists('CivicMindAI/data/civic_docs'):
    if os.path.isfile('CivicMindAI/data/civic_docs'):
        os.remove('CivicMindAI/data/civic_docs')
    else:
        shutil.rmtree('CivicMindAI/data/civic_docs')

# Create the directory properly
os.makedirs('CivicMindAI/data/civic_docs', exist_ok=True)

# Create civic documents
civic_docs = {
    "water_supply_guidelines.txt": """CHENNAI METRO WATER SUPPLY AND SEWERAGE BOARD
Water Supply Guidelines - October 2025

WATER SUPPLY TIMINGS:
- Morning: 6:00 AM to 8:00 AM  
- Evening: 6:00 PM to 8:00 PM
- Total supply duration: 4 hours per day

ZONE WISE WATER SUPPLY:
Zone 1 (North): Anna Nagar, Kilpauk, Purasawalkam
Zone 2 (North East): Royapuram, Thiruvottiyur, Manali
Zone 3 (Central): Egmore, Chetpet, Nungambakkam  
Zone 4 (South West): Kodambakkam, Saidapet, West Mambalam
Zone 5 (South): Adyar, Thiruvanmiyur, Sholinganallur

CONTACT INFORMATION:
24x7 Complaint Cell: 044-45674567
Customer Care: 044-28451300
Website: https://cmwssb.tn.gov.in""",
    
    "property_tax_rules_2025.txt": """GREATER CHENNAI CORPORATION
Property Tax Assessment Rules - 2025

PROPERTY TAX RATES:
Residential Properties:
- Built-up area up to 600 sq ft: ₹3 per sq ft
- Built-up area 600-1200 sq ft: ₹6 per sq ft  
- Built-up area above 1200 sq ft: ₹10 per sq ft

DUE DATES AND PENALTIES:
- Annual due date: 31st March
- Late payment penalty: 2% per month

EXEMPTIONS AVAILABLE:
- Senior citizens (above 65): 25% discount
- Persons with disabilities: 50% discount""",

    "waste_management_schedule.txt": """GREATER CHENNAI CORPORATION
Solid Waste Management Schedule - October 2025

GARBAGE COLLECTION TIMINGS:
Residential Areas: 6:00 AM to 10:00 AM (Daily)
Commercial Areas: 10:00 PM to 2:00 AM (Daily)  
Markets: 11:00 PM to 4:00 AM (Daily)

COMPLAINTS AND REPORTING:
- Namma Chennai App: Report missed collections
- Helpline: 1913 (24x7)
- WhatsApp: 94440 42097""",

    "emergency_services_directory.txt": """CHENNAI EMERGENCY SERVICES DIRECTORY
Updated: October 2025

FIRE AND RESCUE SERVICES:
Emergency Number: 101
Control Room: 044-28447788

POLICE SERVICES:
Emergency: 100
Control Room: 044-28447700
Women Helpline: 1091 (24x7)
Child Helpline: 1098

MEDICAL EMERGENCY:
Ambulance: 108 (Free service)
Blood bank emergency: 104"""
}

# Write the documents
for filename, content in civic_docs.items():
    with open(f'CivicMindAI/data/civic_docs/{filename}', 'w') as f:
        f.write(content)

print("✅ Sample civic documents created successfully!")
print(f"Created {len(civic_docs)} documents:")
for filename in civic_docs.keys():
    print(f"  • {filename}")
    word_count = len(civic_docs[filename].split())
    print(f"    - {word_count} words")