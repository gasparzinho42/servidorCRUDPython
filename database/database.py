from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/user_records.db"  # nome da base de dados

# crie banco de dados dentro da pasta do banco de dados se não existir
connection = connect(DB_NAME)

cursor = connection.cursor()


def create_table():
    """funcao para criar tabela dentro do banco de dados"""
    table_script = '''CREATE TABLE IF NOT EXISTS User(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name VARCHAR(255),
                        country VARCHAR(150)
                        );
                    '''
    cursor.executescript(table_script)
    connection.commit()


def update_table(ID, fullname, country):
    """funcao para atualizar dados da tabela"""
    cursor.execute("UPDATE User SET full_name = ?, country = ? WHERE ID = ?", (fullname, country, ID))
    connection.commit()


def delete_record(ID):
    """funcao para deletar um dado da tabela"""
    cursor.execute("DELETE from User WHERE ID=?", (ID))
    connection.commit()


def insert_record(fullname, country):
    """funcao para inserir dados dentro da tabela"""
    cursor.execute("INSERT INTO User(full_name, country) VALUES(?, ?)", (fullname, country))
    connection.commit()


def fetch_records():
    """funcao para buscar todos os registros de usuarios"""
    data = cursor.execute("SELECT * FROM User")
    return data
