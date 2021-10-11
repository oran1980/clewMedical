from sqlalchemy import Column, String,  DATETIME
from ConsumerService.consumer.persistence.db import Base


class PatientsMeds(Base):
    __tablename__ = 'patients_meds'

    p_id = Column(String, primary_key=True)
    medication_name = Column(String, primary_key=True)
    medication_period_start = Column(DATETIME, primary_key=True)
    medication_period_end = Column(DATETIME)

    def __init__(self, p_id, medication_name, medication_period_start, medication_period_end):
        self.p_id = p_id
        self.medication_name = medication_name
        self.medication_period_start = medication_period_start

        if medication_period_end is not None:
            self.medication_period_end = medication_period_end
