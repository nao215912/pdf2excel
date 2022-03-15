from typing_extensions import Self
import tabula
from pathlib import Path
import os

class Convert():
	def __init__(self, path : str):
		self.pdpath = path
		self.filename = Path(self.pdpath).stem
		self.expath = os.getcwd() + '/' + self.filename + '.xlsx'

	def table_extraction(self):
		self.dfs = tabula.read_pdf(self.pdpath, lattice=False, pages = '1')

	def convert_excel(self):
		for df in self.dfs:
			df.to_excel(self.expath,index=None) # Excel
		os.remove(self.pdpath)

	def get_expath(self):
		return self.expath
