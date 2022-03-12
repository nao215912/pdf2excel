from sqlalchemy.orm import Session
import models
import schemas


def get_excel_file_by_path(db: Session, path: str):
    return db.query(models.ExcelFile).filter(models.ExcelFile.path == path).first()


def get_excel_files(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.ExcelFile).offset(offset).limit(limit).all()


def create_excel_file(db: Session, excel_file: schemas.ExcelFilesCreate):
    db_excel_file = models.ExcelFile(path=excel_file.path, name=excel_file.name)
    db.add(db_excel_file)
    db.commit()
    db.refresh(db_excel_file)
    return db_excel_file
