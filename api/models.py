from sqlalchemy import Column, Integer, String, DateTime, func

from database import Base


class ExcelFile(Base):
    __tablename__ = "excel_files"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    path = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(45), unique=True, index=True, nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now()
    )
    created_at = Column(
        DateTime,
        server_default=func.now()
    )