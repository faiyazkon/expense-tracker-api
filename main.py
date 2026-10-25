from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── Pydantic models (the security guards) ─────────────────────

class UserCreate(BaseModel):
    name: str = Field(min_length=1)

class UserOut(BaseModel):
    id: int
    name: str

class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    paid_by_id: int

class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    paid_by_id: int

# ── In-memory storage (replaced by database on Day 3) ────────

users: dict[int, dict] = {}
expenses: dict[int, dict] = {}
next_user_id = 1
next_expense_id = 1

# ── App ───────────────────────────────────────────────────────

app = FastAPI(title="Expense Tracker API")


# ── POST /users ───────────────────────────────────────────────

@app.post("/users", status_code=201, response_model=UserOut)
def create_user(user: UserCreate):
    global next_user_id
    new_user = {"id": next_user_id, "name": user.name}
    users[next_user_id] = new_user
    next_user_id += 1
    return new_user

# ── POST /expenses ────────────────────────────────────────────

@app.post("/expenses", status_code=201, response_model=ExpenseOut)
def create_expense(expense: ExpenseCreate):
    global next_expense_id
    if expense.paid_by_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    new_expense = {
        "id": next_expense_id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
        "paid_by_id": expense.paid_by_id,
    }
    expenses[next_expense_id] = new_expense
    next_expense_id += 1
    return new_expense

# ── GET /expenses ─────────────────────────────────────────────

@app.get("/expenses")
def list_expenses(category: str | None = None, min_amount: float = 0):
    result = list(expenses.values())
    if category:
        result = [e for e in result if e["category"] == category]
    result = [e for e in result if e["amount"] >= min_amount]
    return result

# ── GET /balances ─────────────────────────────────────────────

@app.get("/balances")
def get_balances():
    total = sum(e["amount"] for e in expenses.values())
    per_person = total / len(users) if users else 0
    balances = {}
    for uid, user in users.items():
        paid = sum(e["amount"] for e in expenses.values() if e["paid_by_id"] == uid)
        balances[user["name"]] = round(paid - per_person, 2)
    return balances

@app.get("/users")
def list_users():
    return list(users.values())

# ── DELETE /expenses/{expense_id} ─────────────────────────────

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    deleted = expenses.pop(expense_id)
    return {"message": "Deleted", "expense": deleted}

@app.get("/")
def root():
    return {"message": "Expense Tracker API"} 

print(users)