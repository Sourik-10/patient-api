<div align="center">

# 🩺 Patient Management API

A clean, validated REST API for managing patient records, with **BMI and health category calculated automatically**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![License](https://img.shields.io/badge/data-dummy%20only-lightgrey)

</div>

---

## ✨ Features

- **Full CRUD**: create, view, partially update and delete patients
- **Strict validation** with Pydantic: positive age/height/weight, allowed gender values, non-empty ID
- **Auto-calculated fields**: `bmi` and `verdict` (`Underweight` / `Normal` / `Overweight` / `Obese`) via Pydantic `computed_field`
- **Sorting** by height, weight or BMI (ascending or descending)
- **Correct HTTP status codes**: `201`, `400`, `404`, `422`
- **Interactive docs** at `/docs` (Swagger UI), generated automatically

> **Note:** `patients.json` holds dummy data and acts as a simple file-based store for learning purposes.

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Sourik-10/patient-api.git
cd patient-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs** to try every endpoint from the browser.

## 📡 API Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/view` | List all patients |
| `GET` | `/patient/{patient_id}` | Get a single patient |
| `GET` | `/sort?sort_by=bmi&order=desc` | Sort by `height`, `weight` or `bmi` |
| `POST` | `/create` | Create a new patient |
| `PUT` | `/update/{patient_id}` | Update any subset of fields (BMI recalculated) |
| `DELETE` | `/delete/{patient_id}` | Delete a patient |

## 🧪 Example

**Create a patient**

```bash
curl -X POST http://127.0.0.1:8000/create \
  -H "Content-Type: application/json" \
  -d '{"id":"P011","name":"Test User","city":"Kolkata","age":28,"gender":"male","height":1.75,"weight":70}'
```

**Get a patient** (`GET /patient/P002`)

```json
{
  "name": "Ravi Mehta",
  "city": "Mumbai",
  "age": 35,
  "gender": "male",
  "height": 1.75,
  "weight": 85,
  "bmi": 27.76,
  "verdict": "Overweight"
}
```

## 📏 BMI Categories

| BMI | Verdict |
|-----|---------|
| below 18.5 | Underweight |
| 18.5 to 24.99 | Normal |
| 25 to 29.99 | Overweight |
| 30 and above | Obese |

## 📁 Project Structure

```
patient-api/
├── main.py            # FastAPI app, models and endpoints
├── patients.json      # Dummy patient data (file-based store)
├── requirements.txt   # Python dependencies
└── README.md
```

## ⚠️ Known Limitations

- JSON file storage is not safe for concurrent writes. A production setup would use a database such as SQLite or PostgreSQL.
- No authentication or authorization.

## 🔭 Roadmap

- [ ] Move storage to SQLite / PostgreSQL
- [ ] Add automated tests with `pytest`
- [ ] Add an ML-powered `/predict` endpoint

## 🛠️ Built With

Python · FastAPI · Pydantic · Uvicorn

---

<div align="center">

Made by [Sourik](https://github.com/Sourik-10)

</div>
