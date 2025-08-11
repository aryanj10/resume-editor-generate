def render_resume(data_path, template_path, output_dir, context=None):
    import json
    import os
    import subprocess
    from jinja2 import Environment, FileSystemLoader

    if context is None:
        context = {}

    # Load JSON data
    with open(data_path) as f:
        data = json.load(f)

    # Merge extra context (e.g. showteaching=True)
    data.update(context)

    # Jinja2 environment
    template_dir, template_file = os.path.split(template_path)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        block_start_string='((*',
        block_end_string='*))',
        variable_start_string='(((',
        variable_end_string=')))',
        comment_start_string='((=',
        comment_end_string='=))'
    )
    template = env.get_template(template_file)

    # Render LaTeX content
    rendered_tex = template.render(**data)

    # Write LaTeX file to output directory
    os.makedirs(output_dir, exist_ok=True)
    tex_path = os.path.join(output_dir, "Aryan_Jain_Resume.tex")
    with open(tex_path, 'w') as f:
        f.write(rendered_tex)

    # Compile to PDF using pdflatex
    subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_path],
        check=True
    )
