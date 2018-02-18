#!/usr/local/bin/python2.7

'''Credentials to access databases as the webdb user.

Also creates a function to replace the MySQL.connect method and
reassigns the error class, so that we reduce the number of dependencies
on MySQLdb.

How to use this:

import dbconn2
import MySQLdb

dsn = dbconn2.read_cnf()
dsn = dbconn2.read_cnf('~/.my.cnf')
dsn = dbconn2.read_cnf('foo.cnf')
dsn['db'] = 'wmdb'     # the database we want to connect to
dbconn2.connect(dsn)
curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
curs.execute('select name,birthdate from person')
curs.execute('select name,birthdate from person where name like %s',
             ['%george%'])
curs.fetchall()
curs.fetchone()
'''

import MySQLdb
import re
import os

Error = MySQLdb.Error

def file_contents(filename):
    '''Returns contents of file as a string.'''
    with open(filename,"r") as infile:
        return infile.read()

def read_cnf(cnf_file=None):
    '''Read a file formatted roughly like the ~/.my.cnf file; defaulting
    to that file. Return a dictionary with the necessary information to
    connect to a database. See the connect() function, below.'''
    if cnf_file is None:
        cnf_file = os.path.expanduser('~/.my.cnf')
    else:
        cnf_file = os.path.expanduser(cnf_file)
    cnf = file_contents(cnf_file)
    credentials = {}
    # the key is the name used in the CNF file;
    # the value is the name used in the MySQLdb.connect() function
    mapping = {'host':'host',
               'user':'user',
               'password':'passwd',
               'database':'db'}
    for key in ('host', 'user', 'password', 'database' ):
        cred_key = mapping[key]
        regex = r"\b{k}\s*=\s*[\'\"]?(\w+)[\'\"]?\b".format(k=key)
        # print 'regex',regex
        p = re.compile(regex)
        m = p.search(cnf)
        if m:
            credentials[ cred_key ] = m.group(1)
        elif key == 'host' or key == 'database':
            credentials[ cred_key ] = 'not specified in ' + cnf_file
        else:
            raise Exception('Could not find key {k} in {file}'.format(k=key,file=cnf_file))
    return credentials

# this is essentially a static variable of this package. It caches the DB
# connection, so that it can be returned quickly without setting up a new
# connection, if the user tries to connect again.  

# This code is *not* THREAD SAFE!

the_database_connection = False

def connect_singleton(dsn):
    '''Returns a database connection/handle given the dsn (a dictionary)

This function saves the database connection, so if you invoke this again,
it gives you the same one, rather than making a second connection.  This
is the so-called Singleton pattern.  In a more sophisticated
implementation, the DSN would be checked to see if it has the same data as
for the cached connection.'''
    global the_database_connection
    if not the_database_connection:
        try:
            the_database_connection = MySQLdb.connect( use_unicode=True, charset='utf8', **dsn )
            # so each modification takes effect automatically
            the_database_connection.autocommit(True)
        except MySQLdb.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %
                   (e.args[0], e.args[1]))
            raise
    return the_database_connection

# this is essentially a static variable of this package. It caches the DB
# connection, so that it can be returned quickly without setting up a new
# connection, if the user tries to connect again.  

the_database_connection = False

def connect(dsn):
    '''Creates and returns a new database connection/handle given the dsn (a dictionary)'''
    checkDSN(dsn)
    try:
        conn = MySQLdb.connect( use_unicode=True, charset='utf8', **dsn )
        # so each modification takes effect automatically
        conn.autocommit(True)
    except MySQLdb.Error, e:
        print ("Couldn't connect to database. MySQL error %d: %s" %
               (e.args[0], e.args[1]))
        raise
    return conn

def checkDSN(dsn):
    '''Raises a comprehensible error message if the DSN is missing some necessary info'''
    for key in ('host', 'user', 'passwd', 'db' ):
        if not key in dsn:
            raise KeyError('''DSN lacks necessary '{k}' key'''.format(k=key))
    return True

if __name__ == '__main__':
    print 'starting test code'
    import sys
    if len(sys.argv) < 2:
        print('''Usage: {cmd} cnf_file
test dbconn by giving the name of a cnf_file on the command line'''
              .format(cmd=sys.argv[0]))
        sys.exit(1)
    cnf_file = sys.argv[1]
    DSN = read_cnf(cnf_file)
    DSN['db']='wmdb'
    c = connect(DSN)
    print('successfully connected')
    curs = c.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select user() as user, database() as db')
    row = curs.fetchone()
    print('connected to {db} as {user}'
          .format(db=row['db'],user=row['user']))
    curs.execute('select name,birthdate from person limit 3')
    print('first three people')
    print(curs.fetchall())
    curs.execute('select name,birthdate from person where name like %s',
                 ['%george%'])
    print('names like george')
    print(curs.fetchall())
