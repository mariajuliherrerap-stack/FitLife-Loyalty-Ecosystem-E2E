import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "fitlife_fidelizacion.db")

class FitLifeDB:
    @staticmethod
    def inicializar():
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # 1. Esquema Estrella (Dimensiones y Hechos)
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_clientes (
                                id_cliente INTEGER PRIMARY KEY, nombre TEXT, genero TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_sedes (
                                id_sede INTEGER PRIMARY KEY, nombre_sede TEXT, ciudad TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS fact_transacciones (
                                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_cliente INTEGER, id_sede INTEGER,
                                monto_compra REAL, bono_entregado REAL, fecha TEXT,
                                FOREIGN KEY(id_cliente) REFERENCES dim_clientes(id_cliente),
                                FOREIGN KEY(id_sede) REFERENCES dim_sedes(id_sede))''')
            
            # 2. Data Seeding (Autogeneración de 5 registros mínimos)
            cursor.execute("SELECT COUNT(*) FROM dim_clientes")
            if cursor.fetchone()[0] == 0:
                print("Inyectando Base de Datos FitLife...")
                cursor.executemany("INSERT INTO dim_clientes VALUES (?, ?, ?)", 
                                   [(1, "Laura", "F"), (2, "Mateo", "M"), (3, "Pedro", "M"), (4, "Ana", "F"), (5, "Camilo", "M")])
                cursor.executemany("INSERT INTO dim_sedes VALUES (?, ?, ?)", 
                                   [(101, "Sede Norte", "Bogotá"), (102, "Sede Centro", "Medellín"), (103, "Sede Sur", "Cali")])
                
                # Transacciones base (Oro > 10M, Plata > 5M, Bronce < 5M)
                transacciones = [
                    (1, 101, 15000000, 1500000, "2026-05-01"), # Oro (10% bono)
                    (2, 102, 11000000, 1100000, "2026-05-05"), # Oro (10% bono)
                    (3, 101, 8000000, 400000, "2026-05-10"),   # Plata (5% bono)
                    (4, 103, 6000000, 300000, "2026-05-15"),   # Plata (5% bono)
                    (5, 102, 2000000, 0, "2026-05-20")         # Bronce (0% bono)
                ]
                cursor.executemany("INSERT INTO fact_transacciones (id_cliente, id_sede, monto_compra, bono_entregado, fecha) VALUES (?, ?, ?, ?, ?)", transacciones)
            conn.commit()