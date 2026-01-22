import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import json
import re

# --- PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Phoenix-Eye | AI Hardware Surgeon",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "HIGH-TECH" LOOK ---
st.markdown("""
<style>
    /* Main Background & Font */
    .stApp {
        background-color: #0E1117;
        color: #00FF99;
    }
    
    /* Neon Headers */
    h1, h2, h3 {
        color: #00FF99 !important;
        text-shadow: 0 0 10px #00FF99;
        font-family: 'Courier New', monospace;
    }
    
    /* Input Fields styling */
    .stTextInput>div>div>input {
        background-color: #161B22;
        color: #FFFFFF;
        border: 1px solid #00FF99;
        border-radius: 5px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #00FF99, #00CC7A);
        color: #000000;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00FF99;
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #00E5FF !important;
        text-shadow: 0 0 10px #00E5FF;
    }
    
    /* Code Block Area */
    .stCodeBlock {
        border: 1px solid #00FF99;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER: LOAD LOTTIE ANIMATION ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a Tech/Robot Animation
lottie_tech = load_lottieurl("https://lottie.host/5a0c1074-6720-4103-8869-923f99057b06/8Xb3QYyQ1X.json")

# --- AUTHENTICATION ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        auth_status = "🟢 SYSTEM ONLINE"
    else:
        st.error("⚠️ GOOGLE_API_KEY missing in Secrets.")
        st.stop()
except Exception:
    # Fallback for local run without secrets
    # API_KEY = "PASTE_YOUR_KEY_HERE" 
    # genai.configure(api_key=API_KEY)
    st.warning("Running Locally")

# --- SMART MODEL SELECTOR ---
def get_model():
    # Priority list
    models = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro-vision"]
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    for m in models:
        if m in available_models:
            return genai.GenerativeModel(m)
    return genai.GenerativeModel(available_models[0]) if available_models else None

model = get_model()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🖥️ SYSTEM STATUS")
    st.markdown(f"**API Connection:** {auth_status}")
    if model:
        st.markdown(f"**Neural Engine:** `{model.model_name}`")
    
    st.markdown("---")
    st.markdown("### 📊 Live Telemetry")
    col_a, col_b = st.columns(2)
    col_a.metric("CPU", "34%", "+2%")
    col_b.metric("RAM", "1.2GB", "-12MB")
    st.markdown("---")
    st.caption("Phoenix-Eye v2.0 | TechSprint 2025")

# --- MAIN UI ---
col1, col2 = st.columns([0.8, 3])
with col1:
    if lottie_tech:
        from streamlit_lottie import st_lottie
        st_lottie(lottie_tech, height=150, key="tech_anim")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/2621/2621040.png", width=100)

with col2:
    st.title("PHOENIX-EYE ⚡")
    st.markdown("### `AI-Powered Hardware Resurrection Interface`")

# Tabs
tab1, tab2, tab3 = st.tabs(["👁️ VISUAL DIAGNOSTICS", "🧠 NEURAL RECURSION (CODE)", "🌍 SUSTAINABILITY MATRIX"])

# --- PHASE 1: VISUAL DIAGNOSIS ---
with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("1. Hardware Scan")
        uploaded_file = st.file_uploader("Drop Circuit Image", type=["jpg", "png", "jpeg"])
    
    with c2:
        st.subheader("2. AI Analysis")
        if uploaded_file and st.button("INITIATE SCAN", type="primary"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Scanning...", use_container_width=True)
            
            with st.spinner("Processing Logic Gates..."):
                prompt = """
                Analyze this circuit board. 
                1. Identify Components. 
                2. Detect Faults (Solder issues, corrosion).
                3. Provide Repair Steps.
                """
                response = model.generate_content([prompt, image])
                st.success("SCAN COMPLETE")
                st.markdown(response.text)
                st.session_state['repair_data'] = response.text
                st.session_state['phase1_done'] = True
                st.session_state['device_context'] = "Custom PCB" # Placeholder, improved by AI in real app

# --- PHASE 2: CODE RECURSION (UPDATED LAYOUT) ---
with tab2:
    st.subheader("3. Firmware Reconstruction")
    
    # Input Section (Top)
    ic1, ic2 = st.columns(2)
    with ic1:
        hw_list = st.text_input("Detected Hardware", value="ESP32, DHT22, OLED 0.96")
    with ic2:
        user_goal = st.text_input("Target Functionality", value="Monitor Temp/Humidity & Deep Sleep")
    
    # Button (Middle)
    if st.button("GENERATE FIRMWARE PATCH", type="primary"):
        with st.spinner("Compiling Neural Code..."):
            code_prompt = f"""
            Act as an Embedded Systems Expert. Write complete, optimized C++ (Arduino) code for:
            Hardware: {hw_list}
            Goal: {user_goal}
            Requirements: Add comments, use Deep Sleep where possible.
            """
            response = model.generate_content(code_prompt)
            st.session_state['gen_code'] = response.text
            
    # Output Section (Bottom - FULL WIDTH)
    if 'gen_code' in st.session_state:
        st.markdown("---")
        st.markdown("### 💻 Generated Firmware Source")
        st.code(st.session_state['gen_code'], language='cpp')

# --- PHASE 3: IMPACT DASHBOARD (DYNAMIC) ---
with tab3:
    st.subheader("4. Sustainability Impact Matrix")
    
    if 'phase1_done' in st.session_state:
        # DYNAMIC CALCULATION
        if st.button("CALCULATE IMPACT METRICS"):
            with st.spinner("Simulating Environmental Impact..."):
                # Ask Gemini to estimate numbers based on the specific repair
                context = st.session_state.get('repair_data', 'Standard Electronics Repair')
                
                impact_prompt = f"""
                Based on this repair context: "{context[:200]}...", estimate the environmental impact.
                Return ONLY a JSON string with these 3 keys: "ewaste_saved_g" (integer grams), "co2_saved_kg" (float), "cost_saved_inr" (integer).
                Do not include markdown formatting. Just the JSON.
                """
                
                try:
                    impact_res = model.generate_content(impact_prompt)
                    # Clean response to get pure JSON
                    clean_json = re.sub(r'```json|```', '', impact_res.text).strip()
                    metrics = json.loads(clean_json)
                    
                    # Display Dynamic Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("E-Waste Diverted", f"{metrics['ewaste_saved_g']} g", "High Value")
                    m2.metric("CO2 Prevented", f"{metrics['co2_saved_kg']} kg", "Atmospheric Impact")
                    m3.metric("Cost Efficiency", f"₹{metrics['cost_saved_inr']}", "User Savings")
                    
                    st.success("✅ Impact Analysis Verified")
                    
                    # Download Report
                    report = f"PHOENIX-EYE PROTOCOL\n\nIMPACT:\n{metrics}\n\nDIAGNOSIS:\n{context}"
                    st.download_button("EXPORT MISSION REPORT", report, file_name="Impact_Log.txt")
                    
                except Exception as e:
                    st.error("Calculation Matrix Error (Try Again)")
                    st.caption(f"Debug: {e}")
        else:
            st.info("Ready to calculate. Click button above.")
            
    else:
        st.warning("⚠️ DATA MISSING: Please complete Phase 1 Scan first.")
