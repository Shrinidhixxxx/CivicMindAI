# Create requirements.txt
requirements_content = """# CivicMindAI Requirements
streamlit>=1.28.0
langchain>=0.0.340
langchain-openai>=0.0.2
faiss-cpu>=1.7.4
chromadb>=0.4.15
networkx>=3.2.1
openai>=1.3.0
sentence-transformers>=2.2.2
pandas>=2.1.0
numpy>=1.24.0
gtts>=2.4.0
speechrecognition>=3.10.0
python-dotenv>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
"""

with open('CivicMindAI/requirements.txt', 'w') as f:
    f.write(requirements_content)

print("✅ Requirements.txt created successfully!")
print("\nDependencies included:")
for line in requirements_content.strip().split('\n'):
    if line and not line.startswith('#'):
        print(f"  • {line}")