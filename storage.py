# dictionary example:
#
# recs = {'general': <general>, examples: <list of link to examples>}

from PyQt5 import QtSql


def merge(*recs):
        pass
    # find biggest recs
    # choose general form from biggest recs
    # mix recs.


def separate(*recs):
    pass
    #remove elements from recs


def remember_action():
    pass
    #remember action for redo/undo


def redo():
    pass


def undo():
    pass


def save_base():
    pass


def read_base():
    pass


def read_text_file():
    pass

def createDB():  #TODO: replace
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('sports.db')

    if not db.open():
      return False

    query = QtSql.QSqlQuery()

    query.exec_("create table sportsmen(id int primary key, "
      "firstname varchar(20), lastname varchar(20))")

    query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
    query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
    query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
    query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
    query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
    return True

