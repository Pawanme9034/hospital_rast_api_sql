import pyodbc

class PatientDatabase:
    def __init__(self):
        try:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-3GAVRKK;DATABASE=hospital;Trusted_Connection=yes;')
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            print(f"Database connection error: {e}")
            raise

    def get_patients(self):
        try:
            patients = []
            query = "SELECT * FROM Patients"
            self.cursor.execute(query)
        
            for row in self.cursor.fetchall():
                patient_dict = {
                    'PatientID': row[0],
                    'FirstName': row[1],
                    'LastName': row[2],
                    'DateOfBirth': row[3],
                    'Gender': row[4],
                    'Address': row[5],
                    'PhoneNumber': row[6],
                    'Email': row[7],
                    'BloodType': row[8],
                    'MedicalHistory': row[9],
                    'AdmissionDate': row[10],
                    'DischargeDate': row[11],
                    'RoomNumber': row[12],
                    'DoctorID': row[13]
                }
                patients.append(patient_dict)
            
            return patients
        except pyodbc.Error as e:
            print(f"Error fetching patients: {e}")
            raise
        finally:
            self.conn.close()

    def get_patient(self, patient_id):
        try:
            query = f"SELECT * FROM Patients WHERE PatientID = {patient_id}"
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                patient_dict = {
                    'PatientID': row[0],
                    'FirstName': row[1],
                    'LastName': row[2],
                    'DateOfBirth': row[3],
                    'Gender': row[4],
                    'Address': row[5],
                    'PhoneNumber': row[6],
                    'Email': row[7],
                    'BloodType': row[8],
                    'MedicalHistory': row[9],
                    'AdmissionDate': row[10],
                    'DischargeDate': row[11],
                    'RoomNumber': row[12],
                    'DoctorID': row[13]
                }
                return patient_dict
            else:
                return False
        except pyodbc.Error as e:
            print(f"Error fetching patient with ID {patient_id}: {e}")
            raise

    def add_patient(self, patient_data):
         try:
             query = f"INSERT INTO Patients (FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber, Email, BloodType, MedicalHistory, AdmissionDate, DischargeDate, RoomNumber, DoctorID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
             self.cursor.execute(query, (
             patient_data['FirstName'],
             patient_data['LastName'],
             patient_data['DateOfBirth'],
             patient_data['Gender'],
             patient_data['Address'],
             patient_data['PhoneNumber'],
             patient_data['Email'],
             patient_data['BloodType'],
             patient_data.get('MedicalHistory', None),
             patient_data.get('AdmissionDate', None),
             patient_data.get('DischargeDate', None),
             patient_data.get('RoomNumber', None),
             patient_data.get('DoctorID', None)
        ))
             self.conn.commit()
         except pyodbc.Error as e:
                print(f"Error adding patient: {e}")
                self.conn.rollback()
                raise


    def update_patient(self, patient_id, patient_data):
        try:
            query = f"UPDATE Patients SET FirstName=?, LastName=?, DateOfBirth=?, Gender=?, Address=?, PhoneNumber=?, Email=?, BloodType=?, MedicalHistory=?, AdmissionDate=?, DischargeDate=?, RoomNumber=?, DoctorID=? WHERE PatientID=?"
            self.cursor.execute(query, (
                patient_data['FirstName'],
                patient_data['LastName'],
                patient_data['DateOfBirth'],
                patient_data['Gender'],
                patient_data['Address'],
                patient_data['PhoneNumber'],
                patient_data['Email'],
                patient_data['BloodType'],
                patient_data.get('MedicalHistory', None),
                patient_data.get('AdmissionDate', None),
                patient_data.get('DischargeDate', None),
                patient_data.get('RoomNumber', None),
                patient_data.get('DoctorID', None),
                patient_id
            ))
            if self.cursor.rowcount == 0:
                return False
            else:
                self.conn.commit()
                return True
        except pyodbc.Error as e:
            print(f"Error updating patient with ID {patient_id}: {e}")
            self.conn.rollback()

    def delete_patient(self, patient_id):
        try:
            query = f"DELETE FROM Patients WHERE PatientID = ?"
            self.cursor.execute(query, (patient_id,))
            if self.cursor.rowcount == 0:
                return False
            else:
                self.conn.commit()
                return True
        except pyodbc.Error as e:
            print(f"Error deleting patient with ID {patient_id}: {e}")
            self.conn.rollback()
            raise
