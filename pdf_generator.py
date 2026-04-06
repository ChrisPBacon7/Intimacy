import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from database import Invoice

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("invoice.html")

OUTPUT_DIR = "invoices"

def generate_pdf(invoice: Invoice) -> str:
    """Generates a PDF for the given invoice and returns the file path."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Render HTML with invoice data
    html_out = template.render(invoice=invoice)

    # Define output path
    file_name = f"Rechnung_{invoice.id}_{invoice.customer_name.replace(' ', '_')}.pdf"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    # Generate PDF
    HTML(string=html_out).write_pdf(file_path)

    return file_path

def generate_all_pdfs(invoices: list[Invoice]) -> list[str]:
    """Generates PDFs for a list of invoices."""
    paths = []
    for invoice in invoices:
        paths.append(generate_pdf(invoice))
    return paths
