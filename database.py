from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "1. In Person using cash"
    CARD = "2. In Person using credit/debit card"
    TRANSFER = "3. Using Paypal / Bank Transfer"
    NONE = "None"

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    customer_address: str
    service_description: str
    total_amount: float
    down_payment: float = Field(default=50.0)
    down_payment_method: str = Field(default=PaymentMethod.TRANSFER.value)
    final_payment_method: str = Field(default=PaymentMethod.CASH.value)
    invoice_date: date = Field(default_factory=date.today)
    pdf_generated: bool = Field(default=False)

sqlite_file_name = "invoices.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created.")
