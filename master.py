#!/usr/bin/python3
import sys

from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt, QTime
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QGridLayout, QGroupBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QTreeView, QVBoxLayout, QPushButton, QWidget, QLabel, QAbstractItemView, QTableView


class MyWin(QWidget):
    def __init__(self, mydb):
        super(MyWin, self).__init__()
        main_lt = QVBoxLayout()
        self.view = QTableView()
        main_lt.addWidget(self.view)
        self.view.setWindowTitle("Table Model (View 1)")
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.mydb = mydb

        button = QPushButton("Join")
        button.clicked.connect(self.merge)
        main_lt.addWidget(button)

        button = QPushButton("Exit")
        button.clicked.connect(lambda: exit())
        main_lt.addWidget(button)

        self.setLayout(main_lt)
        self.setWindowTitle('QT1')

    def set_model(self):
        self.view.setModel(self.mydb.get_model())

    def merge(self):
        ind_list = self.view.selectedIndexes()
        out = list(self.view.model().data(i) for i in ind_list)
        self.mydb.merge(out)


class MyDB:
    def __init__(self):
        pass

    def merge(self, out):
        query = QSqlQuery(db=self.db)
        query.exec("update sportsmen set id = 0 where lastname = 'Bill'")

        mb = QMessageBox()
        mb.setText('Merge! %s' % str(out))
        mb.exec_()


    def get_model(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('sports.db')
        self.db.open()
        model = QSqlQueryModel()
        query_str = """ select firstname, count(firstname) from sportsmen group by firstname
        """
        model.setQuery(query_str, db=self.db)
        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "First name")
        model.setHeaderData(2, Qt.Horizontal, "Last name")
        return model

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('sports.db')
        if not self.db.open():
            return False
        query = QSqlQuery(db=self.db)

        query.exec_("create table sportsmen(id int primary key, "
                    "firstname varchar(20), lastname varchar(20))")
        query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
        query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
        query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
        query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
        query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # createDB()
    base = MyDB()
    window = MyWin(base)

    window.set_model()
    window.show()
    sys.exit(app.exec_())
