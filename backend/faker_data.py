import pandas as pd
from faker import Faker
import random
import json
import os
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_data(num_records=1500):
    print("Generating synthetic data...")
    
    # 1. Branches / Departments
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Medicine', 'Dermatology', 'Emergency']
    
    # 2. Doctors
    doctors = []
    for _ in range(50):
        doctors.append({
            'doctor_id': fake.uuid4(),
            'name': f"Dr. {fake.first_name()} {fake.last_name()}",
            'department': random.choice(departments),
            'joining_date': fake.date_between(start_date='-5y', end_date='today').isoformat()
        })
    df_doctors = pd.DataFrame(doctors)
    
    # 3. Patients
    patients = []
    for _ in range(500):
        patients.append({
            'patient_id': fake.uuid4(),
            'mr_number': f"MR-{fake.unique.random_number(digits=6)}",
            'name': fake.name(),
            'age': random.randint(1, 90),
            'gender': random.choice(['Male', 'Female']),
            'city': fake.city()
        })
    df_patients = pd.DataFrame(patients)
    
    # 4. Case History (Visits)
    case_history = []
    # We want ~1500 visits
    for _ in range(num_records):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        
        # Logic: Emergency dept has more emergency cases
        visit_type = 'Emergency' if doctor['department'] == 'Emergency' else random.choice(['OPD', 'OPD', 'OPD', 'Emergency']) # 75% OPD
        
        visit_date = fake.date_time_between(start_date='-1y', end_date='now')
        
        case_history.append({
            'case_id': fake.uuid4(),
            'patient_id': patient['patient_id'],
            'doctor_id': doctor['doctor_id'],
            'visit_date': visit_date.isoformat(),
            'visit_type': visit_type,
            'diagnosis': fake.sentence(nb_words=3),
            'consultation_fee': random.randint(500, 3000)
        })
    df_case_history = pd.DataFrame(case_history)
    
    # 5. Prescriptions
    prescriptions = []
    common_drugs = ['Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Metformin', 'Atorvastatin', 'Omeprazole', 'Amlodipine', 'Metoprolol', 'Azithromycin', 'Albuterol']
    
    for case in case_history:
        # 80% of visits result in a prescription
        if random.random() < 0.8:
            num_meds = random.randint(1, 4)
            for _ in range(num_meds):
                prescriptions.append({
                    'prescription_id': fake.uuid4(),
                    'case_id': case['case_id'],
                    'medicine_name': random.choice(common_drugs),
                    'dosage': f"{random.randint(1, 3)} times a day",
                    'duration': f"{random.randint(3, 14)} days"
                })
    df_prescriptions = pd.DataFrame(prescriptions)
    
    # Compile into a single dictionary
    data = {
        'doctors': doctors,
        'patients': patients,
        'case_history': case_history,
        'prescriptions': prescriptions
    }
    
    # Save to JSON
    output_file = os.path.join(os.path.dirname(__file__), 'mock_data.json')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data generated successfully! Saved to {output_file}")
    print(f"Stats: {len(doctors)} Doctors, {len(patients)} Patients, {len(case_history)} Visits, {len(prescriptions)} Prescriptions")

if __name__ == "__main__":
    generate_data()
