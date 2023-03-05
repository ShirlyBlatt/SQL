import sqlite3


#   DTO
class Hat:
    def __init__(self, hat_id, topping, supplier, quantity):
        self.hat_id = hat_id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, supplier_id, supplier_name):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name.rstrip("\n")


class Order:
    def __init__(self, order_id, location, hat):
        self.order_id = order_id
        self.location = location
        self.hat = hat


#   DAO
class Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("INSERT INTO hats (id, topping, supplier, quantity) VALUES (?, ?, ?, ?)",
                           [hat.hat_id, hat.topping, hat.supplier, hat.quantity])

    def find(self, hat_id):
        c = self._conn.cursor()
        c.execute("SELECT * FROM hats WHERE id=?", [hat_id, ])
        return Hat(*c.fetchone())

    def update_quantity(self, hat_id):
        c = self._conn.cursor()
        c.execute("SELECT quantity FROM hats WHERE id=?", [hat_id, ])
        quantity = c.fetchone()[0]
        if quantity > 1:
            c.execute("UPDATE hats SET quantity=? WHERE id=?", [quantity - 1, hat_id])
        else:
            c.execute("DELETE FROM hats WHERE id=?", [hat_id, ])

    def select_hat(self, topping):
        c = self._conn.cursor()
        c.execute("SELECT * FROM hats WHERE topping=? ORDER BY supplier ASC", [topping, ])
        selected_hat = c.fetchone()
        if selected_hat:
            return Hat(*selected_hat)
        else:
            return None


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("INSERT INTO suppliers (id, name) VALUES (?, ?)",
                           [supplier.supplier_id, supplier.supplier_name])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("SELECT * FROM suppliers WHERE id=?", [supplier_id, ])
        return Supplier(*c.fetchone())


class Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)",
                           [order.order_id, order.location, order.hat])

    def find(self, order_id):
        c = self._conn.cursor()
        c.execute("SELECT * FROM orders WHERE id=?", [order_id, ])
        return Order(*c.fetchone())


#    Repository
class Repository:
    def __init__(self, database_path):
        self._conn = sqlite3.connect(database_path)
        self.hats = Hats(self._conn)
        self.suppliers = Suppliers(self._conn)
        self.orders = Orders(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def crate_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats(
            id INTEGER PRIMARY KEY,
            topping VARCHAR NOT NULL,
            supplier INTEGER REFERENCES suppliers(id),
            quantity INTEGER NOT NULL 
        );
        
        CREATE TABLE suppliers(
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL 
        );
        
        CREATE TABLE orders(
            id INTEGER PRIMARY KEY,
            location VARCHAR NOT NULL,
            hat INTEGER REFERENCES hats(id)
        );
        """)
