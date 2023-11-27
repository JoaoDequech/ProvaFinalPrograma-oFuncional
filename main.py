from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime

app = FastAPI()

engine = create_engine('postgresql://postgres:root@localhost:6700/postgres')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patient'

    PatientID = Column(Integer, primary_key=True)
    Name = Column(String)
    LastName = Column(String)
    vaccines = relationship('Vaccine')

class Vaccine(Base):
    __tablename__ = 'vaccine'

    VaccineID = Column(Integer, primary_key=True)
    PatientID = Column(Integer, ForeignKey('patient.PatientID', ondelete='CASCADE'))
    VaccineName = Column(String)
    DoseDate = Column(DateTime)
    DoseNumber = Column(Integer)
    VaccineType = Column(String)
    doses = relationship('Dose')

class Dose(Base):
    __tablename__ = 'dose'

    DoseID = Column(Integer, primary_key=True)
    VaccineID = Column(Integer, ForeignKey('vaccine.VaccineID', ondelete='CASCADE'))
    TypeDose = Column(String)
    DoseDate = Column(DateTime)
    DoseNumber = Column(Integer)
    ApplicationType = Column(String)


Base.metadata.create_all(bind=engine)

@app.post("/patients")
def create_patient(name: str, last_name: str):
    patient = Patient(Name=name, LastName=last_name)
    session.add(patient)
    session.commit()

    return JSONResponse(content={'PatientID': patient.PatientID, 'Name': patient.Name, 'LastName': patient.LastName})

@app.post("/vaccines")
def create_vaccine(patient_id: int, vaccine_name: str, dose_number: int, vaccine_type: str):
    vaccine = Vaccine(PatientID=patient_id, DoseDate = datetime.datetime.now(), VaccineName=vaccine_name, DoseNumber=dose_number, VaccineType=vaccine_type)
    session.add(vaccine)
    session.commit()

    return JSONResponse(content={'VaccineID': vaccine.VaccineID, 'PatientID': vaccine.PatientID, 'VaccineName': vaccine.VaccineName, 'DoseDate': str(vaccine.DoseDate), 'DoseNumber': vaccine.DoseNumber, 'VaccineType': vaccine.VaccineType})

@app.post("/doses")
def create_dose(vaccine_id: int, type_dose: str, dose_number: int, application_type: str):
    dose = Dose(VaccineID=vaccine_id, TypeDose=type_dose,DoseDate = datetime.datetime.now(), DoseNumber=dose_number, ApplicationType=application_type)
    session.add(dose)
    session.commit()

    return JSONResponse(content={'DoseID': dose.DoseID, 'VaccineID': dose.VaccineID, 'TypeDose': dose.TypeDose, 'DoseDate': str(dose.DoseDate), 'DoseNumber': dose.DoseNumber, 'ApplicationType': dose.ApplicationType})


@app.put("/patients")
def update_patient(patient_id: int, name: str, last_name: str):
    patient = session.query(Patient).filter_by(PatientID=patient_id).first()
    if patient:
        patient.Name = name
        patient.LastName = last_name
        session.commit()
        return JSONResponse(content={'PatientID': patient.PatientID, 'Name': patient.Name, 'LastName': patient.LastName})
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/vaccines/")
def update_vaccine(vaccine_id: int, patient_id: int, vaccine_name: str, dose_number: int, vaccine_type: str):
    vaccine = session.query(Vaccine).filter_by(VaccineID=vaccine_id).first()
    if vaccine:
        vaccine.PatientID = patient_id
        vaccine.VaccineName = vaccine_name
        vaccine.DoseNumber = dose_number
        vaccine.VaccineType = vaccine_type
        session.commit()
        return JSONResponse(content={'VaccineID': vaccine.VaccineID, 'PatientID': vaccine.PatientID, 'VaccineName': vaccine.VaccineName, 'DoseDate': str(vaccine.DoseDate), 'DoseNumber': vaccine.DoseNumber, 'VaccineType': vaccine.VaccineType})
    else:
        raise HTTPException(status_code=404, detail="Vaccine not found")

@app.put("/doses/")
def update_dose(dose_id: int, vaccine_id: int, type_dose: str, dose_number: int, application_type: str):
    dose = session.query(Dose).filter_by(DoseID=dose_id).first()
    if dose:
        dose.VaccineID = vaccine_id
        dose.TypeDose = type_dose
        dose.DoseNumber = dose_number
        dose.ApplicationType = application_type
        session.commit()
        return JSONResponse(content={'DoseID': dose.DoseID, 'VaccineID': dose.VaccineID, 'TypeDose': dose.TypeDose, 'DoseDate': str(dose.DoseDate), 'DoseNumber': dose.DoseNumber, 'ApplicationType': dose.ApplicationType})
    else:
        raise HTTPException(status_code=404, detail="Dose not found")
    

@app.get("/patients/")
def get_patient(patient_id: int):
    patient = session.query(Patient).filter_by(PatientID=patient_id).first()
    if patient:
        return JSONResponse(content={'PatientID': patient.PatientID, 'Name': patient.Name, 'LastName': patient.LastName})
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patients")
def get_all_patients():
    patients = session.query(Patient).all()

    patients_list = []
    for patient in patients:
        patients_list.append({'PatientID': patient.PatientID, 'Name': patient.Name, 'LastName': patient.LastName})

    return JSONResponse(content=patients_list)

@app.get("/vaccines/")
def get_vaccine(vaccine_id: int):
    vaccine = session.query(Vaccine).filter_by(VaccineID=vaccine_id).first()
    if vaccine:
        return JSONResponse(content={'VaccineID': vaccine.VaccineID, 'PatientID': vaccine.PatientID, 'VaccineName': vaccine.VaccineName, 'DoseDate': str(vaccine.DoseDate), 'DoseNumber': vaccine.DoseNumber, 'VaccineType': vaccine.VaccineType})
    else:
        raise HTTPException(status_code=404, detail="Vaccine not found")

@app.get("/vaccines")
def get_all_vaccines():
    vaccines = session.query(Vaccine).all()

    vaccines_list = []
    for vaccine in vaccines:
        vaccines_list.append({'VaccineID': vaccine.VaccineID, 'PatientID': vaccine.PatientID, 'VaccineName': vaccine.VaccineName, 'DoseDate': str(vaccine.DoseDate), 'DoseNumber': vaccine.DoseNumber, 'VaccineType': vaccine.VaccineType})

    return JSONResponse(content=vaccines_list)

@app.get("/doses/")
def get_dose(dose_id: int):
    dose = session.query(Dose).filter_by(DoseID=dose_id).first()
    if dose:
        return JSONResponse(content={'DoseID': dose.DoseID, 'VaccineID': dose.VaccineID, 'TypeDose': dose.TypeDose, 'DoseDate': str(dose.DoseDate), 'DoseNumber': dose.DoseNumber, 'ApplicationType': dose.ApplicationType})
    else:
        raise HTTPException(status_code=404, detail="Dose not found")

@app.get("/doses")
def get_all_doses():
    doses = session.query(Dose).all()

    doses_list = []
    for dose in doses:
        doses_list.append({'DoseID': dose.DoseID, 'VaccineID': dose.VaccineID, 'TypeDose': dose.TypeDose, 'DoseDate': str(dose.DoseDate), 'DoseNumber': dose.DoseNumber, 'ApplicationType': dose.ApplicationType})

    return JSONResponse(content=doses_list)

@app.delete("/patients")
def delete_patient(patient_id: int):
    patient = session.query(Patient).filter_by(PatientID=patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        return JSONResponse(content={"message": f"Patient {patient_id} deleted"})
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/vaccines")
def delete_vaccine(vaccine_id: int):
    vaccine = session.query(Vaccine).filter_by(VaccineID=vaccine_id).first()
    if vaccine:
        session.delete(vaccine)
        session.commit()
        return JSONResponse(content={"message": f"Vaccine {vaccine_id} deleted"})
    else:
        raise HTTPException(status_code=404, detail="Vaccine not found")

@app.delete("/doses")
def delete_dose(dose_id: int):
    dose = session.query(Dose).filter_by(DoseID=dose_id).first()
    if dose:
        session.delete(dose)
        session.commit()
        return JSONResponse(content={"message": f"Dose {dose_id} deleted"})
    else:
        raise HTTPException(status_code=404, detail="Dose not found")
    

@app.get("/pacientsAndVaccinesAndDoses")

def get_pacientsAndVaccinesAndDoses(pacient_id: int):

    pacients = session.query(Patient).filter_by(PatientID=pacient_id).first()

    pacients_list = []

    pacients_dict = {'PatientID': pacients.PatientID, 'Name': pacients.Name, 'LastName': pacients.LastName}
    pacients_list.append(pacients_dict)

    vaccines = session.query(Vaccine).filter_by(PatientID=pacient_id).all()

    vaccines_list = []

    for vaccine in vaccines:
        vaccines_dict = {'VaccineID': vaccine.VaccineID, 'PatientID': vaccine.PatientID, 'VaccineName': vaccine.VaccineName, 'DoseDate': str(vaccine.DoseDate), 'DoseNumber': vaccine.DoseNumber, 'VaccineType': vaccine.VaccineType}
        vaccines_list.append(vaccines_dict)

    doses = session.query(Dose).filter_by(VaccineID=vaccine.VaccineID).all()

    doses_list = []

    for dose in doses:
        doses_dict = {'DoseID': dose.DoseID, 'VaccineID': dose.VaccineID, 'TypeDose': dose.TypeDose, 'DoseDate': str(dose.DoseDate), 'DoseNumber': dose.DoseNumber, 'ApplicationType': dose.ApplicationType}
        doses_list.append(doses_dict)

    return JSONResponse(content={'pacients': pacients_list, 'vaccines': vaccines_list, 'doses': doses_list})

@app.get("/vaccinesAndDoses")

def get_vaccinesAndDoses(vaccine_id: int):

    vaccines = session.query(Vaccine).filter_by(VaccineID=vaccine_id).first()

    vaccines_list = []

    vaccines_dict = {'VaccineID': vaccines.VaccineID, 'PatientID': vaccines.PatientID, 'VaccineName': vaccines.VaccineName, 'DoseDate': str(vaccines.DoseDate), 'DoseNumber': vaccines.DoseNumber, 'VaccineType': vaccines.VaccineType}
    vaccines_list.append(vaccines_dict)

    doses = session.query(Dose).filter_by(VaccineID=vaccine_id).all()

    doses_list = []

    for dose in doses:
        doses_dict = {'DoseID': dose.DoseID, 'VaccineID': dose.VaccineID, 'TypeDose': dose.TypeDose, 'DoseDate': str(dose.DoseDate), 'DoseNumber': dose.DoseNumber, 'ApplicationType': dose.ApplicationType}
        doses_list.append(doses_dict)

    return JSONResponse(content={'vaccines': vaccines_list, 'doses': doses_list})


