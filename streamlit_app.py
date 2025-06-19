import streamlit as st
import json
import base64
import os
import difflib
from datetime import datetime
from utils.render import render_resume
from streamlit_ace import st_ace

# --- Page Setup ---
st.set_page_config(page_title="📄 Resume Builder", layout="wide")
st.markdown("# 📄 Resume Editor")

# --- Sidebar options ---
resume_type = st.sidebar.selectbox("Resume Type", ["Main", "Data Analyst"])
with_publication = st.sidebar.checkbox("Include Publications", value=False)

# --- Path Construction ---
variant_folder = resume_type.lower().replace(" ", "_")
suffix = "_with_publication" if with_publication else ""

DATA_PATH = os.path.join("resume_data", variant_folder, f"resume_data{suffix}.json")
TEMPLATE_PATH = os.path.join("template", f"resume_template{suffix}.tex") if with_publication else os.path.join("template", "resume_template.tex")
OUTPUT_DIR = os.path.join("output", f"{variant_folder}{suffix}")
PDF_PATH = os.path.join(OUTPUT_DIR, "Aryan_Jain_Resume.pdf")

LOG_DIR = os.path.join("logs", f"{variant_folder}{suffix}")
LOG_FILE = os.path.join(LOG_DIR, "change_log.txt")

# --- Ensure necessary directories exist ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- Tabs for Editor and Log Viewer ---
tab1, tab2 = st.tabs(["📝 Edit Resume", "📜 View Change Logs"])

with tab1:
    # --- Load current JSON into session ---
    if "last_selection" not in st.session_state or st.session_state.last_selection != DATA_PATH:
        try:
            with open(DATA_PATH, "r") as f:
                resume_data = json.load(f)
            st.session_state.editor_content = json.dumps(resume_data, indent=2)
            st.session_state.last_selection = DATA_PATH
        except Exception as e:
            st.error(f"Error loading resume data: {e}")
            st.stop()

    # --- Layout: Editor and PDF Preview ---
    left, right = st.columns([1.3, 2])

    with left:
        st.markdown("### 📝 JSON Editor")

        updated_code = st_ace(
            value=st.session_state.editor_content,
            language="json",
            theme="chrome",
            height=800,
            key=f"editor_{variant_folder}_{'pub' if with_publication else 'no_pub'}"
        )

        if updated_code and updated_code != st.session_state.editor_content:
            st.session_state.editor_content = updated_code

        if st.button("🚀 Generate PDF"):
            try:
                parsed = json.loads(st.session_state.editor_content)

                # Load old JSON
                old_json = {}
                if os.path.exists(DATA_PATH):
                    with open(DATA_PATH, "r") as f:
                        old_json = json.load(f)

                # Save new JSON
                with open(DATA_PATH, "w") as f:
                    json.dump(parsed, f, indent=2)

                # Generate PDF
                render_resume(DATA_PATH, TEMPLATE_PATH, OUTPUT_DIR)

                # Create change log (only diff)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                old_text = json.dumps(old_json, indent=2).splitlines()
                new_text = json.dumps(parsed, indent=2).splitlines()
                diff = "\n".join(
                    difflib.unified_diff(old_text, new_text, fromfile="old", tofile="new", lineterm="")
                ).strip()

                if diff:
                    with open(LOG_FILE, "a") as log:
                        log.write(f"\n\n--- {timestamp} ---\n")
                        log.write(f"Variant: {variant_folder}, Publication: {'Yes' if with_publication else 'No'}\n")
                        log.write("Changes:\n" + diff + "\n")

                st.success("✅ PDF and change log saved successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    with right:
        st.markdown("### 📄 PDF Preview")

        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            st.download_button(
                "📥 Download PDF",
                open(PDF_PATH, "rb"),
                file_name=f"Aryan_Jain_Resume.pdf",
                mime="application/pdf"
            )
        else:
            st.info("No PDF generated yet.")

with tab2:
    st.markdown("### 📜 Change Log Viewer")

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log:
            full_log = log.read().strip()

        # Split logs by timestamp marker
        log_entries = full_log.split("\n\n--- ")
        log_entries = [entry if entry.startswith("--- ") else "--- " + entry for entry in log_entries if entry.strip()]
        sorted_logs = "\n\n".join(reversed(log_entries))

        if sorted_logs:
            st.code(sorted_logs, language="diff")
        else:
            st.info("Log file is empty.")
    else:
        st.info("No log file found for this resume variant.")

