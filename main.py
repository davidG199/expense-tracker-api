from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Base, engine
from routers.expenses import expense_router
from routers.users import user_router

app = FastAPI()

app.title = "Expense-tracker-api"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

app.include_router(expense_router)
app.include_router(user_router)

@app.get("/", tags=["root"])
def message():
    return HTMLResponse("<h1>Expense tracker api</h1>")



