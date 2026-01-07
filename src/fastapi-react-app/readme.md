This is based on one-page React UI and FastAPI backend that uses a JSON file as the DB.
Backend (src/fastapi-react-app/app.py): CRUD endpoints under /api/employees, health at /api/health, CORS enabled, static hosting for the React page, JSON persistence at data/employees.json (auto-created), runs on port 8000 by default.
Frontend (src/fastapi-react-app/static/index.html + styles.css): React (CDN) single page to list, create, edit, and delete employees; uses the same-origin /api endpoints.

Run it:
1) pip install -r src/requirements.txt (use your venv).
2) uvicorn src.fastapi-react-app.app:app --reload --port 8000
3) Open http://localhost:8000 for the UI; API available at /api/....

The purpose of this is to get my hands into react and fastapi for light weight app development.
