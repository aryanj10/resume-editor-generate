from utils.render import render_resume

if __name__ == "__main__":
    render_resume(
        data_path="resume_data/resume_data.json",
        template_path="template/resume_template.tex",
        output_dir="output"
    )
