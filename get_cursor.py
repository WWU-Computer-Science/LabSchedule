from sys import platform, version_info
import getpass


def get_cursor(username="", password=""):
    """Prompt for username and password if they are not present, and return a
    cursor to the database connection."""

    # Get the username to use for the connection.
    if not username:

        if version_info[0] >= 3:
            get_input = input
        else:
            get_input = raw_input

        username = get_input("Enter Database Username: ")

    # Get the password to use for the connection.
    if not password:
        password = getpass.getpass("Enter Password: ")

    host = "datadb.admsec.wwu.edu"

    # Use pyodbc for Windows, otherwise use cx_Oracle.
    if platform.startswith('win32'):
        import pyodbc
        cnxnstr = ("DRIVER={{Microsoft ODBC for Oracle}};"
                   "SERVER={};UID={};PWD={}".format(host, username, password))
        cnxn = pyodbc.connect(cnxnstr)
    else:
        import cx_Oracle
        port = 1521
        db = "DATAW"
        dsn = cx_Oracle.makedsn(host, port, db)
        cnxn = cx_Oracle.connect(username, password, dsn)

    # Clear out the password.
    password = ""

    return cnxn.cursor()
