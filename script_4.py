# Create sample civic documents for RAG module
civic_docs = {
    "water_supply_guidelines.txt": """
CHENNAI METRO WATER SUPPLY AND SEWERAGE BOARD
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

WATER QUALITY STANDARDS:
- pH Level: 6.5 to 8.5
- TDS: Less than 500 ppm
- Chlorine residual: 0.2 to 0.5 ppm
- Tested at 145 sampling points daily

NEW CONNECTION PROCEDURE:
1. Application submission with documents
2. Site inspection within 7 days
3. Estimate approval and payment
4. Connection within 15 working days
5. Quality check and meter installation

COMPLAINT RESOLUTION:
- Emergency repairs: Within 24 hours
- Regular maintenance: 3-5 working days  
- Major pipeline work: 7-15 days
- Complaint tracking via SMS and website

CONTACT INFORMATION:
24x7 Complaint Cell: 044-45674567
Customer Care: 044-28451300
Website: https://cmwssb.tn.gov.in
Emergency SMS: WATER <COMPLAINT> to 56677
""",
    
    "property_tax_rules_2025.txt": """
GREATER CHENNAI CORPORATION
Property Tax Assessment Rules - 2025

PROPERTY TAX RATES:
Residential Properties:
- Built-up area up to 600 sq ft: ₹3 per sq ft
- Built-up area 600-1200 sq ft: ₹6 per sq ft  
- Built-up area above 1200 sq ft: ₹10 per sq ft

Commercial Properties:
- Shops and offices: ₹15 per sq ft
- Hotels and lodges: ₹20 per sq ft
- Industries: ₹12 per sq ft

ADDITIONAL CHARGES:
- Library cess: 5% of property tax
- Education cess: 2% of property tax  
- Scavenging charges: ₹100 per year
- Lighting charges: ₹200 per year

DUE DATES AND PENALTIES:
- Annual due date: 31st March
- Late payment penalty: 2% per month
- Disconnection of water supply after 6 months default
- Legal action after 1 year default

ONLINE PAYMENT OPTIONS:
- Net banking from all major banks
- Credit/Debit cards (Visa, Master, RuPay)
- UPI payments
- Chennai Corporation mobile app

EXEMPTIONS AVAILABLE:
- Senior citizens (above 65): 25% discount
- Persons with disabilities: 50% discount  
- Widow/divorced women: 30% discount
- Ex-servicemen: 25% discount

DOCUMENTS REQUIRED:
- Property ownership documents
- Previous year tax receipt
- Identity proof of owner
- Mobile number for SMS alerts
""",

    "waste_management_schedule.txt": """
GREATER CHENNAI CORPORATION
Solid Waste Management Schedule - October 2025

GARBAGE COLLECTION TIMINGS:
Residential Areas: 6:00 AM to 10:00 AM (Daily)
Commercial Areas: 10:00 PM to 2:00 AM (Daily)  
Markets: 11:00 PM to 4:00 AM (Daily)
Bulk waste: Wednesdays and Saturdays

SEGREGATION REQUIREMENTS:
Wet Waste (Green bins): Food waste, vegetable peels, garden waste
Dry Waste (Blue bins): Paper, plastic, metal, glass
E-Waste: Batteries, electronics, bulbs (Special collection monthly)
Medical Waste: Masks, gloves, syringes (Red bags - Daily collection from clinics)

WARD-WISE COLLECTION ROUTES:
Wards 1-50: Monday, Wednesday, Friday (Primary collection)
Wards 51-100: Tuesday, Thursday, Saturday (Primary collection)
Wards 101-200: Daily collection with 2-shift system

COMPOSTING FACILITIES:
- Perungudi: 1000 MT/day capacity
- Kodungaiyur: 600 MT/day capacity  
- Sholinganallur: 800 MT/day capacity
- Mini composting: Available in 50 locations

PENALTIES FOR VIOLATIONS:
- Improper segregation: ₹500 fine
- Littering on roads: ₹200 fine
- Burning garbage: ₹1000 fine
- Commercial dumping in residential bins: ₹2000 fine

COMPLAINTS AND REPORTING:
- Namma Chennai App: Report missed collections
- Helpline: 1913 (24x7)
- WhatsApp: 94440 42097
- Email: swr.gcc@tn.gov.in

SPECIAL SERVICES:
- Bulk waste pickup: Schedule via app
- Construction debris: Separate collection on request  
- Hazardous waste: Monthly collection drives
- Organic waste converters: Subsidized distribution
""",

    "emergency_services_directory.txt": """
CHENNAI EMERGENCY SERVICES DIRECTORY
Updated: October 2025

FIRE AND RESCUE SERVICES:
Emergency Number: 101
Control Room: 044-28447788
30 Fire Stations across Chennai
Average response time: 4-6 minutes in city limits
24x7 Ambulance service available

POLICE SERVICES:
Emergency: 100
Control Room: 044-28447700
Traffic Control: 103
Women Helpline: 1091 (24x7)
Child Helpline: 1098
Cyber Crime: 1930

MEDICAL EMERGENCY:
Ambulance: 108 (Free service)
Private ambulance: 1962
Blood bank emergency: 104
Poison control: 044-26591781 (AIIMS)

DISASTER MANAGEMENT:
State Control Room: 044-28527175
District Control Room: 044-28520314
Flood Control Room: 1913 (During monsoon)
Cyclone Alert: Download 'Tamil Nadu Alert' app

UTILITIES EMERGENCY:
Gas Leak: 1906
Power failure: 94987 94987 (TANGEDCO)
Water emergency: 044-45674567 (CMWSSB)
Telecom fault: 198 (BSNL), 121 (Airtel)

TRANSPORT EMERGENCY:
Railway enquiry: 139
Bus enquiry: 044-28542325  
Metro helpline: 044-25385555
Airport enquiry: 044-22560551

GOVERNMENT HELPLINES:
Chief Minister's Cell: 1100
Collector Office: 044-25620314
Revenue enquiry: 044-25383006
RTI enquiry: 044-25384510

SPECIAL HELPLINES:
Senior citizen helpline: 14567
Tourist helpline: 1363
Consumer forum: 1800-425-2005
Legal aid: 15100
""",

    "sewage_management_update.txt": """
CHENNAI METRO WATER SUPPLY AND SEWERAGE BOARD
Sewage Management System Update - October 2025

UNDERGROUND DRAINAGE COVERAGE:
Total areas covered: 426 sq km
Population served: 8.2 million  
Sewage generation: 842 MLD (Million Litres per Day)
Treatment capacity: 748 MLD across 14 STPs

SEWAGE TREATMENT PLANTS (STPs):
1. Nesapakkam STP: 90 MLD
2. Koyambedu STP: 90 MLD  
3. Perungudi STP: 126 MLD
4. Sholinganallur STP: 54 MLD
5. Kodungaiyur STP: 180 MLD

RECENT IMPROVEMENTS (2025):
- 45 km new sewer lines added
- 120 pumping stations upgraded
- Real-time monitoring system installed
- Mobile sewage treatment units for emergencies

COMMON SEWAGE ISSUES:
Sewage overflow: Report to 044-45674567
Manhole blocks: Emergency response in 2 hours  
Pipe bursts: Repair within 24 hours
Bad odor: Investigation within 48 hours

ONLINE SERVICES:
- Sewage complaint registration
- Treatment plant capacity tracker
- Water quality reports (monthly)
- Construction clearance applications

ENVIRONMENTAL COMPLIANCE:
- BOD levels: <10 mg/L (Target: <5 mg/L by 2026)
- COD levels: <50 mg/L 
- pH maintained: 6.5-8.5
- Daily monitoring at all STPs

CITIZEN INITIATIVES:
- Septic tank cleaning subsidy: ₹1000 per household
- Sewage connection drive: 50,000 new connections in 2025
- School awareness programs: 200 schools covered
- Community composting toilets: 45 new installations

EMERGENCY PROTOCOLS:
- Heavy rain sewage backup: Mobile pumps deployed
- Treatment plant failure: Bypass treatment activated  
- Chemical spill: Hazmat team response in 30 minutes
- Public health alerts: SMS to registered users
"""
}

# Create civic documents directory and files
os.makedirs('CivicMindAI/data/civic_docs', exist_ok=True)

for filename, content in civic_docs.items():
    with open(f'CivicMindAI/data/civic_docs/{filename}', 'w') as f:
        f.write(content)

print("✅ Sample civic documents created successfully!")
print(f"Created {len(civic_docs)} documents:")
for filename in civic_docs.keys():
    print(f"  • {filename}")
    word_count = len(civic_docs[filename].split())
    print(f"    - {word_count} words")