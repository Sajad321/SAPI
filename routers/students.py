from fastapi import APIRouter
from Models import session, engine, Base, Insitute, Student, Student_Installment, Installment
from typing import Optional
import json

router = APIRouter()


# To get Insitutes Number , Students
@router.get("/main-admin")
def main_admin():
    students = session.query(Student)
    institutes = session.query(Insitute)

    result = {
        "Response": "OK",
        "students_count": students.count(),
        "institutes_count": institutes.count(),
        "insitutes": []

    }
    child = {}
    for insitute in institutes:
        print(insitute.format())
        child['id'] = insitute.format()['id']
        child['name'] = insitute.format()['name']
        student_count = students.filter_by(insitute_id=insitute.format()['id']).count()
        child['Students_institute_count'] = student_count
        result['insitutes'].append(child)
        child = {}
    return result

# To insert Insitute
@router.post("/insitute")
def insituteInsert(name: str):
    new = Insitute(name=name)
    Insitute.insert(new)

    return {"Response": "Done"}


# To insert Student
@router.post("/studentInsert")
def studentInsert(name: str, batch: int, dob: Optional[str], insitute_id: int, phone: Optional[int], qr: str,
                  picture: Optional[str], note: Optional[str] = "لا يوجد"):
    newstudent = Student(name=name, dob=dob, insitute_id=insitute_id, phone=phone, qr=qr, note=note,
                         picture=picture, batch=batch)
    Student.insert(newstudent)
    return {"Response": "Done"}


# To get students info by insitute and batch
@router.get("/studentInfo/<int:insitute_id>/<int:batch>")
def studentInfo(insitute_id, batch):
    studentJoin = session.query(Student).join(Insitute, Student.insitute_id == Insitute.id).filter(
        Student.insitute_id == insitute_id, Student.batch == batch).all()

    studentsinfo1 = [stu.format() for stu in studentJoin]

    return studentsinfo1


# to get intallement of students by student id and install id
@router.get("/studentInstallementbyid")
def installStudent(student_id, install_id):
    installstudent = session.query(Student_Installment).join(Student, Student_Installment.student_id == Student.id).join(
        Installment, Student_Installment.installment_id == Installment.id)
    query = installstudent.filter(Student_Installment.student_id ==
                                  student_id, Student_Installment.installment_id == install_id).all()
    liststudentinstall = [inst.format() for inst in query]
    return liststudentinstall


# To insert Installment

@router.post("/installmentInsert")
def installmentInsert(name: str, date: str, insitute_id: int):
    new = Installment(name=name, date=date, insitute_id=insitute_id)
    Installment.insert(new)
    return {"Response": "Done"}


# To insert student Installment

@router.post("/studentInstllinsert")
def studentInstallinsert(student_id: int, install_id: int, received: str, insitute_id):
    received = json.loads(received.lower())
    new = Student_Installment(
        student_id=student_id, installment_id=install_id, received=received, insitute_id=insitute_id)
    Student_Installment.insert(new)
    return {
        "Response": "OK"
    }

# To get students installements bulky


@router.get("/studentInstall")
def studentInstall():
    # query = session.query(Student_Installment).join(Installment, Installment.id == Student_Installment.installment_id).join(
    #    Insitute, Insitute.id == Student_Installment.insitute_id).join(Student, Student.id == Student_Installment.student_id)
    #query = query.filter(Student_Installment.insitute_id == insitute_id).all()
    installment = {}
    query = session.query(Student).all()
    query2 = session.query(Student_Installment)
    query3 = session.query(Installment).all()
    studen_json = {
        "Students": [], "Installments": []
    }
    student = {}
    installNum = 1
    installl = {}
    for stu in query:
        student['id'] = stu.format()['id']
        student['name'] = stu.format()['name']
        student["insitute_id"] = stu.format()['insitute_id']
        student_id = stu.format()['id']
        print()
        for install in query2.filter_by(student_id=student_id):
            if install.received()['received']:
                installl[installNum] = "true"
            else:
                installl[installNum] = "false"
            student["installment_received"] = installl

            installNum += 1
        installl = {}
        studen_json['Students'].append(student)
        student = {}
        installNum = 1
    for install in query3:
        installment['id'] = install.format()['id']
        installment['name'] = install.format()['name']
        installment['insitute_id'] = install.format()['insitute_id']
        installment['insitute_name'] = install.format()['insitute_name']
        installment['date'] = install.format()['date']
        studen_json['Installments'].append(installment)
        installment = {}
    return studen_json
