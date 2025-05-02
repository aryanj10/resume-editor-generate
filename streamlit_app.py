import streamlit as st
import json
import os
import shutil
from utils.render import render_resume
from streamlit_ace import st_ace

# Constants
DATA_PATH = "resume_data/resume_data.json"
TEMPLATE_PATH = "template/resume_template.tex"
OUTPUT_DIR = "output"
PDF_PATH = os.path.join(OUTPUT_DIR, "resume.pdf")
STATIC_PDF_PATH = "static/resume.pdf"  # public path for Streamlit app

st.set_page_config(page_title="📄 Resume Builder", layout="wide")
st.markdown("# 📄 Resume Editor")

# Load resume data
with open(DATA_PATH, "r") as f:
    resume_data = json.load(f)

# Layout: side-by-side
left, right = st.columns([1.3, 2])

# Left: JSON editor
with left:
    st.markdown("### 📝 JSON Editor")
    json_code = st_ace(
        value=json.dumps(resume_data, indent=2),
        language="json",
        theme="chrome",
        height=800,
        key="editor"
    )
    if st.button("🚀 Generate PDF"):
        try:
            parsed = json.loads(json_code)
            with open(DATA_PATH, "w") as f:
                json.dump(parsed, f, indent=2)

            render_resume(DATA_PATH, TEMPLATE_PATH, OUTPUT_DIR)

            # Copy to static folder for external preview
            os.makedirs("static", exist_ok=True)
            shutil.copy(PDF_PATH, STATIC_PDF_PATH)

            st.success("✅ PDF generated successfully.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Right: PDF preview
with right:
    st.markdown("### 📄 PDF Preview")
    if os.path.exists(STATIC_PDF_PATH):
        st.markdown("[📄 Click to View Resume PDF](static/resume.pdf)", unsafe_allow_html=True)
        st.download_button("📥 Download PDF", open(STATIC_PDF_PATH, "rb"), file_name="Aryan_Jain_Resume.pdf", mime="application/pdf")
    else:
        st.info("No PDF generated yet.")
