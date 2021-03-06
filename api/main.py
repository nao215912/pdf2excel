import os
import shutil

#import convert as convert
from fastapi import (Depends,
					 FastAPI,
					 Query,
					 HTTPException,
					 Path,
					 UploadFile)
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from os.path import exists

import cruds
import models
import schemas
import convert
import infomation_input
import database
import boto3

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

ALLOWED_EXTENSIONS = set(['pdf'])

def get_db():
	db = database.SessionLocal()
	try:
		yield db
	finally:
		db.close()


def convert_excel_files(excel_file_creates: list[models.ExcelFile]):
	excel_files: list[schemas.ExcelFile] = []

	for excel_file_create in excel_file_creates:
		excel_files.append(
			schemas.ExcelFile(id=excel_file_create.id,
							  path=excel_file_create.path,
							  name=excel_file_create.name))

	return excel_files


@app.get("/excels")
async def get_excels_info_from_db(offset: int = Query(..., ge=0),
								  limit: int = Query(..., ge=0),
								  db: Session = Depends(get_db)):
	excel_files = cruds.get_excel_files(db, offset=offset, limit=limit)
	return {
		"total": len(excel_files),
		"next": f"http://127.0.0.1:8000/excels/?offset={offset + len(excel_files)}&limit={limit}",
		"items": convert_excel_files(excel_files)
	}


@app.get("/excels/{path}")
async def get_excels_file(path: str):
	if exists(path):
		return FileResponse(path)
	else:
		raise HTTPException(status_code=400, detail="File not found")

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_fotmat_s3():
	s3_endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL', None)
	s3 = boto3.resource('s3',
						'us-east-1',
						endpoint_url=s3_endpoint_url,
						aws_access_key_id="minio",
						aws_secret_access_key="minio123")
	s3.Bucket('local-pdf2excel').download_file('format.xlsx', './format.xlsx')

@app.post("/pdf")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
	if file and allowed_file(file.filename):
		download_fotmat_s3()
		filename = file.filename
		fileobj = file.file
		filepath =  "./" + filename
		with open(filename,'wb') as buffer:
			shutil.copyfileobj(fileobj, buffer)
		conv = convert.Convert(filepath)
		conv.table_extraction()
		conv.convert_excel()
		info = infomation_input.InformationInput(conv.get_expath())
		info.iter_cols()
		info.add_data_by_column()
		info.create_excel()
		name, path = info.get_path_name()
		excel_file = schemas.ExcelFileCreate(path=path, name=name)
		if cruds.get_excel_file_by_path(db, excel_file.path):
			raise HTTPException(status_code=400, detail="A file with the same name already exists.")
		else:
			return convert_excel_files([cruds.create_excel_file(db=db, excel_file=excel_file)])[0]
