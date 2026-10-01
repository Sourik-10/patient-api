# Patient Management API

A small REST API built with **FastAPI** and **Pydantic** for managing patient records. Each patient's BMI and weight category are calculated automatically from height and weight.

> **Note:** `patients.json` contains dummy data for learning purposes. It is used as a simple file-based store, not a real database.

## Features

- Full CRUD: create, view, update (partial) and delete patients
- Input validation with Pydantic (positive height/weight/age, allowed gender values, non-empty ID)
- BMI and verdict (`Underweight` / `Normal` / `Overweight` / `Obese`) computed with Pydantic `computed_field`
- Sort patients by height, weight or BMI
- Proper HTTP status codes (201, 400, 404, 422)

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive Swagger UI.

## Endpoints

| Method | Path                    | Description                                      |
|--------|-------------------------|--------------------------------------------------|
| GET    | `/view`                 | List all patients                                |
| GET    | `/patient/{patient_id}` | Get one patient                                  |
| GET    | `/sort?sort_by=bmi&order=desc` | Sort by `height`, `weight` or `bmi`       |
| POST   | `/create`               | Create a patient                                 |
| PUT    | `/update/{patient_id}`  | Update any subset of fields, BMI is recalculated |
| DELETE | `/delete/{patient_id}`  | Delete a patient                                 |

## Example

```bash
curl -X POST http://127.0.0.1:8000/create \
  -H "Content-Type: application/json" \
  -d '{"id":"P011","name":"Test User","city":"Kolkata","age":28,"gender":"male","height":1.75,"weight":70}'
```

## Known limitations

- JSON file storage is not safe for concurrent writes. A real deployment would use a database such as SQLite or PostgreSQL.
- No authentication.

## Tech

Python, FastAPI, Pydantic, Uvicorn
