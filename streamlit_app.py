import streamlit as st
import json
import base64
import os
from utils.render import render_resume
from streamlit_ace import st_ace

st.set_page_config(page_title="📄 Resume Builder", layout="wide")
st.markdown("# 📄 Resume Editor")

# Sidebar
resume_type = st.sidebar.selectbox("Resume Type", ["Main", "Data Analyst"])
with_publication = st.sidebar.checkbox("Include Publications", value=False)

# Slugify folder names
variant_folder = resume_type.lower().replace(" ", "_")
suffix = "_with_publication" if with_publication else ""

# Define file paths
DATA_PATH = os.path.join("resume_data", variant_folder, f"resume_data{suffix}.json")
TEMPLATE_PATH = os.path.join("template", f"resume_template{suffix}.tex") if with_publication else os.path.join("template", "resume_template.tex")
OUTPUT_DIR = os.path.join("output", f"{variant_folder}{suffix}")
PDF_PATH = os.path.join(OUTPUT_DIR, "Aryan_Jain_Resume.pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load JSON into session_state if new selection
if "last_selection" not in st.session_state or st.session_state.last_selection != DATA_PATH:
    try:
        with open(DATA_PATH, "r") as f:
            resume_data = json.load(f)
        st.session_state.editor_content = json.dumps(resume_data, indent=2)
        st.session_state.last_selection = DATA_PATH
    except Exception as e:
        st.error(f"Error loading resume data: {e}")
        st.stop()

# Layout: editor + preview
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

    # Update session state content
    if updated_code and updated_code != st.session_state.editor_content:
        st.session_state.editor_content = updated_code

    if st.button("🚀 Generate PDF"):
        try:
            parsed = json.loads(st.session_state.editor_content)
            with open(DATA_PATH, "w") as f:
                json.dump(parsed, f, indent=2)
            render_resume(DATA_PATH, TEMPLATE_PATH, OUTPUT_DIR)
            st.success("✅ PDF generated successfully.")
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
            file_name=f"Aryan_Jain_Resume_{variant_folder}{suffix}.pdf",
            mime="application/pdf"
        )
    else:
        st.info("No PDF generated yet.")
