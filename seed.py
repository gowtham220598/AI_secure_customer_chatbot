from datetime import date
from decimal import Decimal
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Customer, Invoice

with SessionLocal() as db:
    for name, mobile, prefix in [('Arun','+919876543210','AR'),('Deepa','+919123456780','DE')]:
        customer = db.scalar(select(Customer).where(Customer.mobile == mobile))
        if not customer:
            customer = Customer(name=name, mobile=mobile)
            db.add(customer); db.flush()
        for n in range(1,6):
            number = f'{prefix}-{n:03d}'
            if not db.scalar(select(Invoice).where(Invoice.customer_id == customer.id, Invoice.invoice_number == number)):
                db.add(Invoice(customer_id=customer.id, invoice_number=number, invoice_date=date(2026,10,n),
                               amount=Decimal(500*n), currency='INR', status='unpaid' if n%2 else 'paid', indexed=False))
    db.commit()
print('Seeded Arun and Deepa with 5 invoices each; run reindex for each account')
