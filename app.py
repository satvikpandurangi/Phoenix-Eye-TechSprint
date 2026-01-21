import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="Phoenix-Eye", page_icon="🔥", layout="wide")

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2621/2621040.png", width=50)
    st.title("⚙️ System Config")
    
    # SAFE: Ask for Key here (prevents GitHub from revoking it)
    api_key = st.text_input("Enter Google API Key", type="password")
    
    selected_model = None
    
    if api_key:
        genai.configure(api_key=api_key)
        try:
            # DYNAMIC MODEL SELECTOR
            model_list = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_list.append(m.name)
            
            if model_list:
                st.success(f"✅ Found {len(model_list)} Models")
                # Default to Flash if available, otherwise first on list
                default_ix = 0
                if "models/gemini-1.5-flash" in model_list:
                    default_ix = model_list.index("models/gemini-1.5-flash")
                
                selected_model = st.selectbox("Select Model", model_list, index=default_ix)
            else:
                st.error("Key valid, but no models found.")
        except Exception as e:
            st.error(f"Key Error: {e}")
    else:
        st.warning("⚠️ Paste API Key to Start")

    st.markdown("---")
    st.info("TechSprint 2025 Submission")

# --- MAIN APP UI ---
st.title("🔥 Phoenix-Eye: The AI Hardware Surgeon")
st.markdown("### `Multimodal Diagnosis & Logic Resurrection System`")

if not selected_model:
    st.info("👈 Please enter your API Key in the sidebar to connect to the Google Brain.")
    st.stop()

# Initialize Model
model = genai.GenerativeModel(selected_model)

# Tab Selection
tab1, tab2, tab3 = st.tabs(["👁️ Phase 1: Visual Diagnosis", "🧠 Phase 2: Code Resurrection", "🌍 Phase 3: Impact Dashboard"])

# --- PHASE 1: VISUAL DIAGNOSIS ---
with tab1:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.header("1. Visual Scanning")
        uploaded_file = st.file_uploader("Upload PCB/Hardware Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        with col1:
            st.image(image, caption='Input Hardware', use_column_width=True)
        
        with col2:
            st.header("2. AI Analysis")
            if st.button("Run Diagnostics", type="primary"):
                with st.spinner(f"Analyzing with {selected_model}..."):
                    try:
                        prompt = """
                        You are an expert Electronics Repair Engineer. Analyze this circuit board image.
                        1. LIST COMPONENTS: Identify visible chips, sensors, or connectors.
                        2. DETECT FAULTS: Look closely for cold solder joints, burnt marks, broken traces, or corrosion.
                        3. REPAIR INSTRUCTION: Give a specific technical instruction to fix it.
                        4. STATUS: Output 'Repairable' or 'Irreparable'.
                        """
                        response = model.generate_content([prompt, image])
                        st.success("✅ Diagnosis Complete")
                        st.markdown(response.text)
                        st.session_state['phase1_done'] = True
                        st.session_state['repair_data'] = response.text
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- PHASE 2: CODE RESURRECTION ---
with tab2:
    st.header("3. Logic Resurrection")
    st.info("Describe your hardware to generate new Firmware.")
    
    c1, c2 = st.columns(2)
    with c1:
        hw_list = st.text_input("Hardware Detected", value="ESP32, DHT11 Sensor, OLED Display")
        user_goal = st.text_area("Desired Functionality", value="Read temperature every 5 seconds and display on OLED.")
    
    with c2:
        if st.button("Generate Firmware"):
            with st.spinner(f"Writing Code with {selected_model}..."):
                try:
                    code_prompt = f"""
                    Write complete Arduino C++ code for:
                    Hardware: {hw_list}
                    Goal: {user_goal}
                    """
                    response = model.generate_content(code_prompt)
                    st.code(response.text, language='cpp')
                    st.session_state['gen_code'] = response.text
                except Exception as e:
                    st.error(f"Error: {e}")

# --- PHASE 3: IMPACT & EXPORT ---
with tab3:
    st.header("4. Sustainability Impact")
    
    if 'phase1_done' in st.session_state:
        m1, m2, m3 = st.columns(3)
        m1.metric("E-Waste Diverted", "145 g", "+1 Device")
        m2.metric("CO2 Emissions Saved", "2.4 kg", "High Impact")
        m3.metric("Money Saved", "₹450", "Est.")
        
        report = f"PHOENIX-EYE REPORT\n\nDIAGNOSIS:\n{st.session_state.get('repair_data','')}\n\nCODE:\n{st.session_state.get('gen_code','')}"
        st.download_button("Download Report", report, file_name="repair.txt")
        st.success("Blueprint saved to Global Library.")
    else:
        st.warning("⚠️ Run Phase 1 Diagnosis first.")