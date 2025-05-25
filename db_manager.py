from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, CheckConstraint, TIMESTAMP, BYTEA
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), default='student')
    registration_date = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("role IN ('student','teacher','admin')", name='check_user_role'),
    )

    progress = relationship("UserProgress", back_populates="user")
    sessions = relationship("Session", back_populates="user")


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(20), default='medium')
    task_type = Column(String(20), default='practice')
    creation_date = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("difficulty IN ('easy','medium','hard')", name='check_difficulty'),
        CheckConstraint("task_type IN ('theory','practice','test')", name='check_task_type'),
    )

    content = relationship("TaskContent", back_populates="task")
    progress = relationship("UserProgress", back_populates="task")


class TaskContent(Base):
    __tablename__ = 'task_content'

    content_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=False)
    question_text = Column(Text)
    question_image = Column(BYTEA)
    answer_text = Column(Text)
    answer_image = Column(BYTEA)
    format_type = Column(String(10), default='text')

    __table_args__ = (
        CheckConstraint("format_type IN ('text','image','mixed')", name='check_format_type'),
    )

    task = relationship("Task", back_populates="content")


class UserProgress(Base):
    __tablename__ = 'user_progress'

    progress_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=False)
    is_completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    last_attempt_date = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 100", name='check_score'),
    )

    user = relationship("User", back_populates="progress")
    task = relationship("Task", back_populates="progress")


class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    start_time = Column(TIMESTAMP, default=datetime.utcnow)
    end_time = Column(TIMESTAMP)
    ip_address = Column(String(45))

    user = relationship("User", back_populates="sessions")
