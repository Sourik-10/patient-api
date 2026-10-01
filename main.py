import json
from pathlib import Path as FilePath
from typing import Annotated, Literal, Optional

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

app = FastAPI(title="Patient Management API")

# Always resolve patients.json next to this file, so the app works from any folder
DATA_FILE = FilePath(__file__).parent / "patients.json"


class Patient(BaseModel):
    id: Annotated[str, Field(..., min_length=1, description="The ID of the patient")]
    name: Annotated[str, Field(..., min_length=1, description="The name of the patient")]
    city: Annotated[str, Field(..., min_length=1, description="The city of the patient")]
    age: Annotated[int, Field(..., gt=0, description="The age of the patient")]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in metres")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# Model for partial updates. 'id' is excluded because it must not change.
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, min_length=1)]
    city: Annotated[Optional[str], Field(default=None, min_length=1)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.get("/view")
def view_data():
    return load_data()


@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="The field to sort patients by: height, weight, bmi"),
    order: str = Query("asc", description="Sort order: asc or desc"),
):
    valid_sort_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Valid fields are: {', '.join(valid_sort_fields)}",
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc, desc")

    data = load_data()
    return sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == "desc"))


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    # The ID is the dictionary key, so it is not stored inside the record itself
    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully", "patient": patient.model_dump()},
    )


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]

    # Only the fields the client actually sent
    changes = patient_update.model_dump(exclude_unset=True)
    existing_patient.update(changes)

    # Re-validate through Patient so bmi and verdict are recalculated
    patient_obj = Patient(**{**existing_patient, "id": patient_id})
    data[patient_id] = patient_obj.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully", "patient": patient_obj.model_dump()},
    )


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    deleted_patient = data.pop(patient_id)
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully", "deleted_patient": deleted_patient},
    )
