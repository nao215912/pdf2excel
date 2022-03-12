import tabula
from pathlib import Path
import os


class Convert():
    def __init__(self, path: str):
        self.pdpath = path
        self.filename = Path(self.pdpath).stem

    def tableExtraction(self):
        self.dfs = tabula.read_pdf(self.pdpath, lattice=False, pages='1')

    def convertExcel(self):
        i = 0
        for df in self.dfs:
            df.to_excel("./xlsx/" + self.filename + ".xlsx", index=None)  # Excel
            self.expath = os.getcwd() + "/xlsx/" + self.filename + ".xlsx"
            i += 1

    def getExpath(self):
        return self.expath
