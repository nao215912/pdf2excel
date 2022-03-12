from pydantic import BaseModel


class ExcelFilesBase(BaseModel):
    path: str
    name: str


class ExcelFileCreate(ExcelFilesBase):
    pass


class ExcelFile(ExcelFilesBase):
    id: int

    class Config:
        orm_mode = True
