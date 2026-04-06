from database import Invoice, PaymentMethod
from pdf_generator import generate_pdf

test_invoice = Invoice(
    id=2,
    customer_name="Max Mustermann",
    customer_address="Musterweg 5\n54321 Teststadt",
    service_description="Tattoo Oberarm (Rose)",
    total_amount=250.0,
    down_payment=50.0,
    down_payment_method=PaymentMethod.TRANSFER.value,
    final_payment_method=PaymentMethod.CASH.value,
    payment_notes="Belegnr. 12345"
)

path = generate_pdf(test_invoice)
print(f"Generated PDF at: {path}")
