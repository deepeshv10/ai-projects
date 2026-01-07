## Simple App in React using fastapi as backend

from pathlib import Path
from threading import Lock
from typing import List, Optional
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn


# Basic FastAPI app that serves a React single page and a tiny file-backed CRUD API
app = FastAPI(title="File DB Employee App", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = ROOT_DIR / "data" / "employees.json"
STATIC_DIR = Path(__file__).resolve().parent / "static"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

_file_lock = Lock()


def _load_employees_unlocked() -> List[dict]:
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        DATA_FILE.write_text("[]", encoding="utf-8")
    return []


def _save_employees_unlocked(items: List[dict]) -> None:
    DATA_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


def _next_id(items: List[dict]) -> int:
    existing = [item.get("id", 0) for item in items]
    return (max(existing) + 1) if existing else 1


class EmployeeBase(BaseModel):
    name: str
    role: str
    department: str
    email: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None


class Employee(EmployeeBase):
    id: int


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/employees", response_model=List[Employee])
def list_employees():
    with _file_lock:
        return _load_employees_unlocked()


@app.get("/api/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    with _file_lock:
        employees = _load_employees_unlocked()
    for emp in employees:
        if emp.get("id") == employee_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/api/employees", response_model=Employee)
def create_employee(payload: EmployeeCreate):
    with _file_lock:
        employees = _load_employees_unlocked()
        new_employee = payload.model_dump()
        new_employee["id"] = _next_id(employees)
        employees.append(new_employee)
        _save_employees_unlocked(employees)
    return new_employee


@app.put("/api/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, payload: EmployeeUpdate):
    with _file_lock:
        employees = _load_employees_unlocked()
        for idx, emp in enumerate(employees):
            if emp.get("id") == employee_id:
                updated = {**emp, **{k: v for k, v in payload.model_dump().items() if v is not None}}
                employees[idx] = updated
                _save_employees_unlocked(employees)
                return updated
    raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/api/employees/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int):
    with _file_lock:
        employees = _load_employees_unlocked()
        for idx, emp in enumerate(employees):
            if emp.get("id") == employee_id:
                removed = employees.pop(idx)
                _save_employees_unlocked(employees)
                return removed
    raise HTTPException(status_code=404, detail="Employee not found")


# Serve the one-pager React app (built with CDN React for simplicity)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

