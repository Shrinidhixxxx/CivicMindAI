import os
import json
import networkx as nx

# Create the project directory structure
project_structure = {
    'CivicMindAI': {
        'data': {
            'civic_docs': {},
            'civic_knowledge.json': {},
            'civic_cache.json': {}
        },
        'main.py': {},
        'agent_controller.py': {},
        'rag_module.py': {},
        'kag_module.py': {},
        'cag_module.py': {},
        'slm_module.py': {},
        'requirements.txt': {}
    }
}

def create_directory_structure(base_path, structure):
    """Create directory structure recursively"""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict) and content:
            # It's a directory with content
            os.makedirs(path, exist_ok=True)
            create_directory_structure(path, content)
        elif isinstance(content, dict) and not content:
            # It's an empty file
            if not name.endswith('/'):
                with open(path, 'w') as f:
                    f.write('')
        else:
            # It's a directory
            os.makedirs(path, exist_ok=True)

# Create the project structure
create_directory_structure('.', project_structure)

print("✅ Project directory structure created successfully!")
print("\nProject Structure:")
print("CivicMindAI/")
print("├── main.py                 # Streamlit UI")
print("├── agent_controller.py     # Routing logic")
print("├── rag_module.py           # Retrieval pipeline")
print("├── kag_module.py           # Knowledge Graph logic")
print("├── cag_module.py           # Cache handler")
print("├── slm_module.py           # Language model interface")
print("├── data/")
print("│   ├── civic_docs/         # Sample civic documents")
print("│   ├── civic_knowledge.json")
print("│   ├── civic_cache.json")
print("└── requirements.txt")