#search.py
import sqlite3 as sql

#Prompting the user for a database name
database_name = input("Enter the database you wish to search: (postfix with a .db)")

#Connecting to a SQLite database using sqlite3
conn = sql.connect("{}".format(database_name))
curr = conn.cursor()

#Prompting the user for a list of Uniprot accession numbers and slicing the string at whitespace delimiters to form a list
txt = input("Enter the protein accession numbers you wish to search for, separated by spaces: ")
proteins = txt.split()

#Iterating over accession numbers in proteins list, forming SQL SELECT queries, and executing them to fetch/print data
for i in proteins:
    retrieve_query = f"""SELECT * FROM ratio_list WHERE accession = '{i}';"""
    curr.execute(retrieve_query)
    data = curr.fetchall()
    print(data)
