from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, timedelta


class Patient(BaseModel):
    """Patient model"""
    id: Optional[int]
    name: str
    surname: str
    register_date: Optional[date]
    vaccination_date: Optional[date]

    def __init__(self, **data):
        super().__init__(
            register_date=datetime.now().date(),
            vaccination_date=datetime.now().date()
            + timedelta(
                days=Patient.vaccination_timedelta(
                    data.get("name"), data.get("surname")
                )
            ),
            **data
        )

    @classmethod
    def vaccination_timedelta(cls, name, surname):
        name_letters = "".join(filter(str.isalpha, name))
        surname_letters = "".join(filter(str.isalpha, surname))
        """
        Przykład z uzyciem regexp'a:
        import re
        regex = re.compile(r'[A-Za-z]+') // tylko litery! Uzycie \w przepuszcza tez cyfry oraz podloge
        name_letters = "".join(filter(regex.match, name))
        surname_letters = "".join(filter(regex.match, surname))       
        """
        return len(name_letters) + len(surname_letters)