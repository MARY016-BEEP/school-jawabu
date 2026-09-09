from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Boolean
)

from sqlalchemy.sql import func

from database import Base


# ==========================================
# USERS
# ==========================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )


# ==========================================
# STUDENTS
# ==========================================

class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)

    registration_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    student_name = Column(String(200))

    parent_name = Column(String(200))

    parent_phone = Column(String(30))

    admission_date = Column(Date)

    gender = Column(String(20))

    date_of_birth = Column(Date)

    nemis_number = Column(String(100))

    class_name = Column(String(50))

    status = Column(
        String(30),
        default="ACTIVE"
    )


# ==========================================
# FEE BILLS
# ==========================================

class Bill(Base):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)

    registration_number = Column(String(50))

    term = Column(String(20))

    academic_year = Column(Integer)

    tuition_fee = Column(Float, default=0)

    transport_fee = Column(Float, default=0)

    library_fee = Column(Float, default=0)

    arrears = Column(Float, default=0)

    total_bill = Column(Float, default=0)


# ==========================================
# PAYMENTS
# ==========================================

class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    registration_number = Column(String(50))

    amount = Column(Float)

    tuition_amount = Column(
        Float,
        default=0
    )

    transport_amount = Column(
        Float,
        default=0
    )

    library_amount = Column(
        Float,
        default=0
    )

    credit_balance = Column(
        Float,
        default=0
    )

    mpesa_receipt = Column(
        String(100),
        unique=True,
        nullable=True
    )

    checkout_request_id = Column(
        String(200),
        unique=True,
        nullable=True
    )

    phone_number = Column(String(30))

    payment_method = Column(
        String(50),
        default="M-Pesa"
    )

    status = Column(
        String(30),
        default="PENDING"
    )

    payment_date = Column(
        DateTime,
        server_default=func.now()
    )


# ==========================================
# EXPENSES
# ==========================================

class Expense(Base):

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)

    expense_date = Column(Date)

    category = Column(String(100))

    description = Column(String(500))

    amount = Column(Float)

    entered_by = Column(String(100))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ==========================================
# ACADEMIC EXAMS
# ==========================================

class Exam(Base):

    __tablename__ = "exams"

    id = Column(Integer, primary_key=True)

    exam_name = Column(String(100))

    term = Column(String(20))

    academic_year = Column(Integer)

    class_name = Column(String(50))


# ==========================================
# STUDENT MARKS
# ==========================================

class StudentMark(Base):

    __tablename__ = "student_marks"

    id = Column(Integer, primary_key=True)

    registration_number = Column(String(50))

    class_name = Column(String(50))

    subject = Column(String(100))

    exam_name = Column(String(100))

    term = Column(String(20))

    academic_year = Column(Integer)

    marks = Column(Float)

    grade = Column(String(20))


# ==========================================
# AUDIT LOGS
# ==========================================

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    username = Column(String(100))

    action = Column(String(50))

    table_name = Column(String(100))

    record_id = Column(String(100))

    old_value = Column(String(1000))

    new_value = Column(String(1000))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ==========================================
# ANNOUNCEMENTS
# ==========================================

class Announcement(Base):

    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True)

    title = Column(String(200))

    message = Column(String(1000))

    created_by = Column(String(100))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )