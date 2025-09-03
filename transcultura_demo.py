import streamlit as st
import requests
import json
import time
from datetime import datetime
import chromadb
from chromadb.config import Settings
import pandas as pd
import uuid

# Initialize ChromaDB
@st.cache_resource
def init_chromadb():
    client = chromadb.PersistentClient(path="./transcultura_db")
    
    # Cultural Guidelines Collection
    cultural_collection = client.get_or_create_collection(
        name="cultural_guidelines",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Compliance Rules Collection
    compliance_collection = client.get_or_create_collection(
        name="compliance_rules",
        metadata={"hnsw:space": "cosine"}
    )
    
    return client, cultural_collection, compliance_collection

# Ollama API functions
def call_ollama(prompt, model="llama3.2:3b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Connection error: {str(e)}"

# Agent Classes
class ContentTranslationAgent:
    def __init__(self):
        self.name = "Content Translation Agent"
    
    def translate(self, content, target_language):
        prompt = f"""
        You are a professional marketing translator. Translate the following marketing content to {target_language}.
        Maintain the marketing tone, emotional impact, and call-to-action effectiveness.
        
        Original content: {content}
        
        Provide only the translation, no explanations.
        """
        return call_ollama(prompt)

class CulturalAdaptationAgent:
    def __init__(self, cultural_collection):
        self.name = "Cultural Adaptation Agent"
        self.cultural_collection = cultural_collection
    
    def adapt_content(self, content, target_region):
        # Query cultural guidelines
        cultural_context = self._get_cultural_context(target_region)
        
        prompt = f"""
        You are a cultural adaptation expert. Adapt the following marketing content for {target_region}.
        
        Cultural Guidelines for {target_region}:
        {cultural_context}
        
        Original content: {content}
        
        Adapt the content considering:
        1. Cultural values and sensitivities
        2. Local preferences and customs
        3. Communication style
        4. Visual and messaging tone
        
        Provide the adapted content with brief explanation of changes made.
        """
        return call_ollama(prompt)
    
    def _get_cultural_context(self, region):
        # Sample cultural guidelines - in real implementation, this would query ChromaDB
        guidelines = {
            "Japan": "Emphasize quality, respect, harmony. Avoid direct confrontation. Use formal language.",
            "Brazil": "Warm, family-oriented messaging. Vibrant colors. Personal relationships matter.",
            "Germany": "Factual, precise information. Quality and efficiency focus. Conservative approach.",
            "India": "Value-conscious messaging. Family and community focus. Respectful of traditions.",
        }
        return guidelines.get(region, "General international guidelines apply.")

class ComplianceRegulatoryAgent:
    def __init__(self, compliance_collection):
        self.name = "Compliance & Regulatory Agent"
        self.compliance_collection = compliance_collection
    
    def check_compliance(self, content, target_region, industry="general"):
        compliance_rules = self._get_compliance_rules(target_region, industry)
        
        prompt = f"""
        You are a compliance expert. Review the following marketing content for {target_region} in {industry} industry.
        
        Compliance Rules for {target_region}:
        {compliance_rules}
        
        Content to review: {content}
        
        Analyze for:
        1. Legal compliance issues
        2. Advertising standards violations
        3. Industry-specific regulations
        4. Required disclaimers or warnings
        
        Provide: COMPLIANT/NON-COMPLIANT and explanation.
        """
        return call_ollama(prompt)
    
    def _get_compliance_rules(self, region, industry):
        rules = {
            "EU": "GDPR compliance required. Health claims need substantiation. Clear pricing display.",
            "USA": "FDA regulations for health products. FTC advertising guidelines. State-specific rules.",
            "Japan": "Pharmaceutical advertising restrictions. Comparison advertising limitations.",
            "India": "Foreign investment disclosure. Local language requirements in some states.",
        }
        return rules.get(region, "Standard international advertising guidelines.")

class ExceptionManagementAgent:
    def __init__(self):
        self.name = "Exception Management Agent"
    
    def flag_exceptions(self, translation_result, cultural_result, compliance_result):
        prompt = f"""
        You are an exception management system. Analyze the following results and determine if human review is needed.
        
        Translation Result: {translation_result}
        Cultural Adaptation Result: {cultural_result}
        Compliance Check Result: {compliance_result}
        
        Flag for human review if:
        1. Compliance issues detected
        2. Significant cultural adaptation needed
        3. Translation accuracy concerns
        4. Legal disclaimers required
        
        Provide: HUMAN_REVIEW_REQUIRED/AUTO_APPROVE and priority level (HIGH/MEDIUM/LOW) with reason.
        """
        return call_ollama(prompt)

# Initialize session state
if 'processed_campaigns' not in st.session_state:
    st.session_state.processed_campaigns = []

def main():
    st.set_page_config(page_title="TransCultura", page_icon="🌍", layout="wide")
    
    # Header
    st.title("🌍 TransCultura")
    st.markdown("### Autonomous Content Translation, Localization & Compliance for Global Digital Marketing")
    
    # Initialize ChromaDB
    client, cultural_collection, compliance_collection = init_chromadb()
    
    # Initialize agents
    translation_agent = ContentTranslationAgent()
    cultural_agent = CulturalAdaptationAgent(cultural_collection)
    compliance_agent = ComplianceRegulatoryAgent(compliance_collection)
    exception_agent = ExceptionManagementAgent()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Campaign Configuration")
        
        # Target market selection
        target_language = st.selectbox(
            "Target Language",
            ["Spanish", "French", "German", "Japanese", "Portuguese", "Hindi"]
        )
        
        target_region = st.selectbox(
            "Target Region",
            ["Spain", "France", "Germany", "Japan", "Brazil", "India"]
        )
        
        industry = st.selectbox(
            "Industry",
            ["Technology", "Healthcare", "Fashion", "Food & Beverage", "Finance", "General"]
        )
        
        st.header("Agent Status")
        st.success("🤖 Translation Agent: Ready")
        st.success("🎨 Cultural Adaptation Agent: Ready")
        st.success("⚖️ Compliance Agent: Ready")
        st.success("🚩 Exception Management Agent: Ready")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Original Campaign Content")
        
        # Sample campaigns
        sample_campaigns = {
            "Tech Product Launch": "Revolutionize your productivity with our AI-powered assistant! Get 50% off for early adopters. Limited time offer - Transform your workflow today!",
            "Health Supplement": "Boost your immunity naturally! Our vitamin complex provides 100% daily nutrients. Clinically tested formula. Order now and feel the difference!",
            "Fashion Sale": "Summer collection now 70% OFF! Trendy styles that make you stand out. Free shipping worldwide. Shop now before it's gone!",
            "Food Delivery": "Craving authentic cuisine? We deliver happiness to your doorstep! Order now and get your first meal free. Satisfaction guaranteed!"
        }
        
        campaign_type = st.selectbox("Choose Sample Campaign", list(sample_campaigns.keys()))
        
        content = st.text_area(
            "Marketing Content",
            value=sample_campaigns[campaign_type],
            height=100,
            help="Enter your marketing content to be translated and localized"
        )
        
        if st.button("🚀 Process Campaign", type="primary", use_container_width=True):
            if content:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Translation
                status_text.text("🔄 Translating content...")
                progress_bar.progress(25)
                
                with st.spinner("Translation in progress..."):
                    translation_result = translation_agent.translate(content, target_language)
                
                # Step 2: Cultural Adaptation
                status_text.text("🎨 Adapting for cultural context...")
                progress_bar.progress(50)
                
                with st.spinner("Cultural adaptation in progress..."):
                    cultural_result = cultural_agent.adapt_content(translation_result, target_region)
                
                # Step 3: Compliance Check
                status_text.text("⚖️ Checking compliance...")
                progress_bar.progress(75)
                
                with st.spinner("Compliance check in progress..."):
                    compliance_result = compliance_agent.check_compliance(cultural_result, target_region, industry.lower())
                
                # Step 4: Exception Management
                status_text.text("🚩 Analyzing for exceptions...")
                progress_bar.progress(100)
                
                with st.spinner("Exception analysis in progress..."):
                    exception_result = exception_agent.flag_exceptions(translation_result, cultural_result, compliance_result)
                
                status_text.text("✅ Processing complete!")
                
                # Store results
                campaign_result = {
                    'id': str(uuid.uuid4())[:8],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'original_content': content,
                    'target_language': target_language,
                    'target_region': target_region,
                    'industry': industry,
                    'translation': translation_result,
                    'cultural_adaptation': cultural_result,
                    'compliance_check': compliance_result,
                    'exception_analysis': exception_result
                }
                
                st.session_state.processed_campaigns.append(campaign_result)
            else:
                st.error("Please enter campaign content to process")
    
    with col2:
        st.header("📊 Processing Results")
        
        if st.session_state.processed_campaigns:
            latest_campaign = st.session_state.processed_campaigns[-1]
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🔤 Translation", "🎨 Cultural", "⚖️ Compliance", "🚩 Exception"])
            
            with tab1:
                st.subheader("Translation Results")
                st.info(f"**Target Language:** {latest_campaign['target_language']}")
                st.text_area("Translated Content", latest_campaign['translation'], height=100, disabled=True)
            
            with tab2:
                st.subheader("Cultural Adaptation")
                st.info(f"**Target Region:** {latest_campaign['target_region']}")
                st.text_area("Culturally Adapted Content", latest_campaign['cultural_adaptation'], height=150, disabled=True)
            
            with tab3:
                st.subheader("Compliance Check")
                st.info(f"**Industry:** {latest_campaign['industry']}")
                compliance_text = latest_campaign['compliance_check']
                if "NON-COMPLIANT" in compliance_text.upper():
                    st.error("⚠️ Compliance Issues Detected")
                else:
                    st.success("✅ Compliance Check Passed")
                st.text_area("Compliance Analysis", compliance_text, height=150, disabled=True)
            
            with tab4:
                st.subheader("Exception Management")
                exception_text = latest_campaign['exception_analysis']
                if "HUMAN_REVIEW_REQUIRED" in exception_text.upper():
                    if "HIGH" in exception_text.upper():
                        st.error("🔴 HIGH Priority - Human Review Required")
                    elif "MEDIUM" in exception_text.upper():
                        st.warning("🟡 MEDIUM Priority - Human Review Recommended")
                    else:
                        st.info("🟢 LOW Priority - Minor Review Needed")
                else:
                    st.success("✅ Auto-Approved - No Human Review Needed")
                st.text_area("Exception Analysis", exception_text, height=150, disabled=True)
        else:
            st.info("👆 Process a campaign to see results here")
    
    # Campaign History
    if st.session_state.processed_campaigns:
        st.header("📈 Campaign Processing History")
        
        # Create DataFrame for history
        history_data = []
        for campaign in st.session_state.processed_campaigns:
            # Determine status from exception analysis
            status = "Auto-Approved"
            if "HUMAN_REVIEW_REQUIRED" in campaign['exception_analysis'].upper():
                status = "Needs Review"
            elif "NON-COMPLIANT" in campaign['compliance_check'].upper():
                status = "Compliance Issue"
            
            history_data.append({
                'Campaign ID': campaign['id'],
                'Timestamp': campaign['timestamp'],
                'Target': f"{campaign['target_language']} / {campaign['target_region']}",
                'Industry': campaign['industry'],
                'Status': status
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Campaigns", len(st.session_state.processed_campaigns))
        
        with col2:
            auto_approved = sum(1 for c in st.session_state.processed_campaigns 
                              if "AUTO_APPROVE" in c['exception_analysis'].upper())
            st.metric("Auto-Approved", auto_approved)
        
        with col3:
            needs_review = len(st.session_state.processed_campaigns) - auto_approved
            st.metric("Needs Review", needs_review)
        
        with col4:
            if st.session_state.processed_campaigns:
                automation_rate = (auto_approved / len(st.session_state.processed_campaigns)) * 100
                st.metric("Automation Rate", f"{automation_rate:.1f}%")

    # Footer
    st.markdown("---")
    st.markdown("🚀 **TransCultura Demo** - Powered by Ollama & Llama3.2:3b | Built for Gen AI Hackathon")

if __name__ == "__main__":
    main()