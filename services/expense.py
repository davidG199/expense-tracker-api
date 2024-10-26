from datetime import datetime, timedelta
from typing import Optional
from models.expense import Expense as ExpenseModel
from schemas.expense import Expense



class ExpenseService():

    def __init__(self, db, user_id: int) -> None:
        self.db = db
        self.user_id = user_id

    def get_expenses(self):
        result = self.db.query(ExpenseModel).filter(ExpenseModel.user_id == self.user_id).all()
        return result
    
    def get_expense(self, id: int):
        result = self.db.query(ExpenseModel).filter(ExpenseModel.id == id, ExpenseModel.user_id == self.user_id).first()
        return result

    def create_expense(self, expense: Expense):
        new_expense = ExpenseModel(**expense.model_dump(), user_id = self.user_id)
        self.db.add(new_expense)
        self.db.commit()
        self.db.refresh(new_expense)
        return new_expense
    
    def update_expense(self, data: Expense, id: int):
        expense = self.get_expense(id)
        if not expense:
            return None
        expense.description = data.description
        expense.category = data.category
        expense.date = data.date
        expense.mount = data.mount
        self.db.commit()
        return expense
    
    def delete_expense(self, id: int):
        expense = self.get_expense(id)
        if not expense:
            return None
        self.db.delete(expense)
        self.db.commit()
        return True

    def get_expenses_past_week(self):
        result = self.db.query(ExpenseModel).filter(ExpenseModel.user_id == self.user_id, ExpenseModel.date >= (datetime.now() - timedelta(days=7))).all()
        return result
    
    def get_expenses_past_month(self):
        result = self.db.query(ExpenseModel).filter(ExpenseModel.user_id == self.user_id, ExpenseModel.date >= (datetime.now() - timedelta(weeks=4))).all()
        return result
    
    def get_expenses_three_past_month(self):
        result = self.db.query(ExpenseModel).filter(ExpenseModel.user_id == self.user_id, ExpenseModel.date >= (datetime.now() - timedelta(weeks=12))).all()
        return result

    def get_expenses_custom(self, start_date: Optional[datetime], end_date: Optional[datetime]):
        result = self.db.query(ExpenseModel).filter(ExpenseModel.user_id == self.user_id)

        if start_date:
            result = result.filter(ExpenseModel.date >= start_date)
        if end_date:
            result = result.filter(ExpenseModel.date <= end_date)

        return result.all()

