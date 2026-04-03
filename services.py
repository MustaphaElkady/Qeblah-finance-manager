from sqlalchemy.orm import joinedload
from sqlalchemy import extract, func
from models import Client, Package, Contract, Payment, Expense

def get_all_clients(session):
     return session.query(Client).all()

def get_all_packages(session):
    return session.query(Package).all()

def get_all_contracts(session):
    return (
        session.query(Contract)
        .options(joinedload(Contract.client), joinedload(Contract.package))
        .all()
    )

def get_contract_summary(session, contract_id):
     contract = (
     session.query(Contract)
     .options(joinedload(Contract.client), joinedload(Contract.package))
     .filter(Contract.id == contract_id)
     .first()
     )
     if not contract:
          return None
     
     total_paid = sum(p.amount for p in contract.payments)
     total_expenses = sum(e.amount for e in contract.expenses)
     remaining = contract.agreed_price - total_paid
     profit = total_paid - total_expenses
     return {
    "contract_id": contract.id,
    "client_name": contract.client.name,
    "package_name": contract.package.package_name,
    "agreed_price": contract.agreed_price,
    "total_paid": total_paid,
    "remaining": remaining,
    "total_expenses": total_expenses,
    "profit": profit,
    "status": contract.status,
}

def get_dashboard_metrics(session):
    total_clients = session.query(Client).count()
    total_contracts = session.query(Contract).count()

    total_payments = session.query(func.coalesce(func.sum(Payment.amount), 0)).scalar()
    total_expenses = session.query(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    total_profit = total_payments - total_expenses

    return {
        "total_clients": total_clients,
        "total_contracts": total_contracts,
        "total_payments": total_payments,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
    }

def get_monthly_summary(session, year, month):
    payments_total = (
        session.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(extract("year", Payment.payment_date) == year)
        .filter(extract("month", Payment.payment_date) == month)
        .scalar()
    )

    expenses_total = (
        session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(extract("year", Expense.expense_date) == year)
        .filter(extract("month", Expense.expense_date) == month)
        .scalar()
    )

    return {
        "month_income": payments_total,
        "month_expenses": expenses_total,
        "month_profit": payments_total - expenses_total,
    }

def get_package_profitability(session):
    contracts = get_all_contracts(session)
    result = []

    for contract in contracts:
        total_paid = sum(p.amount for p in contract.payments)
        total_expenses = sum(e.amount for e in contract.expenses)
        profit = total_paid - total_expenses

        result.append({
            "contract_id": contract.id,
            "client_name": contract.client.name,
            "package_name": contract.package.package_name,
            "agreed_price": contract.agreed_price,
            "total_paid": total_paid,
            "total_expenses": total_expenses,
            "profit": profit,
        })

    return result