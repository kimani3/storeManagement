import sqlite3
import datetime


def get_date_time():
    date = str(datetime.datetime.today())[8:10]
    time = str(datetime.datetime.today())[11:19]
    month = str(datetime.datetime.today())[5:7]
    year = str(datetime.datetime.today())[0:4]
    return time, date, month, year


def create_data_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        create table data (name varchar2, inventory number, time varchar2,dte varchar2);       
        """

    )
    conn.commit()
    cursor.close()
    conn.close()


def insert_data(name: str, inventory: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    time, date, month, year = get_date_time()
    date_f = date + '-' + month + '-' + year
    cursor.execute(
        f"""
         insert into data values('{name.capitalize()}',{inventory},'{time}','{date_f}')     
        """

    )
    conn.commit()
    cursor.close()
    conn.close()


def show_all_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        f"""
         select * from data where name not like '%powder%'
        """

    )
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data


def update_inventory(name: str, new_inventory: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
            update data set inventory={new_inventory} where name='{name.capitalize()}'
        """

    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_product(name: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
             delete from data where name='{name.capitalize()}'  
        """

    )
    conn.commit()
    cursor.close()
    conn.close()


def is_present(name: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
            select * from data where name='{name.capitalize()}'
        """

    )

    if cursor.fetchall():
        conn.commit()
        cursor.close()
        conn.close()
        return True
    conn.commit()
    cursor.close()
    conn.close()
    return False

def clear_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
            delete from data
        """

    )
    conn.commit()
    cursor.close()
    conn.close()


def change_name(name: str, new_name: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
           update data set name='{new_name}' where name='{name.capitalize()}';
         """

    )
    conn.commit()
    cursor.close()
    conn.close()


def bulk_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        f"""
          select * from data where name like '%powder%'
            """

    )
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data