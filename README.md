# Intimacy Tattoo Invoicing App

A streamlined tool tailored for the tattoo artist *Intimacy* to create and manage professional, legally compliant invoices seamlessly. Built specifically to handle standard operations, payments (down payment + remaining payment), and outputs into nicely structured PDFs.

## Tech Stack
- **Python**: 3.12+
- **Package Manager**: PDM
- **Frontend**: Streamlit
- **Database**: SQLite (managed with SQLModel / Pydantic)
- **PDF Generation**: WeasyPrint & Jinja2
- **Data Handling**: Pandas

## Core Features
1. **Interactive Data Editor**: Add, edit, or delete customer/invoice details in a dynamically scaling grid right in your browser.
2. **Automated Calculations & Standardized Details**:
   - Pre-fills down payments (50€ default).
   - Dynamically calculates the rest sum based on standard prices.
   - Contains Kleinunternehmerregelung info ("Gemäß § 19 UStG wird keine Umsatzsteuer berechnet und ausgewiesen.").
3. **Professional PDF Rendering**: Generates beautiful A4 PDF files using customized HTML/CSS Templates, ready to print or email.
4. **Download Overview**: Shows newly and previously generated PDFs in an overview segment for direct downloading.

## Setup Instructions

Ensure you have [PDM](https://pdm-project.org/) installed on your machine.

1. **Clone the repository** (if applicable) and move into the project directory:
   ```bash
   cd intimacy-invoicing
   ```

2. **Install dependencies**:
   ```bash
   pdm install
   ```

3. **Run the Application**:
   ```bash
   pdm run streamlit run app.py
   ```

4. **Open your browser** to the Local URL indicated by Streamlit (usually `http://localhost:8501`).

## Usage Guide
1. At the top of the interface, use the data editor grid to enter new clients or modify past entries. Click `Save Changes to Database`!
2. Click `Generate PDFs for pending Invoices` to automatically generate all missing invoices, or regenerate the entire database.
3. Download the finished `.pdf` files from the "Generated Invoices Overview" directly.

## Customization
- **Logo**: Open `templates/invoice.html` and replace the placeholder text with an `<img>` tag linking to your actual logo.
- **Shop details**: Update addresses/email details directly in the HTML template.
