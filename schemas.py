from marshmallow import Schema, fields

class PatientSchema(Schema):
    PatientID = fields.Int(required=True)
    FirstName = fields.Str(required=True)
    LastName = fields.Str(required=True)
    DateOfBirth = fields.Date(required=True)
    Gender = fields.Str(required=True)
    Address = fields.Str(required=True)
    PhoneNumber = fields.Str(required=True)
    Email = fields.Email(required=True)
    BloodType = fields.Str(required=True)
    MedicalHistory = fields.Str(required=False)
    AdmissionDate = fields.DateTime(required=False)
    DischargeDate = fields.DateTime(required=False)
    RoomNumber = fields.Int(required=False)
    DoctorID = fields.Int(required=False)
