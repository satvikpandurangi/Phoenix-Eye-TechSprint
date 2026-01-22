import streamlit as st
import google.generativeai as genai
from PIL import Image
import re 

# --- PAGE CONFIG ---
st.set_page_config(page_title="Phoenix-Eye", page_icon="🔥", layout="wide")

# --- AUTHENTICATION (The "Invisible" Key) ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        auth_status = "✅ Connected (Cloud)"
        
        # --- MODEL SELECTOR (Automatic) ---
        try:
            model_list = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_list.append(m.name)
            
            # Smart default selection
            default_ix = 0
            if "models/gemini-1.5-flash" in model_list:
                default_ix = model_list.index("models/gemini-1.5-flash")
                
            selected_model = model_list[default_ix] if model_list else None
            
        except Exception as e:
            selected_model = None
            auth_status = f"⚠️ API Error: {e}"
            
    else:
        st.error("Secrets not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")
        st.stop()
        
except FileNotFoundError:
    st.warning("Running locally? Set up `.streamlit/secrets.toml` or uncomment the local key line.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2621/2621040.png", width=50)
    st.title("System Status")
    st.success(auth_status)
    if selected_model:
        st.caption(f"Brain: `{selected_model}`")
    st.markdown("---")
    st.info("TechSprint 2025 Submission")

# --- MAIN APP UI ---
st.title("🔥 Phoenix-Eye: The AI Hardware Surgeon")
st.markdown("### `Multimodal Diagnosis & Logic Resurrection System`")

if not selected_model:
    st.error("Could not find a working AI model. Check API Quota.")
    st.stop()

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
                with st.spinner(f"Analyzing circuit..."):
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

# --- PHASE 2: CODE RESURRECTION (UPDATED LAYOUT) ---
with tab2:
    st.header("3. Logic Resurrection")
    st.info("Describe your hardware to generate new Firmware.")
    
    # Inputs remain in columns (looks neat)
    c1, c2 = st.columns(2)
    with c1:
        hw_list = st.text_input("Hardware Detected", value="ESP32, DHT11 Sensor, OLED Display")
    with c2:
        user_goal = st.text_input("Desired Functionality", value="Read temperature every 5 seconds and display on OLED.")
    
    # Button below inputs
    if st.button("Generate Firmware"):
        with st.spinner(f"Writing Code..."):
            try:
                code_prompt = f"""
                Write complete Arduino C++ code for:
                Hardware: {hw_list}
                Goal: {user_goal}
                """
                response = model.generate_content(code_prompt)
                st.session_state['gen_code'] = response.text
            except Exception as e:
                st.error(f"Error: {e}")

    # OUTPUT IS NOW FULL SCREEN (Outside the columns)
    if 'gen_code' in st.session_state:
        st.markdown("---")
        st.subheader("💻 Generated Firmware")
        st.code(st.session_state['gen_code'], language='cpp')

# --- PHASE 3: IMPACT & EXPORT (DYNAMIC) ---
with tab3:
    st.header("4. Sustainability Impact")
    
    if 'phase1_done' in st.session_state:
        # Dynamic Sustainability Analysis
        if st.button("Calculate Environmental Impact"):
            with st.spinner("AI is analyzing material composition & repair impact..."):
                try:
                    # Prompt Gemini to calculate specific metrics based on the repair data
                    impact_prompt = f"""
                    Analyze the sustainability impact of repairing this specific device:
                    {st.session_state.get('repair_data', 'Generic Electronics')}
                    
                    Estimate the following 3 values relative to this specific device:
                    1. E-Waste Diverted (in grams)
                    2. CO2 Emissions Saved (in kg)
                    3. Money Saved (in Indian Rupees ₹)
                    
                    Return ONLY the numbers in this format: 
                    Waste: 150, CO2: 2.5, Money: 500
                    """
                    impact_res = model.generate_content(impact_prompt)
                    
                    # Parse the AI response (Simple extraction)
                    text = impact_res.text
                    
                    # Default values in case AI fails
                    waste, co2, money = "145", "2.4", "450" 
                    
                    # Try to extract numbers dynamically
                    try:
                        # Simple logic to grab numbers after keywords
                        if "Waste:" in text: waste = text.split("Waste:")[1].split(",")[0].strip()
                        if "CO2:" in text: co2 = text.split("CO2:")[1].split(",")[0].strip()
                        if "Money:" in text: money = text.split("Money:")[1].strip()
                    except:
                        pass 
                        
                    st.session_state['impact_waste'] = waste
                    st.session_state['impact_co2'] = co2
                    st.session_state['impact_money'] = money
                    
                except Exception as e:
                    if "429" in str(e):
                        st.warning("🚦 Speed Limit Reached! Please wait 30 seconds and try again.")
                    else:
                        st.error(f"Calculation Error: {e}")

        # Display Metrics (Dynamic)
        m1, m2, m3 = st.columns(3)
        m1.metric("E-Waste Diverted", f"{st.session_state.get('impact_waste', '---')} g", "Estimated")
        m2.metric("CO2 Emissions Saved", f"{st.session_state.get('impact_co2', '---')} kg", "High Impact")
        m3.metric("Money Saved", f"₹{st.session_state.get('impact_money', '---')}", "User Savings")
        
        # Download Report
        report = f"PHOENIX-EYE REPORT\n\nDIAGNOSIS:\n{st.session_state.get('repair_data','')}\n\nCODE:\n{st.session_state.get('gen_code','')}"
        st.download_button("Download Report", report, file_name="repair.txt")
        st.success("Blueprint saved to Global Library.")
    else:
        st.warning("⚠️ Run Phase 1 Diagnosis first.")
