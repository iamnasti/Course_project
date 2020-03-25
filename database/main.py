from peewee import *
import pandas
import sqlite3


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