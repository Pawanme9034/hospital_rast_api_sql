from flask import request
from db import PatientDatabase  # Import the PatientDatabase from db.py
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import PatientSchema  # Import the PatientSchema from schemas.py

blp = Blueprint("patients", __name__, description='Operations on patients')

@blp.route('/patient')
class Patient(MethodView):
    
    def __init__(self):
        self.db = PatientDatabase()

    @blp.response(200, PatientSchema(many=True))
    def get(self):
        patient_id = request.args.get("PatientID")
        if patient_id is None:
           return self.db.get_patients()
        else:
             result = self.db.get_patient(patient_id)
        
             if result is False:
                 return {"message": "Record not found for PatientID"}, 404  # Return appropriate message
             return [result]  # Wrap result in a list to maintain consistency



    @blp.arguments(PatientSchema)
    def post(self, request_data):
        try:
            self.db.add_patient(request_data)

            return {"msg": "Patient is added successfully"}, 201
        except Exception as e:
            return {"msg": str(e)}, 400
    
    @blp.arguments(PatientSchema)
    def put(self, request_data):
        patient_id = request.args.get("PatientID")
        if patient_id is None:
            return {"msg": "Missing 'PatientID' parameter in the request URL"}, 400
        try:
            if self.db.update_patient(patient_id, request_data):
                return {"msg": "Patient is updated successfully"}, 200
            else:
                return {"msg": "Patient with the given PatientID not found"}, 404
        except Exception as e:
            return {"msg": str(e)}, 400

    @blp.response(204)
    def delete(self):
        patient_id = request.args.get("PatientID")
        if patient_id is None:
            return {"msg": "Missing 'PatientID' parameter in the request URL"}, 400
        try:
            if self.db.delete_patient(patient_id):
                return {"msg": "Patient is deleted successfully"}, 200
            else:
                return {"msg": "Patient with the given PatientID not found"}, 404
        except Exception as e:
            return {"msg": str(e)}, 400
