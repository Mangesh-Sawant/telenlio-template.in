from jinja2 import Template
from weasyprint import HTML
import tempfile
import os

def generate_pdf_from_template(html: str, css: str, data: dict) -> str:
    # Render HTML with data
    jinja_template = Template(html)
    rendered_html = jinja_template.render(**data)

    # Save CSS to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".css", mode="w") as css_file:
        css_file.write(css)
        css_path = css_file.name

    # Create PDF from rendered HTML and CSS
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=rendered_html).write_pdf(pdf_file.name, stylesheets=[css_path])

    os.unlink(css_path)  # cleanup
    return pdf_file.name
