from datetime import datetime
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from schemas.expense import Expense
from fastapi import APIRouter, Depends, Query
from services.expense import ExpenseService
from models.user import User as UserModel
from middlewares.jwt_bearer import get_current_user

expense_router = APIRouter(prefix="/expense", tags=["expense"])

@expense_router.post("/create", response_model=dict, status_code=201)
def new_expense(expense: Expense, current_user: UserModel = Depends(get_current_user)) -> dict:
    db = Session()
    ExpenseService(db, user_id=current_user.id).create_expense(expense)
    return JSONResponse(status_code=200, content={"message": "expense created successfully"})

@expense_router.get("/", response_model=List[Expense], status_code=200)
def get_expenses(current_user: UserModel = Depends(get_current_user)) -> List:
    db = Session()
    result = ExpenseService(db, user_id = current_user.id).get_expenses()

    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    return JSONResponse(status_code=404, content={"message": "No expenses found"})
@expense_router.get("/id/{id}", response_model=dict, status_code=200)
def get_expense(id: int, current_user: UserModel = Depends(get_current_user)) -> dict:
    db = Session()
    result = ExpenseService(db, user_id=current_user.id).get_expense(id)

    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={"message": "Expense not found"})

@expense_router.put("/edit/{id}", response_model=dict, status_code=200)
def edit_expense(expense: Expense,id: int, current_user: UserModel = Depends(get_current_user)) -> dict:
    db = Session()
    result = ExpenseService(db, user_id=current_user.id).get_expense(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Expense not found"})
    ExpenseService(db, user_id=current_user.id).update_expense(expense, id)
    return JSONResponse(status_code=200, content={"message": "Expense updated"})

@expense_router.delete("/delete/{id}", response_model=dict, status_code=200)
def delete_expense(id: int, current_user: UserModel = Depends(get_current_user)) -> dict:
    db = Session()
    result = ExpenseService(db, user_id=current_user.id).delete_expense(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Expense not found"})
    return JSONResponse(status_code=200, content={"message": "Expense deleted"})

@expense_router.get("/search/past-week", response_model=List[Expense], status_code=200)
def search_past_week(current_user: UserModel = Depends(get_current_user)) -> dict:
    db = Session()
    result = ExpenseService(db, user_id=current_user.id).get_expenses_past_week()
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={"message": "No expenses found in the past week"})

@expense_router.get("/search/past-month", response_model=List[Expense], status_code=200)
def search_past_month(current_user: UserModel = Depends(get_current_user)) -> dict:
    db = Session()
    result = ExpenseService(db, user_id=current_user.id).get_expenses_past_month()
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={"message": "No expenses found in the past month"})

@expense_router.get("/search/three-past-month", response_model=List[Expense], status_code=200)
def search_three_past_month(current_user: UserModel =Depends(get_current_user)) -> dict:
    db = Session()
    result = ExpenseService(db, user_id=current_user.id).get_expenses_three_past_month()
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={"message": "No expenses found in the past three months"})

@expense_router.get("/search/by-dates", response_model=List[Expense], status_code=200)
def search_by_dates(
    start_date: Optional[str] = Query(None, description="start date in format YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="end date in format YYYY-MM-DD"),
    current_user: UserModel = Depends(get_current_user)
) -> dict:
    db = Session()
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    except ValueError:
        return JSONResponse(status_code=400, content={"message": "Invalid date format. Use YYYY-MM-DD."})

    result = ExpenseService(db, user_id=current_user.id).get_expenses_custom(start, end)
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={"message": "No expenses found in the specified date range"})


