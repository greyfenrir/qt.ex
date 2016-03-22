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
        query_str = """ select name, count(name) as counts from domains group by name order by counts desc
        """
        model.setQuery(query_str, db=self.db)
        model.setHeaderData(0, Qt.Horizontal, "Word")
        model.setHeaderData(1, Qt.Horizontal, "Count")

        return model

    def fill_db(self):
        query = QSqlQuery(db=self.db)
        with open('/home/fenrir/tmp/sha.txt') as book:
            text = book.read()
            text = text[:int(len(text)/20)]
            num_s = 0
            num_w = 0
            while text:
                ends = '.!?'
                endn = [text.find(e) for e in ends if e in text]
                if endn:
                    sentence = text[:min(endn) + 1]
                    text = text[min(endn) + 1:]
                else:
                    sentence = text
                    text = ''
                q4 = 'insert into sentences values (%s, "%s", %s)' % (num_s, sentence, 0)
                query.exec_(q4)
                words = sentence.split(' ')
                for word in words:
                    q5 = 'insert into words values (%s, "%s", %s)' % (num_w, word, num_s)
                    query.exec_(q5)
                    q6 = 'insert into domains values (%s, "%s", %s)' % (num_w, word, num_w)
                    query.exec_(q6)
                    num_w += 1
                num_s += 1

    def create_db(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('sports.db')
        if not self.db.open():
            return False
        query = QSqlQuery(db=self.db)

        q1 = ("CREATE TABLE sentences(" +
                    "id INTEGER, " +
                    "content TEXT, " +
                    "page INTEGER, " +
                    "PRIMARY KEY(id))")
        query.exec_(q1)

        q2 = ("CREATE TABLE words(" +
                    "id INTEGER, " +
                    "word TEXT, " +
                    "sentence_id INTEGER, " +
                    "PRIMARY KEY(id), "
                    "FOREIGN KEY (sentence_id) REFERENCES sentences(id))")
        query.exec_(q2)
        q3 = ("CREATE TABLE domains(" +
                    "id INTEGER, " +
                    "name TEXT, " +
                    "word_id INTEGER, " +
                    "PRIMARY KEY(id), " +
                    "FOREIGN KEY (word_id) REFERENCES words(id))")
        query.exec_(q3)

        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = MyDB()
    #base.create_db()
    #base.fill_db()

    window = MyWin(base)

    window.set_model()
    window.show()
    sys.exit(app.exec_())
