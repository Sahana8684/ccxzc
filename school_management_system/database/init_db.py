import logging
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from school_management_system.database.base import Base
from school_management_system.database.session import get_engine_for_init, AsyncSessionLocal
from school_management_system.models.user import User
from school_management_system.utils.security import get_password_hash
from school_management_system.config import settings

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """
    Initialize the database:
    - Create tables if they don't exist
    - Create initial superuser if it doesn't exist
    """
    # Get the engine for initialization
    engine = get_engine_for_init()
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create initial superuser
    try:
        await create_initial_superuser()
    except Exception as e:
        logger.error(f"Error creating superuser: {e}")
        # Don't raise the exception, just log it
    
    # Create sample data if using in-memory database
    # Only create sample data in development or if explicitly requested in Vercel
    if settings.USE_SQLITE_MEMORY and (not os.environ.get("RENDER") or os.environ.get("SERVERLESS") or os.environ.get("CREATE_SAMPLE_DATA") == "true"):
        try:
            await create_sample_data()
        except Exception as e:
            logger.error(f"Error creating sample data: {e}")
            # Don't raise the exception, just log it
    
    logger.info("Database initialized successfully")


async def create_initial_superuser() -> None:
    """
    Create initial superuser if it doesn't exist.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Check if superuser already exists
            if settings.USE_SQLITE_MEMORY:
                # For SQLite, use SQLAlchemy ORM query
                result = await session.execute(
                    select(User).where(User.email == settings.FIRST_SUPERUSER)
                )
                user = result.scalars().first()
                user_id = user.id if user else None
            else:
                # For PostgreSQL, use raw SQL
                result = await session.execute(
                    "SELECT id FROM users WHERE email = :email", 
                    {"email": settings.FIRST_SUPERUSER}
                )
                user_id = result.scalar_one_or_none()
            
            if user_id is None:
                # Create superuser with a shorter password
                password = "admin"  # Short password for testing
                superuser = User(
                    email=settings.FIRST_SUPERUSER,
                    hashed_password=get_password_hash(password),
                    full_name="Initial Admin",
                    is_superuser=True,
                    is_active=True,
                )
                session.add(superuser)
                await session.commit()
                logger.info(f"Superuser {settings.FIRST_SUPERUSER} created with password: {password}")
            else:
                logger.info(f"Superuser {settings.FIRST_SUPERUSER} already exists")
    except Exception as e:
        logger.error(f"Error creating superuser: {e}")
        # Don't raise the exception, just log it


async def create_sample_data() -> None:
    """
    Create sample data for testing when using in-memory database.
    """
    try:
        from school_management_system.services.mock_data_service import MockDataService
        from school_management_system.models.user import User, Role
        from school_management_system.models.student import Student
        from school_management_system.models.admission import Admission
        from school_management_system.models.subject import Subject
        from school_management_system.models.timetable import Timetable, TimetableSlot
        from school_management_system.models.exam import Exam, ExamResult, ExamType
        from school_management_system.models.payment import FeeStructure, FeeItem, FeeRecord, Payment
        from school_management_system.models.report import Report
        
        logger.info("Creating sample data for testing...")
        
        # Create roles first
        admin_role = Role(name="admin", description="Administrator role")
        teacher_role = Role(name="teacher", description="Teacher role")
        parent_role = Role(name="parent", description="Parent role")
        
        # Create users with roles
        admin_user = User(
            email="admin@example.com",
            full_name="Admin User",
            is_active=True,
            is_superuser=True,
            hashed_password=get_password_hash("admin"),  # Short password for testing
        )
        
        teacher_user = User(
            email="teacher@example.com",
            full_name="Teacher User",
            is_active=True,
            is_superuser=False,
            hashed_password=get_password_hash("teacher"),  # Short password for testing
        )
        
        parent_user = User(
            email="parent@example.com",
            full_name="Parent User",
            is_active=True,
            is_superuser=False,
            hashed_password=get_password_hash("parent"),  # Short password for testing
        )
        
        # Create sample data
        async with AsyncSessionLocal() as session:
            # Add roles
            session.add(admin_role)
            session.add(teacher_role)
            session.add(parent_role)
            await session.flush()
            
            # Add users
            session.add(admin_user)
            session.add(teacher_user)
            session.add(parent_user)
            await session.flush()
            
            # Add roles to users
            admin_user.roles.append(admin_role)
            teacher_user.roles.append(teacher_role)
            parent_user.roles.append(parent_role)
            
            # Create sample students
            for student_data in MockDataService.get_mock_students():
                student = Student(**student_data)
                session.add(student)
            
            # Create sample admissions
            for admission_data in MockDataService.get_mock_admissions():
                admission = Admission(**admission_data)
                session.add(admission)
            
            # Create sample subjects
            for subject_data in MockDataService.get_mock_subjects():
                subject = Subject(**subject_data)
                session.add(subject)
            
            # Create sample timetables
            for timetable_data in MockDataService.get_mock_timetables():
                timetable = Timetable(**timetable_data)
                session.add(timetable)
            
            # Create sample timetable slots
            for slot_data in MockDataService.get_mock_timetable_slots():
                slot = TimetableSlot(**slot_data)
                session.add(slot)
            
            # Create sample exams
            for exam_data in MockDataService.get_mock_exams():
                exam = Exam(**exam_data)
                session.add(exam)
            
            # Create sample exam results
            for result_data in MockDataService.get_mock_exam_results():
                result = ExamResult(**result_data)
                session.add(result)
            
            # Create sample fee structures
            for structure_data in MockDataService.get_mock_fee_structures():
                structure = FeeStructure(**structure_data)
                session.add(structure)
            
            # Create sample fee items
            for item_data in MockDataService.get_mock_fee_items():
                item = FeeItem(**item_data)
                session.add(item)
            
            # Create sample fee records
            for record_data in MockDataService.get_mock_fee_records():
                record = FeeRecord(**record_data)
                session.add(record)
            
            # Create sample payments
            for payment_data in MockDataService.get_mock_payments():
                payment = Payment(**payment_data)
                session.add(payment)
            
            # Create sample reports
            for report_data in MockDataService.get_mock_reports():
                report = Report(**report_data)
                session.add(report)
            
            await session.commit()
            logger.info("Sample data created successfully")
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
