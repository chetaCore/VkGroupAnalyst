import sqlite3
import datetime
from sqlite3 import Error

now = datetime.datetime.now()

def sql_connection():
    try:
        con = sqlite3.connect("VK.db")
        return con

    except Error:
        print("Ошибка")





def create_tables(con):
    cursor = con.cursor()

    cursor.execute(""" 
        create table if not exists groups(
            group_id integer PRIMARY KEY,
            group_name text);
    """)

    cursor.execute(""" 
        create table if not exists members(
            member_id integer,
            group_id integer,
            first_name  text,
            last_name   text,
            bdate integer)
   """)
    con.commit()

def insert_group(con, group_id, group_name):
    cursor = con.cursor()
    groupsList = [group_id, group_name]

    cursor.execute(f"select group_id from groups where group_id = {group_id}")
    if cursor.fetchone() is None:
        cursor.execute("insert into groups values(?,?);", groupsList)
        con.commit()


def insert_members(con,  member_id, group_id, first_name, last_name, bdate):
    cursor = con.cursor()
    groupsList = [member_id, group_id, first_name, last_name, bdate]

    cursor.execute(f"SELECT member_id, group_id FROM members WHERE group_id = {group_id} and member_id = {member_id}")
    if cursor.fetchone() is None:
        cursor.execute("insert into members values(?,?,?,?,?);", groupsList)
        con.commit()

def checkRepeats(con,  member_id, group_id,):
    cursor = con.cursor()
    groupsList = [member_id, group_id]
    cursor.execute(f"SELECT member_id, group_id FROM members WHERE group_id = {group_id} and member_id = {member_id}")
    if cursor.fetchone() is None:
        return True
    else:
        return False

def getAverageAge(con, word):
    cursor = con.cursor()
    cursor.execute(f"SELECT bdate from members where members.group_id = (SELECT group_id FROM groups WHERE group_name LIKE ('%{word}%')) and bdate != 0")

    ages = cursor.fetchall()

    averageAge = 0

    for age in ages:
       averageAge += age[0]
    if len(ages) != 0:
        return now.year - averageAge / len(ages)
    else:
        return 1
