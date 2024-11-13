import os
import sqlite3
import numpy as np
import pandas as pd

class _BaseDB:
    '''
    This class contains the core functionality for working with a SQLite database.
    '''
    def __init__(self, 
                 path: str, 
                 create: bool=False
                 ):
        '''
        Arguments:
            - path:   A string containing the path to the database.
            - create: Whether to create the required files/folders if they do not exist (default=False).
                      Should be set to True if using the application for the first time.
                      Should be set to False in all other cases, primarily to detect a misspelled path.
        '''
        self._connected = False
        #sets default state of connection between initializer and SQL DB as False
        self._path = os.path.normpath(path)
        #sets path to path of given file
        self._existed = self._check_exists(create)
        #will create file with filename from self._path, given the file doesn't already exist
        return
    
    def format_sql(self, 
                   sql: str
                   ) -> str:
        '''
        Remove leading whitespace from each line of a SQL string for display purposes.

        Returns a cleaned-up copy of the string.
        '''
        formatted_sql = ''
        for line in sql.split('\n'):
            formatted_sql += line.lstrip() + '\n'
            #removes leading whitespace (lstrip), creates new line for next string
        return formatted_sql

    def run_query(self, 
                  sql: str, 
                  params:tuple|dict = None
                  ) -> pd.DataFrame:
        '''
        Runs a SELECT (or similar) query and returns the results as a Pandas DataFrame.

        Arguments:
            - sql:        A string containing a SQL action query
            - params:     A tuple or dictionary containing query parameters
        '''
        self._connect()
        #connect to sql db
        try:
            results = pd.read_sql(sql, self._conn, params=params)
            #attempts to run query, returns as a dataframe
        except Exception as e:
            raise type(e)(f'sql: {sql}\nparams: {params}') from e 
            #will display error message when 'try' doesn't work
        finally:
            self._close()
            #close connection to sql db
        return results
    
    def run_action(self, 
                   sql:str,
                   params: tuple|dict = None,
                   commit = False,
                   keep_open = True
                   ) -> int:
        '''
        Runs an action query. Returns the lastrowid property of the cursor (see PEP 429 for more info).

        Arguments:
            - sql:        A string containing a SQL action query
            - params:     A tuple or dictionary containing query parameters
            - commit:     Whether to commit the changes immediately (default=False)
            - keep_open:  If True, database connection will not be closed after the query is run.
                          Use this when you want to make multiple calls to this function before committing (default=False)
        '''
        
        if not self._connected: 
            self._connect()
        try:
            if params is None:
                self._curs.execute(sql)
            else:
                self._curs.execute(sql, params)
            if commit:
                self._commit()
        except Exception as e:
            self._rollback()
            self._close()
                
            raise type(e)(f'Action query failed to execute. Query details below:\n\nsql:\n{self.format_sql(sql)}\n\nparams:\n{params}') from e  
        
        if not keep_open:
            self._close()
        return self._curs.lastrowid
    
    def _commit(self) -> None:
        '''
        Convenience method for committing changes.
        '''
        self._conn.commit()
        return
    
    def _rollback(self) -> None:
        '''
        Convenience method for rolling back changes.
        '''
        self._conn.rollback()
        return
    
    def _connect(self, 
                 foreign_keys: bool = True
                 )->None:
        '''
        Establishes connection to the database and stores the connection and cursor objects.

        Arguments:
            - foreign_keys: Boolean indicating whether or not to turn on foreign key constraints (default=True).
        '''
        self._conn = sqlite3.connect(self._path)
        self._curs = self._conn.cursor()
        if foreign_keys:
            self._curs.execute("PRAGMA foreign_keys=ON;")
        self._connected = True
        return
    
    def _close(self)->None:
        '''
        This method should be used rather than a direct call to the connection's close() method.
        In addition to closing the connection, also sets the internal _connected property to False.
        '''
        self._conn.close()
        self._connected = False
        return

    def _check_exists(self, 
                      create: bool
                      ) -> bool:
        '''
        Ensure database and all parts of the filepath exist.  
        Returns a boolean indicating if everything already existed or not.

        Arguments:
            - create: Boolean indicating whether the database and required directories should be created if they did not exist.
                      If False, will raise a FileNotFoundError instead of creating the missing files/folders.
        '''
        existed = True
        path_parts = self._path.split(os.sep)
        n = len(path_parts)
        for i in range(n):
            part = os.sep.join(path_parts[:i+1])
            if not os.path.exists(part):
                if not create:
                    raise FileNotFoundError(f'File or folder "{part}" does not exist.')
                existed = False
                if i == n-1:
                    self._connect()
                    self._close()
                else:
                    os.mkdir(part)
        return existed