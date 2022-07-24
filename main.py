#main.py
import os

print("""  _                        _
 |_) ._ _ _|_  _  o ._    |_) ._ _        _  _  ._
 |   | (_) |_ (/_ | | |   |_) | (_) \/\/ _> (/_ |
                                                     """)
while True:
    choice = int(input("Type '1' to set up a project database, '2' to upload experiment data to the database, '3' to search for protein data, '4' to view existing databases, '5' to delete a database, or '6' to exit the program. "))

    if choice == 1:
        os.system("python3 database.py")
    elif choice == 2:
        os.system("python3 upload.py")
    elif choice == 3:
        os.system("python3 search.py")
    elif choice == 4:
        os.system("ls *.db")
    elif choice == 5:
        dbname = input("Enter the database to delete: ")
        length = len(dbname)
        ext = dbname[-3:-1] + dbname[-1]

        if ext == ".db":
            os.system("rm -f {}".format(dbname))
        else:
            print("Only .db files can be deleted")
    elif choice == 6:
        break
    else:
        print("Invalid input")
