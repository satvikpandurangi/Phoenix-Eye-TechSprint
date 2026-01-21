# 🔧 Phoenix-Eye: The AI Hardware Surgeon
### *TechSprint Belgaum 2025 Submission*

**Phoenix-Eye** is a multimodal AI Agent designed to solve the global E-Waste crisis. It acts as a "Doctor" for broken electronics, using Google Gemini 1.5 to visually diagnose circuit faults and automatically regenerate lost legacy code to bring dead hardware back to life.

---

## 🚨 The Problem
* **50 Million Tons** of E-waste are generated annually.
* Valuable lab equipment and student projects are discarded due to minor physical faults (cold solder, burnt components) or lost source code.
* Most students lack the expertise to troubleshoot complex hardware failures.

## 💡 The Solution
Phoenix-Eye bridges the gap between physical hardware and digital logic:
1.  **Visual Diagnosis (The Eye):** Users upload an image of a broken PCB. The AI identifies damaged components (burnt resistors, broken traces) in real-time.
2.  **Code Resurrection (The Brain):** If the hardware is functional but the code is lost, the AI identifies the microcontroller (e.g., ESP32, Arduino) and auto-generates optimized C++ code to restore functionality.
3.  **Sustainability Tracking:** Calculates the estimated "Carbon Footprint Saved" for every successful repair.

---

## 🌟 Key Features
* **🩺 AI Visual Inspection:** Instantly detects burn marks, corrosion, and missing parts using Gemini Vision.
* **💻 Auto-Coding:** Generates ready-to-flash Arduino/C++ code based on component identification.
* **⚡ Real-Time Analysis:** Powered by Gemini 1.5 Flash for low-latency responses.
* **🌍 Eco-Impact Score:** Gamifies repair by showing environmental impact data.

---

## 🛠️ Tech Stack
* **AI Engine:** Google Gemini 1.5 Flash (Multimodal) & Vertex AI
* **Frontend:** Stream
