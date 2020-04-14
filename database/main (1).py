from peewee import *
import pandas
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (QMainWindow, QWidget,
        QPushButton, QLineEdit, QInputDialog, QDialog, QDialogButtonBox, QComboBox, QCalendarWidget,
        QFormLayout, QLabel, QSpinBox, QTreeView, QVBoxLayout, QHBoxLayout)

from PyQt5 import QtCore

database = SqliteDatabase(
    'db_name'
)

class BaseModel(Model):
    class Meta:
        database = database


class Training(BaseModel):
    Target = CharField()
    Date = IntegerField()


class Competition(BaseModel):
    Name = CharField()
    Date = IntegerField()
    Duration = IntegerField()


class Coach(BaseModel):
    Name = CharField()
    Experience = IntegerField()


class Prize(BaseModel):
    Name = CharField()
    Title = CharField()


class Sportsman(BaseModel):
    Name = CharField()
    Sport_Name = CharField()
    Coach_id = ForeignKeyField(Coach)


class Fan(BaseModel):
    Name = CharField()
    Club = CharField()
    Sportsman_id = ForeignKeyField(Sportsman)


class M_Competition(BaseModel):
    Sportsman_id = ForeignKeyField(Sportsman)
    Competition_id = ForeignKeyField(Competition)


class M_Training(BaseModel):
    Sportsman_id = ForeignKeyField(Sportsman)
    Training_id = ForeignKeyField(Training)
    
class M_Prize(BaseModel):
    Sportsman_id = ForeignKeyField(Sportsman)
    Prize_id = ForeignKeyField(Prize)


csv_path_fan = 'data_fan.csv'
csv_path_coach = 'data_coach.csv'
csv_path_comp = 'data_comp.csv'
csv_path_m_competition = 'data_m_competition.csv'
csv_path_m_training = 'data_m_training.csv'
csv_path_prize = 'data_prize.csv'
csv_path_sportsman = 'data_sportsman.csv'
csv_path_traning = 'data_traning.csv'
csv_path_m_prize = 'data_m_prize.csv'
pandas.read_csv(csv_path_traning).to_sql("Training", database, if_exists='append', index=False)
pandas.read_csv(csv_path_comp).to_sql("Competition", database, if_exists='append', index=False)
pandas.read_csv(csv_path_coach).to_sql("Coach", database, if_exists='append', index=False)
pandas.read_csv(csv_path_prize).to_sql("Prize", database, if_exists='append', index=False)
pandas.read_csv(csv_path_m_prize).to_sql("M_Prize", database, if_exists='append', index=False)
pandas.read_csv(csv_path_sportsman).to_sql("Sportsman", database, if_exists='append', index=False)
pandas.read_csv(csv_path_fan).to_sql("Fan", database, if_exists='append', index=False)
pandas.read_csv(csv_path_m_competition).to_sql("M_Competition", database, if_exists='append', index=False)
pandas.read_csv(csv_path_m_training).to_sql("M_Training", database, if_exists='append', index=False)

MODELS = [Coach,
 Competition,
 Fan,
 M_Competition,
 M_Training,
 Prize,
 Sportsman,
 Training]

database.create_tables(MODELS)
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, QVariant
class MyModel(QAbstractTableModel):
    def __init__(self, items, labels):
        super().__init__()
        self.list = items.copy()
        self.colLabels = labels.copy()

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.colLabels)
    
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QVariant(self.colLabels[section])
        return QVariant()

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return QVariant()
        val = ''
        if role == QtCore.Qt.DisplayRole:
            try:
                tmp = self.list[index.row()]
                val = tuple(tmp)[index.column()]
            except IndexError:
                pass
        return val
    
def query_1(sportX):
    ans = []
    query = (Sportsman.select(Coach.Name).join(Coach).filter(Sportsman.Sport_Name == sportX).group_by('Coach.Name'))
    for x in database.execute(query):
        ans.append(list(x))
    return MyModel(ans, ["Coaches of '"+sportX+"'"])


def query_2(substrX):
    ans = []
    query = (Training
         .select(Training.Target,
                 Training.Date,
                 Sportsman.Name,
                 Competition.Name)
         .join(M_Training)
         .join(Sportsman)
         .join(M_Competition)
         .join(Competition)
         .where(Competition.Name ** f'%{substrX}%')
         .order_by(Training.Date.desc()))
    #print(query)
    for x in database.execute(query):
        print(1)
        ans.append(list(x))
    return MyModel(ans,["Purpose of training","date of training","Names of sportmens"])

def query_3(duratX, titleY):
    ans = []
    query = (Fan
         .select(Fan.Club,
                 Sportsman.Name,
                 Competition.Date,
                 Competition.Name)
         .join(Sportsman)
         .join(M_Competition)
         .join(Competition)
         .switch(Sportsman)
         .join(M_Prize)
         .join(Prize)
         .where(Competition.Duration > duratX,
                Prize.Title == titleY)
         .group_by(Fan.Club)
         )
    for x in database.execute(query):
        ans.append(list(x))
    return MyModel(ans,["Names of clubs","Names of funs"])


class myDialog(QDialog):
    def __init__(self, l, title = "question"):
        super().__init__()
        super().setWindowTitle(title)
        layout = QFormLayout()
        super().setLayout(layout)
        for i, j in l:
            layout.addRow(QLabel(i), j)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


class MainWindow(QMainWindow):
    def __init__(self, dataBaseName):
        super().__init__()
        self._myDatabase = database(dataBaseName)
        self.dataBaseName = dataBaseName
        self._view = QTreeView()

        self._buttonAdd = QPushButton("Add")
        self._buttonAdd.clicked.connect(self.addToDatabase)

        self._buttons = [(QPushButton("Query 1"), self.on1), (QPushButton("Query 2"), self.on2), (QPushButton("Query 3"), self.on3)]
        for i, j in self._buttons:
            i.clicked.connect(j)
        
        self.initUi()

    def initUi(self):
        self.setGeometry(300,300,200,200)
        self.setWindowTitle('Database')

        w = QWidget()

        mainLayout = QVBoxLayout()
        w.setLayout(mainLayout)

        self.setCentralWidget(w)

        mainLayout.addWidget(self._view)

        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(self._buttonAdd)
        for i, _ in self._buttons:
            tmpLayout.addWidget(i)
    def query_4(self,nameFan, clubFan, nameSport):
        sportid = ''
        newid = 0
        query1 = (Sportsman
             .select(Sportsman.id)
             .where(Sportsman.Name == nameSport)
             )
        for i in database.execute(query1):
            sportid = str(list(i)[0])

        query2 = (Fan
             .select(fn.max(Fan.id))
                 )
        for i in database.execute(query2):
            newid = list(i)[0] + 1

        query = (Fan.insert(Name = nameFan, Club = clubFan, Sportsman_id = sportid, id = newid)
                )
        database.execute(query)
        self._myDatabase = database(self.dataBaseName)
        return 0            
    def setModel(self, model):
        if model is None:
            return
        self._view.setModel(model)
    def Sports(self):
        return {i.Sport_Name : None for i in Sportsman.select()}.keys()
    def Sportsmen(self):
        return {i.Name : None for i in Sportsman.select()}.keys()
    def Clubs(self):
        return {i.Club : None for i in Fan.select()}.keys()
    def on1(self):
        str_disc = QLabel("Имена тренеров по виду спорта X")
        l = [("discription", str_disc), ("Sport :", QComboBox())]
        l[1][1].addItems(self.Sports()) 
        d = myDialog(l, "Запрос 1")
        if d.exec() == QDialog.Accepted:
            model = query_1(l[1][1].currentText())
            self.setModel(model)

    def on2(self):
        str_disc = QLabel("Цели и даты тренировок, имена спортсменов, участвующих в соревнованиях,название которых содержит подстроку X (например, «международный»), отсортированные по/nубыванию даты тренировок")
        l = [("Описание", str_disc), ("Подстрока", QLineEdit())]
        d = myDialog(l, "Запрос 2")
        if d.exec() == QDialog.Accepted:
            model = query_2(l[1][1].text())
            self.setModel(model)

    def on3(self):
        str_disc = QLabel("Названия клубов болельщиков, имена спортсменов, даты и названия соревнований продолжительностью больше X, в которых спортсмены получают титул Y")
        l = [("Описание", str_disc), ("Титул Y", QLineEdit())]#, ("Дольше Х", QSpinBox())]
        d = myDialog(l, "Запрос 3")
        num, ok = QInputDialog.getInt(self, "Длительность", "Введите число")
        if not ok:
            return None
        if d.exec() == QDialog.Accepted:
            model = query_3(num, l[1][1].text())
            self.setModel(model)

        if model is None:
            return
        self._view.setModel(model)

    def addToDatabase(self):
        str_disc = QLabel("Имя болельщика")
        name = [("Описание", str_disc), ("Имя болельщика", QLineEdit())]
        l = [("Имя болельщика",QLineEdit()),("Клуб", QComboBox()), ("Спортсмен :", QComboBox())]
        l[1][1].addItems(self.Clubs()) 
        l[2][1].addItems(self.Sportsmen()) 
        d = myDialog(l, "add")
        if d.exec() == QDialog.Accepted:
            self.query_4(l[0][1].text(), l[1][1].currentText(), l[2][1].currentText())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow("test.bd")
    w.show()

    sys.exit(app.exec_())
