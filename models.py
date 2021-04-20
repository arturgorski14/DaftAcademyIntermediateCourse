from pydantic import BaseModel
from typing import Optional
import datetime


class PatientAPI(BaseModel):
    name: str
    surname: str


class Patient(PatientAPI):
    id: Optional[int] = 0
    register_date: Optional[str] = datetime.date.today().strftime("%Y-%m-%d")
    vaccination_date: Optional[str] = datetime.date.today().strftime("%Y-%m-%d")
