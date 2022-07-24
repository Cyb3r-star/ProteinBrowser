#upload.py
import xlrd
import sqlite3 as sql

#Prompting the user for input for Excel file, sheet, database, and some experiment data
filename = input("Enter the name of the Excel file to parse: ")
sheetname = input("Enter the name of the sheet to parse: ")
database_name = input("Enter the name of the database to which you want to upload data: ")
exp_name = input("Enter the experiment name: ")
ctrl = input("Enter the control name: ")
mut = input("Enter the mutant name: ")
conditions = input("Enter the experiment conditions: ")

#Opening and loading the Excel sheet data using xlrd
workbook = xlrd.open_workbook(("{}").format(filename))
db = workbook.sheet_by_name(("{}").format(sheetname))

#Declaring the Protein class to store individual data for a single protein (will be stored in the proteins[] list)
class Protein:
    def __init__(self, accession, name, description, peptides, PSMs, ratios_raw, ratios_corrected, avg, N, SD, SEM, conf):
        self.accession = accession
        self.name = name
        self.description = description
        self.peptides = peptides
        self.PSMs = PSMs
        self.ratios_raw = ratios_raw
        self.ratios_corrected = ratios_corrected
        self.avg = avg
        self.N = N
        self.SD = SD
        self.SEM = SEM
        self.conf = conf

proteins = []

#Iterating over the spreadsheet rows, extracting individual cell data, and assigning it to variables in the Protein class
for row_count in range(3, 62):
    accession = db.cell(row_count, 0).value
    name = db.cell(row_count, 1).value
    description = db.cell(row_count, 2).value
    peptides = db.cell(row_count, 3).value
    PSMs = db.cell(row_count, 4).value

    avg = db.cell(row_count, 13).value
    N = db.cell(row_count, 14).value
    SD = db.cell(row_count, 15).value
    SEM = db.cell(row_count, 16).value
    conf = db.cell(row_count, 17).value

#Populating the ratios lists with values from the spreadsheet using loops
    ratios_raw = []
    ratios_corrected = []

    for i in range(5,8):
        ratios_raw.append(db.cell(row_count, i))
    for i in range(9,12):
        ratios_corrected.append(db.cell(row_count, i))

#Instantiating a new protein object with the attributes extracted from spreadsheet row
    new_protein = Protein(accession, name, description, peptides, PSMs, ratios_raw, ratios_corrected, avg, N, SD, SEM, conf)
    proteins.append(new_protein)
    row_count += 1

#Uploading spreadsheet data to a SQLite database
conn = sql.connect("{}.db".format(database_name))
curr = conn.cursor()

for i in proteins:
    add_protein_list = f"""INSERT INTO protein_list VALUES('{i.accession}', '{i.name}', '{i.description}')"""
    add_ratio_list = f"""INSERT INTO ratio_list VALUES('{i.accession}', '{exp_name}', '{i.avg}')"""
    add_exp_list = f"""INSERT INTO exp_list VALUES('{exp_name}', '{ctrl}', '{mut}', '{conditions}')"""

    print(add_protein_list,"\n", add_ratio_list,"\n", add_exp_list,"\n")
    curr.execute(add_protein_list)
    curr.execute(add_ratio_list)
    curr.execute(add_exp_list)

print("Data added successfully")
conn.commit()
