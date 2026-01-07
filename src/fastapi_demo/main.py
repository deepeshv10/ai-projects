### FastAPI API demo - Deepesh Verma
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    position: str

employees: List[Employee] = []


@app.get("/")
def home():
    return "Welcome to the Employee Management API"

@app.get("/employees")
def get_employees():
    return employees

@app.post("/employees")
def create_employee(employee: Employee):
    employees.append(employee)
    return employee

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    return next((emp for emp in employees if emp.id == employee_id), None)

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    for i, emp in enumerate(employees):
        if emp.id == employee_id:
            employees[i] = employee
            return employee
    return {"error": "Employee not found"}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for i, emp in enumerate(employees):
        if emp.id == employee_id:
            return employees.pop(i)
    return {"error": "Employee not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)

