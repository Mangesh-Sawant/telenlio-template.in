from jinja2 import Template
from weasyprint import HTML

def render_pdf_from_template(html_code: str, data: dict, css_code: str = ""):
    rendered_html = Template(html_code).render(**data)
    return HTML(string=f"<style>{css_code}</style>{rendered_html}").write_pdf()
