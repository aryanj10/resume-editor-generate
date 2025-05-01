# 🧠 Resume Builder (LaTeX + Streamlit + JSON)

This project is a customizable resume builder where you can:

- 📝 Edit your resume content in a JSON file (via a Streamlit UI)
- 📄 Automatically generate a PDF resume using a LaTeX template
- 🔁 See a live preview and download your resume instantly

---

## 🚀 Features

- JSON-based resume structure (easy to edit, reuse, or version-control)
- Streamlit interface with side-by-side:
  - JSON editor (with syntax highlighting)
  - PDF preview
- LaTeX-powered formatting for professional typography
- Download-ready resume generation

---

## 🖼 Output Format

The PDF resume generated will exactly follow the structure and formatting defined in:


### template/resume_template.tex


> 🛠 **To change visual styling** (font size, spacing, section layout), modify the `.tex` file, not the JSON.

---

## 🛠 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/resume-builder.git
cd resume-builder
```

### Install requirements
```bash
pip install -r requirements.txt
```

### Run the app
```bash
streamlit run streamlit_app.py
```


## File Structure
```protobuf
resume_project/
├── resume_data/
│   └── resume_data.json       # Editable JSON resume content
├── template/
│   └── resume_template.tex    # LaTeX resume template
├── output/
│   └── resume.pdf             # Compiled PDF
├── utils/
│   └── render.py              # Template renderer using Jinja2 + pdflatex
├── streamlit_app.py           # Streamlit UI for editing & preview
└── requirements.txt
```

# Note You’ll also need pdflatex installed (via TeX Live, MiKTeX, etc.)

# Coming Soon
GitHub Actions for automatic resume builds

Section-specific UI editors (optional)

PDF themes

Built by Aryan Jain
