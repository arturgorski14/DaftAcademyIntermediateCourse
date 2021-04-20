from pydantic import BaseModel


class PatientAPI(BaseModel):
    """Model used for register new patients"""
    name: str
    surname: str


class Patient(PatientAPI):
    """Main Patient model"""
    id: int
    register_date: str
    vaccination_date: str
