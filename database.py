#database.py
import sqlite3 as sql

#Asking the user for a database name (check for format?)
database_name = input("Enter the name of the database to create: (postfix with .db) ")

#Initialising a SQLite database using the sqlite3 module and the cursor object
conn = sql.connect("{}".format(database_name))
curr = conn.cursor()

#Formatting SQL commands to create three tables within the project database
create_protein_list = """ CREATE TABLE protein_list (
    accession VARCHAR(20),
    name VARCHAR(10),
    description VARCHAR(100)
); """

create_ratio_list = """ CREATE TABLE ratio_list (
    accession VARCHAR(20),
    exp_name VARCHAR(20),
    avg DECIMAL(3,2)
); """

create_exp_list = """ CREATE TABLE exp_list (
    exp_name VARCHAR(20),
    ctrl VARCHAR(20),
    mut VARCHAR(20),
    conditions VARCHAR(100)
);"""

"""
peptides INT,
PSMs INT,
ratios_raw DECIMAL(3,2),
ratios_corrected DECIMAL(3,2),
avg DECIMAL(3,2),
N INT,
SD DECIMAL(4,3),
SEM DECIMAL(4,3),
conf VARCHAR(20)
"""

#Attempting to execute the formatted SQL commands and alerting the user about the status
try:
    curr.execute(create_protein_list)
    curr.execute(create_ratio_list)
    curr.execute(create_exp_list)
    print("Tables successfully created")
except:
    print("Tables could not be created")
