from db import get_database
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from typing import List

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
    
#definir el modelo de datos Student
class Student(BaseModel):
    name: str
    age: int

#definir el modelo de datos Course
class Course(BaseModel):
    name: str
    facultad: str
    alumnos: list[Student]



#crear un estudiante
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
    logger.info("Received request to get all students")
    students = list(db.students.find())
    for student in students:
        student["_id"] = str(student["_id"])
    logger.info(f"Returning {len(students)} students")
    return students

#buscar por nombre
@app.get("/students/oneStudent/{name}")
async def get_one_student(name: str):
    logger.info(f"Received request to get one student with name: {name}")
    student = db.students.find_one({"name": name})
    if student is None:
        logger.warning(f"Student not found with name: {name}")
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    logger.info(f"Returning student with name: {name}")
    return student

#buscar por id
@app.get("/students/oneStudentbyId/{id}")
async def get_one_student_by_id(id: str):
    logger.info(f"Received request to get student by ID: {id}")
    student = db.students.find_one({"_id": ObjectId(id)})
    if student is None:
        logger.warning(f"Student not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    logger.info(f"Returning student with ID: {id}")
    return student

#buscar estudiantes que tengan el mismo nombre
@app.get("/students/{name}")
async def get_student_by_name(name: str):
    logger.info(f"Received request to get students with name: {name}")
    students = list(db.students.find({"name": name}))
    if not students:
        logger.warning(f"No students found with name: {name}")
        raise HTTPException(status_code=404, detail="Student not found")
    for student in students:
        student["_id"] = str(student["_id"])
    logger.info(f"Returning {len(students)} students with name: {name}")
    return students

#actualizar por id
@app.put("/students/updateStudent/{id}")
async def update_student(id: str, student: Student):
    logger.info(f"Received request to update student with ID: {id}")
    try:
        obj_id = ObjectId(id)
    except Exception:
        logger.error(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = db.students.update_one({"_id": obj_id}, {"$set": {
        "name": student.name,
        "age": student.age
    }})

    if result.matched_count == 0:
        logger.warning(f"Student not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Student not found")

    logger.info(f"Student with ID: {id} updated successfully")
    return {"message": "Student updated successfully"}

#eliminar por id
@app.delete("/students/deleteStudent/{id}")
async def delete_student(id: str):
    logger.info(f"Received request to delete student with ID: {id}")
    result = db.students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        logger.warning(f"Student not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Student not found")
    logger.info(f"Student with ID: {id} deleted successfully")
    return {"message": "Student deleted successfully"}
    
#buscar todos los cursos
@app.get("/courses")
async def get_courses():
    logger.info("Received request to get all courses")
    courses = list(db.courses.find())
    for course in courses:
        course["_id"] = str(course["_id"])
    logger.info(f"Returning {len(courses)} courses")
    return courses

#buscar un curso por id
@app.get("/courses/oneCourse/{id}")
async def get_one_course(id: str):
    logger.info(f"Received request to get one course with ID: {id}")
    course = db.courses.find_one({"_id": ObjectId(id)})

    if course is None:
        logger.warning(f"Course not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Course not found")
    course["_id"] = str(course["_id"])
    logger.info(f"Returning course with ID: {id}")
    return course

#buscar cursos por nombre
@app.get("/courses/{name}")
async def get_course_by_name(name: str):
    logger.info(f"Received request to get courses with name: {name}")
    courses = list(db.courses.find({"name": name}))
    if not courses:
        logger.warning(f"No courses found with name: {name}")
        raise HTTPException(status_code=404, detail="Course not found")
    for course in courses:
        course["_id"] = str(course["_id"])
    logger.info(f"Returning {len(courses)} courses with name: {name}")
    return courses

#crear un curso
@app.post("/courses")
async def create_course(course: Course):
    logger.info(f"Received request to create a new course")
    result = db.courses.insert_one( {
        "name": course.name,
        "facultad": course.facultad,
        "alumnos": course.alumnos
    }
    )
    return {
        "id": str(result.inserted_id),
        "message": "Course created successfully"
    }

#actualizar un curso por id
@app.put("/courses/updateCourse/{id}")
async def update_course(id: str, course: Course):
    logger.info(f"Received request to update course with ID: {id}")
    try:
        obj_id = ObjectId(id)
    except Exception:
        logger.error(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = db.courses.update_one({"_id": obj_id}, {"$set": {
        "name": course.name,
        "facultad": course.facultad,
        "alumnos": course.alumnos
    }})

    if result.matched_count == 0:
        logger.warning(f"Course not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Course not found")

    logger.info(f"Course with ID: {id} updated successfully")
    return {"message": "Course updated successfully"}

#eliminar un curso por id
@app.delete("/courses/deleteCourse/{id}")
async def delete_course(id: str):
    logger.info(f"Received request to delete course with ID: {id}")
    result = db.courses.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        logger.warning(f"Course not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Course not found")
    logger.info(f"Course with ID: {id} deleted successfully")
    return {"message": "Course deleted successfully"}


#agregar un estudiante a un curso
@app.put("/courses/{course_id}/add_student_ids")
async def add_student_ids_to_course(course_id: str, student_ids: List[str]):
    logger.info(f"Received request to add student IDs to course with ID: {course_id}")
    try:
        course_obj_id = ObjectId(course_id)
    except Exception:
        logger.error(f"Invalid course ID format: {course_id}")
        raise HTTPException(status_code=400, detail="Invalid course ID format")

    # Verificar que todos los IDs de estudiantes sean válidos
    try:
        student_obj_ids = [ObjectId(student_id) for student_id in student_ids]
    except Exception:
        logger.error("One or more student IDs are invalid")
        raise HTTPException(status_code=400, detail="Invalid student ID format")

    # Verificar que los estudiantes existan
    existing_students = list(db.students.find({"_id": {"$in": student_obj_ids}}))
    if len(existing_students) != len(student_ids):
        logger.warning("Some student IDs do not exist")
        raise HTTPException(status_code=404, detail="Some student IDs do not exist")

    # Actualizar el curso agregando los IDs de los estudiantes
    result = db.courses.update_one(
        {"_id": course_obj_id},
        {"$addToSet": {"alumnos": {"$each": student_ids}}}
    )

    if result.matched_count == 0:
        logger.warning(f"Course not found with ID: {course_id}")
        raise HTTPException(status_code=404, detail="Course not found")

    logger.info(f"Student IDs added to course with ID: {course_id} successfully")
    return {"message": "Student IDs added successfully"}

#ver alumnos de un curso con los atributos de los estudiantes
@app.get("/courses/{course_id}/students")
async def get_students_by_course(course_id: str):
    logger.info(f"Received request to get students by course with ID: {course_id}")
    
    # Buscar el curso por su ID
    course = db.courses.find_one({"_id": ObjectId(course_id)})
    if course is None:
        logger.warning(f"Course not found with ID: {course_id}")
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Obtener los IDs de los estudiantes del curso
    student_ids = course.get("alumnos", [])
    
    # Convertir los IDs a ObjectId
    student_obj_ids = [ObjectId(student_id) for student_id in student_ids]
    
    # Buscar los detalles de los estudiantes
    students = list(db.students.find({"_id": {"$in": student_obj_ids}}))
    
    # Convertir el _id de cada estudiante a string
    for student in students:
        student["_id"] = str(student["_id"])
    
    # Reemplazar los IDs de los estudiantes con los documentos completos
    course["alumnos"] = students
    course["_id"] = str(course["_id"])
    
    logger.info(f"Returning students for course with ID: {course_id}")
    return course














