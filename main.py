from db import get_database
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI()



# Conectar a la base de datos
try:
    db = get_database()
    logging.info("Conectado")
except Exception as e:
    logging.error("Error")
    
#definir el modelo de datos
class Student(BaseModel):
    name: str
    age: int

@app.post("/students")
async def create_student(student: Student):
    result = db.students.insert_one( {
        "name": student.name,
        "age": student.age
    }
    )
    return {
        "id": str(result.inserted_id),
        "massage": "Student created successfully"
    }

#buscar todos los estudiantes
@app.get("/students")
async def get_students():
    students= list(db.students.find())
    for student in students:
        student["_id"] = str(student["_id"])
    return students

#buscar por nombre
@app.get("/students/oneStudent/{name}")
async def get_one_student(name: str):
    student= db.students.find_one({"name": name}) #buscar por nombre
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    return student

#buscar por id
@app.get("/students/oneStudentbyId/{id}")
async def get_one_student_by_id(id:str):
    student = db.students.find_one({"_id": ObjectId(id)})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    return student

#buscar por nombre
@app.get("/students/{name}")
async def get_student_by_name(name: str):
    students = list(db.students.find({"name": name}))
    if not students:
        raise HTTPException(status_code=404, detail="Student not found")
    for student in students:
        student["_id"] = str(student["_id"])
    return students

#actualizar por id
@app.put("/students/updateStudent/{id}")
async def update_student(id: str, student: Student):
    try:
        obj_id = ObjectId(id)  # Convertir el string a ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = db.students.update_one({"_id": obj_id}, {"$set": {
        "name": student.name,
        "age": student.age
    }})

    if result.matched_count == 0:  # Si no encontró ningún documento con ese _id
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student updated successfully"}

#eliminar por id
@app.delete("/students/deleteStudent/{id}")
async def delete_student(id: str):
    result = db.students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
    
    
