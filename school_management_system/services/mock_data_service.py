import datetime
from typing import Dict, List, Any, Optional

from school_management_system.models.user import Role
from school_management_system.models.admission import AdmissionStatus
from school_management_system.models.exam import ExamType
from school_management_system.models.payment import PaymentStatus, PaymentMethod, FeeType
from school_management_system.models.report import ReportType
from school_management_system.models.timetable import DayOfWeek


class MockDataService:
    """
    Service for providing mock data for testing without a database connection.
    """
    
    @staticmethod
    def get_mock_users() -> List[Dict[str, Any]]:
        """
        Get mock user data.
        """
        return [
            {
                "id": 1,
                "email": "admin@example.com",
                "full_name": "Admin User",
                "is_active": True,
                "is_superuser": True,
                "role": "admin",
            },
            {
                "id": 2,
                "email": "teacher@example.com",
                "full_name": "Teacher User",
                "is_active": True,
                "is_superuser": False,
                "role": "teacher",
            },
            {
                "id": 3,
                "email": "parent@example.com",
                "full_name": "Parent User",
                "is_active": True,
                "is_superuser": False,
                "role": "parent",
            },
        ]
    
    @staticmethod
    def get_mock_students() -> List[Dict[str, Any]]:
        """
        Get mock student data.
        """
        return [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": datetime.date(2010, 5, 15),
                "gender": "Male",
                "enrollment_date": datetime.date(2023, 9, 1),
                "grade_level": "Grade 5",
                "student_id": "ST001",
                "address": "123 Main St, City",
                "phone_number": "123-456-7890",
                "email": "john.doe@example.com",
                "is_active": True,
                "parent_id": 3,
            },
            {
                "id": 2,
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": datetime.date(2011, 8, 22),
                "gender": "Female",
                "enrollment_date": datetime.date(2023, 9, 1),
                "grade_level": "Grade 4",
                "student_id": "ST002",
                "address": "456 Oak St, City",
                "phone_number": "234-567-8901",
                "email": "jane.smith@example.com",
                "is_active": True,
                "parent_id": 3,
            },
        ]
    
    @staticmethod
    def get_mock_admissions() -> List[Dict[str, Any]]:
        """
        Get mock admission data.
        """
        return [
            {
                "id": 1,
                "application_date": datetime.date(2023, 6, 15),
                "status": AdmissionStatus.APPROVED,
                "desired_grade_level": "Grade 5",
                "previous_school": "Previous Elementary School",
                "previous_grade_level": "Grade 4",
                "notes": "Good academic record",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": datetime.date(2010, 5, 15),
                "gender": "Male",
                "address": "123 Main St, City",
                "phone_number": "123-456-7890",
                "email": "john.doe@example.com",
                "parent_name": "Parent Doe",
                "parent_phone": "987-654-3210",
                "parent_email": "parent.doe@example.com",
                "parent_address": "123 Main St, City",
                "relationship_to_applicant": "Father",
                "student_id": 1,
            },
            {
                "id": 2,
                "application_date": datetime.date(2023, 6, 20),
                "status": AdmissionStatus.APPROVED,
                "desired_grade_level": "Grade 4",
                "previous_school": "Previous Elementary School",
                "previous_grade_level": "Grade 3",
                "notes": "Good academic record",
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": datetime.date(2011, 8, 22),
                "gender": "Female",
                "address": "456 Oak St, City",
                "phone_number": "234-567-8901",
                "email": "jane.smith@example.com",
                "parent_name": "Parent Smith",
                "parent_phone": "876-543-2109",
                "parent_email": "parent.smith@example.com",
                "parent_address": "456 Oak St, City",
                "relationship_to_applicant": "Mother",
                "student_id": 2,
            },
        ]
    
    @staticmethod
    def get_mock_subjects() -> List[Dict[str, Any]]:
        """
        Get mock subject data.
        """
        return [
            {
                "id": 1,
                "name": "Mathematics",
                "code": "MATH101",
                "description": "Basic mathematics for elementary students",
                "grade_level": "Grade 5",
                "credits": 5,
                "is_active": True,
                "teacher_id": 2,
            },
            {
                "id": 2,
                "name": "Science",
                "code": "SCI101",
                "description": "Basic science for elementary students",
                "grade_level": "Grade 5",
                "credits": 4,
                "is_active": True,
                "teacher_id": 2,
            },
            {
                "id": 3,
                "name": "English",
                "code": "ENG101",
                "description": "English language and literature",
                "grade_level": "Grade 5",
                "credits": 5,
                "is_active": True,
                "teacher_id": 2,
            },
        ]
    
    @staticmethod
    def get_mock_timetables() -> List[Dict[str, Any]]:
        """
        Get mock timetable data.
        """
        return [
            {
                "id": 1,
                "name": "Grade 5 Timetable",
                "description": "Timetable for Grade 5 students",
                "academic_year": "2023-2024",
                "term": "Fall",
                "grade_level": "Grade 5",
                "section": "A",
                "is_active": True,
            },
        ]
    
    @staticmethod
    def get_mock_timetable_slots() -> List[Dict[str, Any]]:
        """
        Get mock timetable slot data.
        """
        return [
            {
                "id": 1,
                "day": DayOfWeek.MONDAY,
                "start_time": datetime.time(8, 0),
                "end_time": datetime.time(9, 0),
                "room_number": "101",
                "timetable_id": 1,
                "subject_id": 1,
                "teacher_id": 2,
            },
            {
                "id": 2,
                "day": DayOfWeek.MONDAY,
                "start_time": datetime.time(9, 0),
                "end_time": datetime.time(10, 0),
                "room_number": "102",
                "timetable_id": 1,
                "subject_id": 2,
                "teacher_id": 2,
            },
            {
                "id": 3,
                "day": DayOfWeek.MONDAY,
                "start_time": datetime.time(10, 0),
                "end_time": datetime.time(11, 0),
                "room_number": "103",
                "timetable_id": 1,
                "subject_id": 3,
                "teacher_id": 2,
            },
        ]
    
    @staticmethod
    def get_mock_exams() -> List[Dict[str, Any]]:
        """
        Get mock exam data.
        """
        return [
            {
                "id": 1,
                "name": "Mathematics Midterm",
                "description": "Midterm exam for Mathematics",
                "exam_type": ExamType.MIDTERM,
                "date": datetime.date(2023, 10, 15),
                "start_time": "09:00",
                "end_time": "11:00",
                "total_marks": 100.0,
                "passing_marks": 40.0,
                "grade_level": "Grade 5",
                "academic_year": "2023-2024",
                "term": "Fall",
                "instructions": "Answer all questions",
            },
            {
                "id": 2,
                "name": "Science Midterm",
                "description": "Midterm exam for Science",
                "exam_type": ExamType.MIDTERM,
                "date": datetime.date(2023, 10, 17),
                "start_time": "09:00",
                "end_time": "11:00",
                "total_marks": 100.0,
                "passing_marks": 40.0,
                "grade_level": "Grade 5",
                "academic_year": "2023-2024",
                "term": "Fall",
                "instructions": "Answer all questions",
            },
        ]
    
    @staticmethod
    def get_mock_exam_results() -> List[Dict[str, Any]]:
        """
        Get mock exam result data.
        """
        return [
            {
                "id": 1,
                "score": 85.0,
                "grade": "A",
                "remarks": "Excellent work",
                "student_id": 1,
                "exam_id": 1,
                "subject_id": 1,
            },
            {
                "id": 2,
                "score": 78.0,
                "grade": "B",
                "remarks": "Good work",
                "student_id": 1,
                "exam_id": 2,
                "subject_id": 2,
            },
        ]
    
    @staticmethod
    def get_mock_fee_structures() -> List[Dict[str, Any]]:
        """
        Get mock fee structure data.
        """
        return [
            {
                "id": 1,
                "name": "Grade 5 Fee Structure",
                "description": "Fee structure for Grade 5 students",
                "academic_year": "2023-2024",
                "grade_level": "Grade 5",
                "is_active": True,
            },
        ]
    
    @staticmethod
    def get_mock_fee_items() -> List[Dict[str, Any]]:
        """
        Get mock fee item data.
        """
        return [
            {
                "id": 1,
                "name": "Tuition Fee",
                "description": "Tuition fee for the academic year",
                "fee_type": FeeType.TUITION,
                "amount": 5000.0,
                "due_date": datetime.date(2023, 9, 15),
                "is_mandatory": True,
                "fee_structure_id": 1,
            },
            {
                "id": 2,
                "name": "Library Fee",
                "description": "Library fee for the academic year",
                "fee_type": FeeType.LIBRARY,
                "amount": 500.0,
                "due_date": datetime.date(2023, 9, 15),
                "is_mandatory": True,
                "fee_structure_id": 1,
            },
        ]
    
    @staticmethod
    def get_mock_fee_records() -> List[Dict[str, Any]]:
        """
        Get mock fee record data.
        """
        return [
            {
                "id": 1,
                "academic_year": "2023-2024",
                "term": "Fall",
                "total_amount": 5500.0,
                "paid_amount": 5500.0,
                "balance": 0.0,
                "status": PaymentStatus.PAID,
                "due_date": datetime.date(2023, 9, 15),
                "student_id": 1,
                "fee_structure_id": 1,
            },
            {
                "id": 2,
                "academic_year": "2023-2024",
                "term": "Fall",
                "total_amount": 5500.0,
                "paid_amount": 3000.0,
                "balance": 2500.0,
                "status": PaymentStatus.PARTIALLY_PAID,
                "due_date": datetime.date(2023, 9, 15),
                "student_id": 2,
                "fee_structure_id": 1,
            },
        ]
    
    @staticmethod
    def get_mock_payments() -> List[Dict[str, Any]]:
        """
        Get mock payment data.
        """
        return [
            {
                "id": 1,
                "amount": 5500.0,
                "payment_date": datetime.datetime(2023, 9, 10, 10, 0),
                "payment_method": PaymentMethod.BANK_TRANSFER,
                "transaction_id": "TXN123456",
                "receipt_number": "REC123456",
                "notes": "Full payment",
                "fee_record_id": 1,
            },
            {
                "id": 2,
                "amount": 3000.0,
                "payment_date": datetime.datetime(2023, 9, 12, 11, 0),
                "payment_method": PaymentMethod.CASH,
                "transaction_id": None,
                "receipt_number": "REC123457",
                "notes": "Partial payment",
                "fee_record_id": 2,
            },
        ]
    
    @staticmethod
    def get_mock_reports() -> List[Dict[str, Any]]:
        """
        Get mock report data.
        """
        return [
            {
                "id": 1,
                "title": "Attendance Report",
                "description": "Monthly attendance report",
                "report_type": ReportType.ATTENDANCE,
                "created_at": datetime.datetime(2023, 10, 1, 9, 0),
                "created_by": 1,
                "parameters": '{"month": "September", "year": "2023"}',
                "file_path": "/reports/attendance_report_202309.pdf",
                "is_scheduled": True,
                "schedule_frequency": "Monthly",
                "last_run": datetime.datetime(2023, 10, 1, 9, 0),
                "next_run": datetime.datetime(2023, 11, 1, 9, 0),
            },
            {
                "id": 2,
                "title": "Academic Report",
                "description": "Term academic report",
                "report_type": ReportType.ACADEMIC,
                "created_at": datetime.datetime(2023, 10, 5, 10, 0),
                "created_by": 1,
                "parameters": '{"term": "Fall", "year": "2023"}',
                "file_path": "/reports/academic_report_2023_fall.pdf",
                "is_scheduled": False,
                "schedule_frequency": None,
                "last_run": datetime.datetime(2023, 10, 5, 10, 0),
                "next_run": None,
            },
        ]
    
    @classmethod
    def get_mock_data(cls, model_name: str) -> List[Dict[str, Any]]:
        """
        Get mock data for a specific model.
        """
        mock_data_methods = {
            "users": cls.get_mock_users,
            "students": cls.get_mock_students,
            "admissions": cls.get_mock_admissions,
            "subjects": cls.get_mock_subjects,
            "timetables": cls.get_mock_timetables,
            "timetable_slots": cls.get_mock_timetable_slots,
            "exams": cls.get_mock_exams,
            "exam_results": cls.get_mock_exam_results,
            "fee_structures": cls.get_mock_fee_structures,
            "fee_items": cls.get_mock_fee_items,
            "fee_records": cls.get_mock_fee_records,
            "payments": cls.get_mock_payments,
            "reports": cls.get_mock_reports,
        }
        
        if model_name in mock_data_methods:
            return mock_data_methods[model_name]()
        
        return []
    
    @classmethod
    def get_mock_item_by_id(cls, model_name: str, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a mock item by ID.
        """
        items = cls.get_mock_data(model_name)
        for item in items:
            if item["id"] == item_id:
                return item
        
        return None
