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

#definir el modelo de datos University
class University(BaseModel):
    name: str
    carreras: list[str]

#definir el modelo de datos Patents
class Patents(BaseModel):
    name: str
    contributors: list[str]
    date: str
    uri: str
    url:str
    summary:str

#definir el modelo de datos Scientists
class Scientists(BaseModel):
    name: str
    email: str
    category:str
    cneaiField:str
    universities:list[str]

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


#crear una universidad
@app.post("/universities")
async def create_university(university: University):
    logger.info(f"Received request to create a new university")
    result = db.universities.insert_one( {
        "name": university.name,
        "carreras": university.carreras
    }
    )
    return {
        "id": str(result.inserted_id),
        "message": "University created successfully"
    }

#buscar una universidad por id
@app.get("/universities/oneUniversity/{id}")
async def get_one_university(id: str):
    logger.info(f"Received request to get one university with ID: {id}")
    university = db.universities.find_one({"_id": ObjectId(id)})
    if university is None:
        logger.warning(f"University not found with ID: {id}")
        raise HTTPException(status_code=404, detail="University not found")
    university["_id"] = str(university["_id"])
    logger.info(f"Returning university with ID: {id}")
    return university

#buscar una universidad por nombre
@app.get("/universities/{name}")
async def get_university_by_name(name: str):
    logger.info(f"Received request to get universities with name: {name}")
    universities = list(db.universities.find({"name": name}))
    if not universities:
        logger.warning(f"No universities found with name: {name}")
        raise HTTPException(status_code=404, detail="University not found")
    for university in universities:
        university["_id"] = str(university["_id"])
    logger.info(f"Returning {len(universities)} universities with name: {name}")
    return universities

#actualizar una universidad por id
@app.put("/universities/updateUniversity/{id}")
async def update_university(id: str, university: University):
    logger.info(f"Received request to update university with ID: {id}")
    try:
        obj_id = ObjectId(id)
    except Exception:
        logger.error(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = db.universities.update_one({"_id": obj_id}, {"$set": {
        "name": university.name,
        "carreras": university.carreras
    }})

    if result.matched_count == 0:
        logger.warning(f"University not found with ID: {id}")
        raise HTTPException(status_code=404, detail="University not found")

    logger.info(f"University with ID: {id} updated successfully")
    return {"message": "University updated successfully"}

#eliminar una universidad por id
@app.delete("/universities/deleteUniversity/{id}")
async def delete_university(id: str):
    logger.info(f"Received request to delete university with ID: {id}")
    result = db.universities.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        logger.warning(f"University not found with ID: {id}")
        raise HTTPException(status_code=404, detail="University not found")
    logger.info(f"University with ID: {id} deleted successfully")
    return {"message": "University deleted successfully"}


#agregar una carrera a una universidad
@app.put("/universities/{university_id}/add")
async def add_carrera_to_university(university_id: str, carrera_ids: List[str]):
    logger.info(f"Received request to add carreras to university with ID: {university_id}")

    try:
        university_obj_id = ObjectId(university_id)
    except Exception:           
        logger.error(f"Invalid university ID format: {university_id}")
        raise HTTPException(status_code=400, detail="Invalid university ID format")

    # Verificar que la universidad exista
    university = db.universities.find_one({"_id": university_obj_id})
    if university is None:
        logger.warning(f"University not found with ID: {university_id}")
        raise HTTPException(status_code=404, detail="University not found")

    # Verificar que las carreras existan
    carrera_obj_ids = [ObjectId(carrera_id) for carrera_id in carrera_ids]
    existing_carreras = list(db.courses.find({"_id": {"$in": carrera_obj_ids}}))

    if len(existing_carreras) != len(carrera_ids):
        logger.warning("Some carreras IDs do not exist")
        raise HTTPException(status_code=404, detail="Some carrera IDs do not exist")

    # Agregar las carreras a la universidad
    result = db.universities.update_one(
        {"_id": university_obj_id},
        {"$addToSet": {"carreras": {"$each": carrera_ids}}}
    )

    if result.matched_count == 0:
        logger.warning(f"University not found with ID: {university_id}")
        raise HTTPException(status_code=404, detail="University not found")

    logger.info(f"Carreras added to university with ID: {university_id} successfully")
    return {"message": "Carreras added successfully"}


#buscar carreras de una universidad por sus atributos
@app.get("/universities/{university_id}/carreras")
async def get_carreras_by_university(university_id: str):
    logger.info(f"Received request to get carreras by university with ID: {university_id}")

    try:
        university_obj_id = ObjectId(university_id)
    except Exception:
        logger.error(f"Invalid university ID format: {university_id}")
        raise HTTPException(status_code=400, detail="Invalid university ID format")

    # Buscar la universidad por su ID
    university = db.universities.find_one({"_id": university_obj_id})
    if university is None:
        logger.warning(f"University not found with ID: {university_id}")
        raise HTTPException(status_code=404, detail="University not found")

    # Obtener los IDs de las carreras de la universidad
    carrera_ids = university.get("carreras", [])

    # Convertir los IDs a ObjectId
    carrera_obj_ids = [ObjectId(carrera_id) for carrera_id in carrera_ids]

    # Buscar los detalles de las carreras
    carreras = list(db.courses.find({"_id": {"$in": carrera_obj_ids}}))

    # Convertir el _id de cada carrera a string
    for carrera in carreras:
        carrera["_id"] = str(carrera["_id"])

    # Reemplazar los IDs de las carreras con los documentos completos
    university["carreras"] = carreras
    university["_id"] = str(university["_id"])

    logger.info(f"Returning carreras for university with ID: {university_id}")
    return university

#crear un cientifico
@app.post("/scientists")
async def create_scientist(scientist: Scientists):
    logger.info(f"Received request to create a new scientist")
    result = db.scientists.insert_one( {
        "name": scientist.name,
        "email": scientist.email,
        "category": scientist.category,
        "cneaiField": scientist.cneaiField,
        "universities": scientist.universities
    }
    )
    return {
        "id": str(result.inserted_id),
        "message": "Scientist created successfully"
    }
    
#buscar un cientifico por id
@app.get("/scientists/oneScientist/{id}")
async def get_one_scientist(id: str):
    logger.info(f"Received request to get one scientist with ID: {id}")
    scientist = db.scientists.find_one({"_id": ObjectId(id)})
    if scientist is None:
        logger.warning(f"Scientist not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Scientist not found")
    scientist["_id"] = str(scientist["_id"])
    logger.info(f"Returning scientist with ID: {id}")
    return scientist

#buscar un cientifico por nombre
@app.get("/scientists/{name}")
async def get_scientist_by_name(name: str):
    logger.info(f"Received request to get scientists with name: {name}")
    scientists = list(db.scientists.find({"name": name}))
    if not scientists:
        logger.warning(f"No scientists found with name: {name}")
        raise HTTPException(status_code=404, detail="Scientist not found")
    for scientist in scientists:
        scientist["_id"] = str(scientist["_id"])
    logger.info(f"Returning {len(scientists)} scientists with name: {name}")
    return scientists

#actualizar un cientifico por id
@app.put("/scientists/updateScientist/{id}")
async def update_scientist(id: str, scientist: Scientists):
    logger.info(f"Received request to update scientist with ID: {id}")
    try:
        obj_id = ObjectId(id)
    except Exception:
        logger.error(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = db.scientists.update_one({"_id": obj_id}, {"$set": {
        "name": scientist.name,
        "email": scientist.email,
        "category": scientist.category,
        "cneaiField": scientist.cneaiField,
        "universities": scientist.universities
    }})

    if result.matched_count == 0:
        logger.warning(f"Scientist not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Scientist not found")

    logger.info(f"Scientist with ID: {id} updated successfully")
    return {"message": "Scientist updated successfully"}

#eliminar un cientifico por id
@app.delete("/scientists/deleteScientist/{id}")
async def delete_scientist(id: str):
    logger.info(f"Received request to delete scientist with ID: {id}")
    result = db.scientists.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        logger.warning(f"Scientist not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Scientist not found")
    logger.info(f"Scientist with ID: {id} deleted successfully")
    return {"message": "Scientist deleted successfully"}

#crear una patente
@app.post("/patents")
async def create_patent(patent: Patents):
    logger.info(f"Received request to create a new patent")
    result = db.patents.insert_one( {
        "name": patent.name,
        "contributors": patent.contributors,
        "date": patent.date,
        "uri": patent.uri,
        "url": patent.url,
        "summary": patent.summary
    }
    )
    return {
        "id": str(result.inserted_id),
        "message": "Patent created successfully"
    }

#buscar una patente por id
@app.get("/patents/onePatent/{id}")
async def get_one_patent(id: str):
    logger.info(f"Received request to get one patent with ID: {id}")
    patent = db.patents.find_one({"_id": ObjectId(id)})
    if patent is None:
        logger.warning(f"Patent not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Patent not found")
    patent["_id"] = str(patent["_id"])
    logger.info(f"Returning patent with ID: {id}")
    return patent

#buscar una patente por nombre
@app.get("/patents/{name}")
async def get_patent_by_name(name: str):
    logger.info(f"Received request to get patents with name: {name}")
    patents = list(db.patents.find({"name": name}))
    if not patents:
        logger.warning(f"No patents found with name: {name}")
        raise HTTPException(status_code=404, detail="Patent not found")
    for patent in patents:
        patent["_id"] = str(patent["_id"])
    logger.info(f"Returning {len(patents)} patents with name: {name}")
    return patents

#actualizar una patente por id
@app.put("/patents/updatePatent/{id}")
async def update_patent(id: str, patent: Patents):
    logger.info(f"Received request to update patent with ID: {id}")
    try:
        obj_id = ObjectId(id)
    except Exception:   
        logger.error(f"Invalid ID format: {id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = db.patents.update_one({"_id": obj_id}, {"$set": {
        "name": patent.name,
        "contributors": patent.contributors,
        "date": patent.date,
        "uri": patent.uri,
        "url": patent.url,
        "summary": patent.summary
    }})

    if result.matched_count == 0:
        logger.warning(f"Patent not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Patent not found")

    logger.info(f"Patent with ID: {id} updated successfully")
    return {"message": "Patent updated successfully"}

#eliminar una patente por id
@app.delete("/patents/deletePatent/{id}")
async def delete_patent(id: str):
    logger.info(f"Received request to delete patent with ID: {id}")
    result = db.patents.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        logger.warning(f"Patent not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Patent not found")
    logger.info(f"Patent with ID: {id} deleted successfully")
    return {"message": "Patent deleted successfully"}





        
    
    
    

    

    
    





    
    
    


    


        









        

















