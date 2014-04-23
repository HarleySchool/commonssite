#
#    Copyright (c) 2012 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
#    $Revision: 1459 $
#    $Author: mwall $
#    $Date: 2013-10-08 20:44:50 -0400 (Tue, 08 Oct 2013) $
#
"""Driver for sqlite"""

import os.path

# Import sqlite3. If it does not support the 'with' statement, then
# import pysqlite2, which might...
import sqlite3
if not hasattr(sqlite3.Connection, "__exit__"):
    del sqlite3
    from pysqlite2 import dbapi2 as sqlite3 #@Reimport @UnresolvedImport

import weedb

def connect(database='', root='', driver='', **argv):
    """Factory function, to keep things compatible with DBAPI. """
    return Connection(database=database, root=root, **argv)

def create(database='', root='', driver='', **argv):
    """Create the database specified by the db_dict. If it already exists,
    an exception of type DatabaseExists will be thrown."""
    file_path = os.path.join(root, database)
    # Check whether the database file exists:
    if os.path.exists(file_path):
        raise weedb.DatabaseExists("Database %s already exists" % (file_path,))
    else:
        # If it doesn't exist, create the parent directories
        fileDirectory = os.path.dirname(file_path)
        if not os.path.exists(fileDirectory):
            os.makedirs(fileDirectory)
        connection = sqlite3.connect(file_path, **argv)
        connection.close()

def drop(database='', root='', driver='', **argv):
    file_path = os.path.join(root, database)
    try:
        os.remove(file_path)
    except OSError:
        raise weedb.NoDatabase("""Attempt to drop non-existent database %s""" % (file_path,))
    
class Connection(weedb.Connection):
    """A wrapper around a sqlite3 connection object."""
    
    def __init__(self, database='', root='', **argv):
        """Initialize an instance of Connection.

        Parameters:
        
            file: Path to the sqlite file (required)

            fileroot: An optional path to be prefixed to parameter 'file'. If not given,
            nothing will be prefixed.
            
        If the operation fails, an exception of type weedb.OperationalError will be raised.
        """
                
        self.file_path = os.path.join(root, database)
        if not os.path.exists(self.file_path):
            raise weedb.OperationalError("Attempt to open a non-existent database %s" % database)
        try:
            connection = sqlite3.connect(self.file_path, **argv)
        except sqlite3.OperationalError:
            # The Pysqlite driver does not include the database file path.
            # Include it in case it might be useful.
            raise weedb.OperationalError("Unable to open database '%s'" % (self.file_path,))
        weedb.Connection.__init__(self, connection, database, 'sqlite')

    def cursor(self):
        """Return a cursor object."""
        return Cursor(self.connection)
    
    def tables(self):
        """Returns a list of tables in the database."""
        
        table_list = list()
        for row in self.connection.execute("""SELECT tbl_name FROM sqlite_master WHERE type='table';"""):
            # Extract the table name. Sqlite returns unicode, so always
            # convert to a regular string:
            table_list.append(str(row[0]))
        return table_list
                
    def columnsOf(self, table):
        """Return a list of columns in the specified table. If the table does not exist,
        None is returned."""
        column_list = list()

        for row in self.connection.execute("""PRAGMA table_info(%s);""" % table):
            # Append this column to the list of columns. 
            column_list.append(str(row[1]))

        # If there are no columns (which means the table did not exist) raise an exceptional
        if not column_list:
            raise weedb.OperationalError("No such table %s" % table)
        return column_list

    def begin(self):
        self.connection.execute("BEGIN TRANSACTION")
        
class Cursor(sqlite3.Cursor):
    """A wrapper around the sqlite cursor object"""
    
    # The sqlite3 cursor object is very full featured. We need only turn
    # the sqlite exceptions into weedb exceptions.
    def __init__(self, *args, **kwargs):
        sqlite3.Cursor.__init__(self, *args, **kwargs)
        
    def execute(self, *args, **kwargs):
        try:
            return sqlite3.Cursor.execute(self, *args, **kwargs)
        except sqlite3.OperationalError, e:
            # Convert to a weedb exception
            raise weedb.OperationalError(e)