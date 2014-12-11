import pyodbc
import getpass


def GetDATAWCursor(username="", password=""):
    """Prompt for username and password if they are not present, and return a
    cursor to the database connection."""
    if not username:
        username = raw_input("Enter Database Username: ")
    if not password:
        password = getpass.getpass("Enter Password: ")
    cnxstr = 'DRIVER={Microsoft ODBC for Oracle};'
    cnxstr += 'SERVER=dataw.admsec.wwu.edu;UID='+username+';PWD='+password
    cnxn = pyodbc.connect(cnxstr)
    password = ""
    return cnxn.cursor()
