
# import random
# import time
# import os

# try:
#     while True:
#         presion_24 = random.randint(10, 20)
#         presion_30 = random.randint(20, 30)
#         presion_35 = random.randint(30, 40)
#         presion_36 = random.randint(40, 50)
        
#         # Limpiar pantalla y mostrar siempre en la misma posición
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print("Simulador de datos")
#         print("=" * 30)
#         print(f"\nPresion 1: {presion_24}")
#         print(f"Presion 2: {presion_30}")
#         print(f"Presion 3: {presion_35}")
#         print(f"Presion 4: {presion_36}")
#         print(f"\nHora: {time.strftime('%H:%M:%S')}")
#         print("\nPresiona Ctrl+C para salir")
#         time.sleep(2)
# except KeyboardInterrupt:
#     print("\nSimulación finalizada")


# import pyodbc

# try:
#     #Para SQL Server Authentication
#     connection = pyodbc.connect('DRIVER={SQL Server}; SERVER=DESKTOP-FUKFLII; DATABASE=Prueba; UID=sa; PWD=Mendoza17')
    
#     #Para Windows Authentication
#     # connection = pyodbc.connect('DRIVER={SQL Server};SERVER=USKOKRUM2010;DATABASE=django_api;Trusted_Connection=yes;')
    
#     print("Conexión exitosa.")
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM Presiones")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)
# except Exception as ex:
#     print("Error durante la conexión: {}".format(ex))
# finally:
#     connection.close()  # Se cerró la conexión a la BD.
#     print("La conexión ha finalizado.")


import random
import time
import pyodbc

# Conectar a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-FUKFLII;'
    'DATABASE=Prueba;'
    'UID=sa;'
    'PWD=Mendoza17'
)

cursor = conn.cursor()

def preparar_tabla_para_una_fila():
    """Prepara la tabla para trabajar con una sola fila"""
    try:
        # Verificar si hay datos en la tabla
        cursor.execute("SELECT COUNT(*) FROM Presiones")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Si no hay datos, insertar una fila inicial
            cursor.execute("""
                INSERT INTO Presiones (presion_24, presion_30, presion_35, presion_36)
                VALUES (0, 0, 0, 0)
            """)
            print("✅ Insertada fila inicial")
        elif count > 1:
            # Si hay más de una fila, eliminar todas excepto la primera
            print(f"⚠️  Tabla tiene {count} filas. Conservando solo la primera...")
            cursor.execute("""
                DELETE FROM Presiones 
                WHERE id NOT IN (SELECT MIN(id) FROM Presiones)
            """)
            print("✅ Conservada solo la primera fila")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error al preparar tabla: {e}")

def actualizar_fila_unica():
    """Actualiza siempre la misma fila (la primera)"""
    try:
        # Obtener el ID de la primera fila
        cursor.execute("SELECT TOP 1 id FROM Presiones ORDER BY id")
        row = cursor.fetchone()
        
        if row:
            id_fila = row[0]
            print(f"🔄 Actualizando fila con ID: {id_fila}")
        else:
            print("❌ No hay filas en la tabla")
            return
        
        contador = 0
        
        while True:
            # Generar nuevos datos
            p1 = random.randint(10, 20)
            p2 = random.randint(20, 30)
            p3 = random.randint(30, 40)
            p4 = random.randint(40, 50)
            
            # Actualizar la fila específica
            cursor.execute("""
                UPDATE Presiones 
                SET 
                    presion_24 = ?,
                    presion_30 = ?,
                    presion_35 = ?,
                    presion_36 = ?,
                    fecha = GETDATE()
                WHERE id = ?
            """, p1, p2, p3, p4, id_fila)
            
            conn.commit()
            contador += 1
            
            # Mostrar progreso cada actualización
            print(f"🔄 #{contador}: P1={p1}, P2={p2}, P3={p3}, P4={p4} | {time.strftime('%H:%M:%S')}")
            
            time.sleep(5)  # Esperar 2 segundos
            
    except KeyboardInterrupt:
        print(f"\n✅ Simulación detenida. Total actualizaciones: {contador}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

# Ejecutar
preparar_tabla_para_una_fila()
actualizar_fila_unica()