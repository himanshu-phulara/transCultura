import chromadb
from chromadb.config import Settings

def initialize_knowledge_base():
    """Initialize ChromaDB with sample cultural and compliance data"""
    
    client = chromadb.PersistentClient(path="./transcultura_db")
    
    # Cultural Guidelines Collection
    cultural_collection = client.get_or_create_collection(
        name="cultural_guidelines",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Sample cultural guidelines
    cultural_data = [
        {
            "id": "japan_general",
            "region": "Japan",
            "content": "Japanese culture values respect, harmony, and indirect communication. Marketing should emphasize quality, craftsmanship, and long-term relationships. Avoid aggressive sales tactics.",
            "guidelines": ["Use formal language", "Emphasize quality over price", "Show respect for tradition", "Avoid direct confrontation"]
        },
        {
            "id": "brazil_general", 
            "region": "Brazil",
            "content": "Brazilian culture is warm, family-oriented, and relationship-focused. Marketing should be vibrant, personal, and emphasize community values. Color and emotion are important.",
            "guidelines": ["Use warm, personal tone", "Emphasize family values", "Use vibrant colors", "Show social connections"]
        },
        {
            "id": "germany_general",
            "region": "Germany", 
            "content": "German culture values precision, efficiency, and factual information. Marketing should be straightforward, detailed, and focus on product benefits and quality.",
            "guidelines": ["Provide detailed information", "Be direct and honest", "Emphasize quality and efficiency", "Use conservative design"]
        },
        {
            "id": "india_general",
            "region": "India",
            "content": "Indian culture is diverse, value-conscious, and family-oriented. Marketing should respect cultural traditions, emphasize value for money, and consider regional differences.",
            "guidelines": ["Show respect for traditions", "Emphasize value proposition", "Consider regional diversity", "Include family contexts"]
        }
    ]
    
    # Add cultural data to collection
    for data in cultural_data:
        cultural_collection.add(
            ids=[data["id"]],
            documents=[data["content"]],
            metadatas=[{"region": data["region"], "type": "cultural_guideline"}]
        )
    
    # Compliance Rules Collection
    compliance_collection = client.get_or_create_collection(
        name="compliance_rules",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Sample compliance rules
    compliance_data = [
        {
            "id": "eu_gdpr",
            "region": "EU",
            "content": "GDPR compliance required for data collection. Must include clear privacy policy links, explicit consent mechanisms, and right to data deletion options.",
            "industry": "general"
        },
        {
            "id": "usa_health",
            "region": "USA",
            "content": "FDA regulations apply to health claims. Cannot make unsubstantiated medical claims. Dietary supplements require disclaimers. FTC truth in advertising standards apply.",
            "industry": "healthcare"
        },
        {
            "id": "japan_pharma",
            "region": "Japan",
            "content": "Pharmaceutical advertising strictly regulated. Cannot show before/after comparisons. Medical claims require approval. Comparison advertising limited.",
            "industry": "healthcare"
        },
        {
            "id": "india_foreign",
            "region": "India",
            "content": "Foreign investment disclosures required. Local language requirements in some states. Cultural sensitivity important for religious content.",
            "industry": "general"
        }
    ]
    
    # Add compliance data to collection
    for data in compliance_data:
        compliance_collection.add(
            ids=[data["id"]], 
            documents=[data["content"]],
            metadatas=[{"region": data["region"], "industry": data["industry"]}]
        )
    
    print("✅ Knowledge base initialized with cultural and compliance data")
    print(f"📊 Cultural guidelines: {len(cultural_data)} entries")
    print(f"📊 Compliance rules: {len(compliance_data)} entries")

if __name__ == "__main__":
    initialize_knowledge_base()