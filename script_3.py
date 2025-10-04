# Create civic_knowledge.json with structured knowledge graph data
civic_knowledge = {
    "entities": {
        "departments": [
            {"id": "gcc", "name": "Greater Chennai Corporation", "type": "government"},
            {"id": "cmwssb", "name": "Chennai Metro Water Supply and Sewerage Board", "type": "government"},
            {"id": "tneb", "name": "Tamil Nadu Electricity Board", "type": "government"},
            {"id": "tn_police", "name": "Tamil Nadu Police", "type": "government"},
            {"id": "fire_dept", "name": "Fire Department", "type": "emergency"},
            {"id": "health_dept", "name": "Health Department", "type": "government"}
        ],
        "services": [
            {"id": "water_supply", "name": "Water Supply", "department": "cmwssb"},
            {"id": "sewage", "name": "Sewage Management", "department": "cmwssb"},
            {"id": "property_tax", "name": "Property Tax", "department": "gcc"},
            {"id": "waste_mgmt", "name": "Waste Management", "department": "gcc"},
            {"id": "street_lights", "name": "Street Lighting", "department": "gcc"},
            {"id": "roads", "name": "Road Maintenance", "department": "gcc"},
            {"id": "electricity", "name": "Electricity", "department": "tneb"},
            {"id": "birth_cert", "name": "Birth Certificate", "department": "gcc"},
            {"id": "death_cert", "name": "Death Certificate", "department": "gcc"}
        ],
        "issues": [
            {"id": "no_water", "name": "No Water Supply", "service": "water_supply"},
            {"id": "water_contamination", "name": "Water Contamination", "service": "water_supply"},
            {"id": "pipeline_leak", "name": "Pipeline Leak", "service": "water_supply"},
            {"id": "sewage_overflow", "name": "Sewage Overflow", "service": "sewage"},
            {"id": "blocked_drain", "name": "Blocked Drain", "service": "sewage"},
            {"id": "garbage_not_collected", "name": "Garbage Not Collected", "service": "waste_mgmt"},
            {"id": "street_light_not_working", "name": "Street Light Not Working", "service": "street_lights"},
            {"id": "pothole", "name": "Pothole on Road", "service": "roads"},
            {"id": "power_cut", "name": "Power Cut", "service": "electricity"}
        ]
    },
    "procedures": {
        "water_connection_new": {
            "title": "Apply for New Water Connection",
            "department": "cmwssb",
            "steps": [
                "Visit CMWSSB website or nearest office",
                "Fill Form No. 1 (New Connection Application)",
                "Submit required documents: Property tax receipt, ID proof, Address proof",
                "Pay connection charges: ₹1,500 for 15mm, ₹2,500 for 20mm",
                "Schedule site inspection",
                "Connection provided within 15 working days"
            ],
            "documents": ["Property tax receipt", "ID proof", "Address proof", "Property ownership documents"],
            "fees": {"15mm": 1500, "20mm": 2500, "25mm": 4000},
            "timeline": "15 working days",
            "contact": "044-28451300"
        },
        "property_tax_payment": {
            "title": "Pay Property Tax Online",
            "department": "gcc",
            "steps": [
                "Visit Chennai Corporation website",
                "Click on 'Online Services' → 'Property Tax'",
                "Enter Property Assessment Number or search by owner name",
                "Verify property details",
                "Select payment method (Net Banking/Card/UPI)",
                "Make payment and download receipt"
            ],
            "documents": ["Property Assessment Number", "Mobile number for OTP"],
            "fees": "As per assessment",
            "timeline": "Immediate",
            "contact": "1913"
        },
        "street_light_repair": {
            "title": "Report Street Light Not Working",
            "department": "gcc",
            "steps": [
                "Call Chennai Corporation helpline: 1913",
                "Provide exact location details",
                "Note complaint reference number",
                "Track status online or via phone",
                "Follow up if not resolved in 3 days"
            ],
            "documents": ["Location details"],
            "fees": "Free",
            "timeline": "3-5 working days",
            "contact": "1913"
        },
        "birth_certificate": {
            "title": "Apply for Birth Certificate",
            "department": "gcc", 
            "steps": [
                "Visit Chennai Corporation citizen portal",
                "Fill online application with child details",
                "Upload hospital birth certificate",
                "Upload parents' ID proofs",
                "Pay online fees ₹15",
                "Download certificate or collect from office"
            ],
            "documents": ["Hospital birth certificate", "Parents' ID proof", "Address proof"],
            "fees": 15,
            "timeline": "Immediate (online) or 3 days (office)",
            "contact": "044-25384680"
        }
    },
    "relationships": [
        {"from": "no_water", "to": "cmwssb", "type": "handled_by"},
        {"from": "water_contamination", "to": "cmwssb", "type": "handled_by"},
        {"from": "pipeline_leak", "to": "cmwssb", "type": "handled_by"},
        {"from": "sewage_overflow", "to": "cmwssb", "type": "handled_by"},
        {"from": "blocked_drain", "to": "cmwssb", "type": "handled_by"},
        {"from": "garbage_not_collected", "to": "gcc", "type": "handled_by"},
        {"from": "street_light_not_working", "to": "gcc", "type": "handled_by"},
        {"from": "pothole", "to": "gcc", "type": "handled_by"},
        {"from": "power_cut", "to": "tneb", "type": "handled_by"},
        {"from": "water_supply", "to": "water_connection_new", "type": "procedure"},
        {"from": "property_tax", "to": "property_tax_payment", "type": "procedure"},
        {"from": "street_lights", "to": "street_light_repair", "type": "procedure"},
        {"from": "birth_cert", "to": "birth_certificate", "type": "procedure"}
    ]
}

with open('CivicMindAI/data/civic_knowledge.json', 'w') as f:
    json.dump(civic_knowledge, f, indent=2)

print("✅ Civic knowledge graph data created successfully!")
print(f"Knowledge base contains:")
print(f"  • {len(civic_knowledge['entities']['departments'])} departments")
print(f"  • {len(civic_knowledge['entities']['services'])} services") 
print(f"  • {len(civic_knowledge['entities']['issues'])} common issues")
print(f"  • {len(civic_knowledge['procedures'])} detailed procedures")
print(f"  • {len(civic_knowledge['relationships'])} entity relationships")