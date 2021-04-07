import sqlite3


class SqliteHelper:

    def __init__(self, name=None):
        self.conn = None
        self.cur = None

        if name:
            self.open(name)
            self.create_table()

    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)  # ПОЗВОЛЯЕТ закрыть и сохранить текущие данные даже при ошибке
            self.cur = self.conn.cursor()  # Позволяет делать SQL запросы
            print(sqlite3.version)
        except sqlite3.Error as e:
            print("Failed connecting to database...")

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Book (
                IdBook INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                NameB     TEXT NOT NULL,
                Author    TEXT,
                Genre   TEXT,
                YearOfPub INTEGER,
                IdPublisher  INTEGER,
                FOREIGN KEY (IdPublisher) REFERENCES Publishers(IdPublisher)
                 );
            """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Reader (
                    IdReader INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    Lastname TEXT NOT NULL,
                    Firstname TEXT NOT NULL,
                    Fastername TEXT,
                    Address TEXT,
                    Tel TEXT
                    );
                """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Publishers (
                    IdPublisher INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    NameP TEXT,
                    Country TEXT,
                    City TEXT,
                    Founded TEXT,
                    Tel TEXT,
                    Email TEXT,
                    Comment TEXT);
                """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Delivery(
                    IdDelivery INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    IdBook INTEGER,
                    IdReader INTEGER,
                    dataDelivery TEXT,
                    dataReturn TEXT,
                    FOREIGN KEY (IdBook) REFERENCES Book(IdBook),
                    FOREIGN KEY (IdReader) REFERENCES Reader (IdReader)
                    );
                """)
        self.conn.commit()

    def edit(self, query, updates):  # UPDATE
        c = self.cur
        c.execute(query, updates)
        self.conn.commit()

    def delete(self, query):  # DELETE
        c = self.cur
        c.execute(query)
        self.conn.commit()

    def insert(self, query, insertes):  # INSERT
        c = self.cur
        c.execute(query, insertes)
        self.conn.commit()

    def select(self, query):  # SELECT
        c = self.cur
        c.execute(query)
        return c.fetchall()

