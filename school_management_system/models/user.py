from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from school_management_system.database.base import Base

# Association table for many-to-many relationship between users and roles
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    """
    Role model for user permissions.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_role, back_populates="roles")


class User(Base):
    """
    User model for authentication and authorization.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships
    roles = relationship("Role", secondary=user_role, back_populates="users")
    
    # Different user types can have additional profiles
    admin_profile = relationship("AdminProfile", back_populates="user", uselist=False)
    teacher_profile = relationship("TeacherProfile", back_populates="user", uselist=False)
    parent_profile = relationship("ParentProfile", back_populates="user", uselist=False)


class AdminProfile(Base):
    """
    Profile for administrative users.
    """
    __tablename__ = "admin_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="admin_profile")


class TeacherProfile(Base):
    """
    Profile for teacher users.
    """
    __tablename__ = "teacher_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    employee_id = Column(String, unique=True, index=True)
    department = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    subjects = relationship("Subject", back_populates="teacher")


class ParentProfile(Base):
    """
    Profile for parent users.
    """
    __tablename__ = "parent_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="parent_profile")
    students = relationship("Student", back_populates="parent")
