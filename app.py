import streamlit as st
import pandas as pd
from sqlmodel import select
import os

from database import engine, get_session, Invoice, PaymentMethod, create_db_and_tables
from pdf_generator import generate_pdf

st.set_page_config(page_title="Intimacy Invoices", layout="wide")

# Ensure DB is created
create_db_and_tables()

st.title("Intimacy Tattoo - Invoicing App")

# Get DB session
session = next(get_session())

# -----------------
# Data Editor Section
# -----------------
st.header("Invoice Data Editor")

# Fetch current invoices
invoices = session.exec(select(Invoice)).all()

# Create a DataFrame for the data editor
if invoices:
    df = pd.DataFrame([inv.model_dump() for inv in invoices])
else:
    # Empty DataFrame with correct columns
    df = pd.DataFrame(columns=[
        "id", "customer_name", "customer_address", "service_description",
        "total_amount", "down_payment", "down_payment_method",
        "final_payment_method", "payment_notes", "invoice_date", "pdf_generated"
    ])

# Ensure datetime for invoice_date
if not df.empty:
    df["invoice_date"] = pd.to_datetime(df["invoice_date"]).dt.date

# Configure columns for Streamlit data editor
column_config = {
    "id": st.column_config.NumberColumn("ID", disabled=True),
    "customer_name": "Customer Name",
    "customer_address": "Customer Address",
    "service_description": "Service Description",
    "total_amount": st.column_config.NumberColumn("Total Amount (€)", min_value=0.0, format="%.2f"),
    "down_payment": st.column_config.NumberColumn("Down Payment (€)", default=50.0, min_value=0.0, format="%.2f"),
    "down_payment_method": st.column_config.SelectboxColumn("Down Payment Method", options=[e.value for e in PaymentMethod], default=PaymentMethod.TRANSFER.value),
    "final_payment_method": st.column_config.SelectboxColumn("Final Payment Method", options=[e.value for e in PaymentMethod], default=PaymentMethod.CASH.value),
    "payment_notes": "Payment Notes (e.g. Belegnr.)",
    "invoice_date": st.column_config.DateColumn("Date"),
    "pdf_generated": st.column_config.CheckboxColumn("PDF Generated?", disabled=True)
}

# Display Data Editor
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    column_config=column_config,
    use_container_width=True,
    column_order=[
        "customer_name", "customer_address", "service_description",
        "total_amount", "down_payment", "down_payment_method",
        "final_payment_method", "payment_notes", "invoice_date", "pdf_generated"
    ], # ID hidden
    key="invoice_editor"
)

if st.button("Save Changes to Database"):
    # Delete missing rows
    current_ids = set(df["id"].dropna().astype(int).tolist())
    edited_ids = set(edited_df["id"].dropna().astype(int).tolist())
    deleted_ids = current_ids - edited_ids

    if deleted_ids:
        for d_id in deleted_ids:
            inv_to_delete = session.get(Invoice, d_id)
            if inv_to_delete:
                session.delete(inv_to_delete)

    # Update or Create rows
    for index, row in edited_df.iterrows():
        row_dict = row.to_dict()

        # Ensure invoice_date is a python date object
        if 'invoice_date' in row_dict and isinstance(row_dict['invoice_date'], str):
            try:
                row_dict['invoice_date'] = pd.to_datetime(row_dict['invoice_date']).date()
            except:
                pass
        elif 'invoice_date' in row_dict and pd.notna(row_dict['invoice_date']) and hasattr(row_dict['invoice_date'], 'date'):
            # It might be a Timestamp
            if hasattr(row_dict['invoice_date'], 'to_pydatetime'):
                row_dict['invoice_date'] = row_dict['invoice_date'].to_pydatetime().date()

        if pd.isna(row_dict.get('id')): # New row
            new_inv = Invoice(**{k: v for k, v in row_dict.items() if k != 'id' and not pd.isna(v)})
            session.add(new_inv)
        else: # Update existing row
            inv_id = int(row_dict['id'])
            existing_inv = session.get(Invoice, inv_id)
            if existing_inv:
                for key, value in row_dict.items():
                    if hasattr(existing_inv, key) and key != 'id':
                        setattr(existing_inv, key, value)
                session.add(existing_inv)

    session.commit()
    st.success("Changes saved successfully!")
    st.rerun()

st.divider()

# -----------------
# PDF Generation Section
# -----------------
st.header("Generate PDFs")

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate PDFs for pending Invoices"):
        pending = session.exec(select(Invoice).where(Invoice.pdf_generated == False)).all()
        if pending:
            for inv in pending:
                generate_pdf(inv)
                inv.pdf_generated = True
                session.add(inv)
            session.commit()
            st.success(f"Generated {len(pending)} PDFs!")
            st.rerun()
        else:
            st.info("No pending invoices to generate.")

with col2:
    if st.button("Regenerate All PDFs"):
        all_inv = session.exec(select(Invoice)).all()
        if all_inv:
            for inv in all_inv:
                generate_pdf(inv)
                inv.pdf_generated = True
                session.add(inv)
            session.commit()
            st.success(f"Regenerated {len(all_inv)} PDFs!")
            st.rerun()
        else:
            st.info("No invoices found.")

st.divider()

# -----------------
# Output Overview Section
# -----------------
st.header("Generated Invoices Overview")

OUTPUT_DIR = "invoices"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

pdf_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".pdf")]

if pdf_files:
    for pdf_file in pdf_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(pdf_file)
        with col2:
            with open(os.path.join(OUTPUT_DIR, pdf_file), "rb") as f:
                st.download_button(
                    label="Download",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
else:
    st.write("No PDFs generated yet.")
