# Create civic_cache.json with Chennai civic information
civic_cache = {
    "emergency_contacts": {
        "fire": "101",
        "police": "100", 
        "ambulance": "108",
        "chennai_corporation": "1913",
        "cmwssb_complaint": "044-45674567",
        "electricity_complaint": "044-25675765",
        "gas_leak": "1906",
        "women_helpline": "1091",
        "child_helpline": "1098",
        "disaster_management": "108",
        "flood_helpline": "1913"
    },
    "government_contacts": {
        "collector_office": "044-28520314",
        "mayor_office": "044-25384681",
        "district_collector": "044-25620314",
        "cm_cell": "044-25675765",
        "tn_police_control": "044-28447095"
    },
    "civic_services_helplines": {
        "property_tax": "1913",
        "water_tax": "044-28451300",
        "birth_certificate": "044-25384680",
        "death_certificate": "044-25384680", 
        "trade_license": "044-25384689",
        "building_permit": "044-25384690",
        "marriage_registration": "044-25384685"
    },
    "zone_contacts": {
        "zone_1_north": "044-28451300 Ext.233",
        "zone_2_north_east": "044-28451300 Ext.213",
        "zone_3_central": "044-28451300 Ext.212",
        "zone_4_south_west": "044-28451300 Ext.386",
        "zone_5_south": "044-28451300 Ext.211",
        "zone_6_adyar": "044-24912345",
        "zone_7_anna_nagar": "044-26152345",
        "zone_8_teynampet": "044-24332345"
    },
    "quick_info": {
        "corporation_office_hours": "9:30 AM to 5:30 PM (Monday to Friday)",
        "emergency_services": "24x7 Available",
        "water_supply_timings": "6 AM to 8 AM and 6 PM to 8 PM",
        "garbage_collection": "Daily 6 AM to 10 AM",
        "property_tax_due_date": "31st March every year",
        "water_tax_frequency": "Bi-monthly",
        "corporation_website": "https://chennaicorporation.gov.in",
        "cmwssb_website": "https://cmwssb.tn.gov.in"
    }
}

with open('CivicMindAI/data/civic_cache.json', 'w') as f:
    json.dump(civic_cache, f, indent=2)

print("✅ Civic cache data created successfully!")
print(f"Cache contains {len(civic_cache)} main categories:")
for category in civic_cache.keys():
    print(f"  • {category.replace('_', ' ').title()}")
    print(f"    - {len(civic_cache[category])} entries")