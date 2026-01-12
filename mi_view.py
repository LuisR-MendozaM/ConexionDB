# import flet as ft
# import random
# import time
# from datetime import datetime

# class UI:
#     def __init__(self, page: ft.Page):
#         self.page = page
#         self.pressure_values = []  # Lista para almacenar referencias a los textos
#         self.setup_ui()
#         self.update_data()
        
#     def setup_ui(self):
#         # Título principal
#         self.title = ft.Text(
#             "Sistema de Monitoreo de Presiones",
#             size=28,
#             weight=ft.FontWeight.BOLD,
#             color=ft.Colors.BLUE_900,
#         )
        
#         # Contenedor para los 4 cuadros de presión
#         self.pressure_grid = ft.Row(
#             spacing=30,
#             alignment=ft.MainAxisAlignment.CENTER,
#             controls=[]
#         )
        
#         # Hora actual
#         self.time_display = ft.Text(
#             size=18,
#             color=ft.Colors.GREY_700,
#         )
        
#         # Layout principal
#         main_container = ft.Container(
#             content=ft.Column(
#                 controls=[
#                     ft.Container(height=20),
#                     self.title,
#                     ft.Container(height=30),
#                     self.pressure_grid,
#                     ft.Container(height=40),
#                     self.time_display,
#                 ],
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             ),
#             padding=20,
#             alignment=ft.alignment.center,
#         )
        
#         self.page.add(main_container)
#         self.create_pressure_boxes()
        
#     def create_pressure_boxes(self):
#         # Colores para cada cuadro
#         colors = [
#             ft.Colors.BLUE_600,
#             ft.Colors.GREEN_600,
#             ft.Colors.ORANGE_600,
#             ft.Colors.RED_600
#         ]
        
#         titles = ["Presión 1", "Presión 2", "Presión 3", "Presión 4"]
        
#         for i in range(4):
#             # Crear el texto para el valor de presión
#             value_text = ft.Text(
#                 "0",
#                 size=36,
#                 weight=ft.FontWeight.BOLD,
#                 color=ft.Colors.WHITE,
#             )
            
#             # Guardar referencia al texto
#             self.pressure_values.append(value_text)
            
#             pressure_box = ft.Container(
#                 content=ft.Column(
#                     controls=[
#                         # Título del cuadro
#                         ft.Text(
#                             titles[i],
#                             size=20,
#                             weight=ft.FontWeight.BOLD,
#                             color=ft.Colors.WHITE,
#                         ),
#                         ft.Container(height=10),
#                         # Valor de presión (referencia guardada)
#                         value_text,
#                         ft.Container(height=5),
#                         # Unidad
#                         ft.Text(
#                             "PSI",
#                             size=16,
#                             color=ft.Colors.WHITE70,
#                         ),
#                     ],
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     alignment=ft.MainAxisAlignment.CENTER,
#                 ),
#                 width=200,
#                 height=150,
#                 bgcolor=colors[i],
#                 border_radius=15,
#                 padding=15,
#                 alignment=ft.alignment.center,
#                 shadow=ft.BoxShadow(
#                     spread_radius=1,
#                     blur_radius=15,
#                     color=ft.Colors.BLACK38,
#                 ),
#                 animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
#             )
            
#             self.pressure_grid.controls.append(pressure_box)
        
#     def update_data(self):
#         def update():
#             while True:
#                 # Generar valores random
#                 pressures = [
#                     random.randint(10, 20),   # Presión 1
#                     random.randint(20, 30),   # Presión 2
#                     random.randint(30, 40),   # Presión 3
#                     random.randint(40, 50),   # Presión 4
#                 ]
                
#                 # Actualizar valores usando las referencias almacenadas
#                 for i in range(4):
#                     self.pressure_values[i].value = str(pressures[i])
                
#                 # Actualizar hora
#                 self.time_display.value = f"Hora: {datetime.now().strftime('%H:%M:%S')}"
                
#                 # Actualizar la página
#                 self.page.update()
#                 time.sleep(2)
        
#         # Ejecutar actualización en un hilo separado
#         import threading
#         thread = threading.Thread(target=update, daemon=True)
#         thread.start()

# def main(page: ft.Page):
#     page.title = "Sistema de Monitoreo de Presiones"
#     page.window.width = 1000
#     page.window.height = 600
#     page.window.resizable = True
#     page.window.min_width = 800
#     page.window.min_height = 500
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.bgcolor = ft.Colors.GREY_100
#     page.padding = 20
    
#     # Crear y mostrar la interfaz
#     ui = UI(page)

# if __name__ == "__main__":
#     ft.app(target=main)


import flet as ft
import pyodbc
import time
from datetime import datetime
import threading

class UI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.pressure_values = []  # Lista para almacenar referencias a los textos
        self.setup_ui()
        self.update_data()
        
    def setup_ui(self):
        # Título principal
        self.title = ft.Text(
            "Sistema de Monitoreo de Presiones",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
        )
        
        # Estado de conexión
        self.connection_status = ft.Text(
            "Conectando...",
            size=16,
            color=ft.Colors.ORANGE,
        )
        
        # IP del servidor
        self.server_info = ft.Text(
            "Servidor: 192.168.1.87",
            size=14,
            color=ft.Colors.GREY_600,
        )
        
        # Contenedor para los 4 cuadros de presión
        self.pressure_grid = ft.Row(
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[]
        )
        
        # Hora actual
        self.time_display = ft.Text(
            size=18,
            color=ft.Colors.GREY_700,
        )
        
        # Última actualización
        self.last_update = ft.Text(
            "Última actualización BD: --:--:--",
            size=14,
            color=ft.Colors.GREY_600,
        )
        
        # Información adicional
        self.info_text = ft.Text(
            "Actualizando cada 2 segundos...",
            size=12,
            color=ft.Colors.GREY_500,
        )
        
        # Layout principal
        main_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=20),
                    self.title,
                    ft.Container(height=5),
                    self.server_info,
                    ft.Container(height=10),
                    self.connection_status,
                    ft.Container(height=30),
                    self.pressure_grid,
                    ft.Container(height=40),
                    self.time_display,
                    self.last_update,
                    ft.Container(height=10),
                    self.info_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )
        
        self.page.add(main_container)
        self.create_pressure_boxes()
        
    def create_pressure_boxes(self):
        # Colores para cada cuadro
        colors = [
            ft.Colors.BLUE_600,
            ft.Colors.GREEN_600,
            ft.Colors.ORANGE_600,
            ft.Colors.RED_600
        ]
        
        titles = ["Presión 24", "Presión 30", "Presión 35", "Presión 36"]
        
        for i in range(4):
            # Crear el texto para el valor de presión
            value_text = ft.Text(
                "--",
                size=36,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            )
            
            # Guardar referencia al texto
            self.pressure_values.append(value_text)
            
            pressure_box = ft.Container(
                content=ft.Column(
                    controls=[
                        # Título del cuadro
                        ft.Text(
                            titles[i],
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Container(height=10),
                        # Valor de presión (referencia guardada)
                        value_text,
                        ft.Container(height=5),
                        # Unidad
                        ft.Text(
                            "PSI",
                            size=16,
                            color=ft.Colors.WHITE70,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=200,
                height=150,
                bgcolor=colors[i],
                border_radius=15,
                padding=15,
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.BLACK38,
                ),
            )
            
            self.pressure_grid.controls.append(pressure_box)
    
    def connect_to_database(self):
        """Establece conexión con SQL Server remoto"""
        try:
            server_ip = "192.168.1.87"  # IP correcta
            
            connection_string = (
                'DRIVER={SQL Server};'
                f'SERVER={server_ip};'
                'DATABASE=Prueba;'
                'UID=sa;'
                'PWD=Mendoza17'
            )
            
            conn = pyodbc.connect(connection_string)
            self.connection_status.value = "✅ Conectado a SQL Server"
            self.connection_status.color = ft.Colors.GREEN
            print(f"✅ Conexión exitosa a {server_ip}")
            return conn
            
        except Exception as e:
            self.connection_status.value = f"❌ Error de conexión: {str(e)[:50]}..."
            self.connection_status.color = ft.Colors.RED
            print(f"❌ Error de conexión: {e}")
            return None
    
    def get_pressure_data(self, cursor):
        """Obtiene los datos de presión desde la base de datos"""
        try:
            # Obtener la última fila actualizada CON HORA
            cursor.execute("""
                SELECT TOP 1 
                    presion_24, 
                    presion_30, 
                    presion_35, 
                    presion_36, 
                    CONVERT(varchar, fecha, 108) as hora,  -- Solo la hora
                    CONVERT(varchar, fecha, 120) as fecha_completa  -- Fecha completa
                FROM Presiones 
                ORDER BY fecha DESC
            """)
            
            row = cursor.fetchone()
            
            if row:
                pressures = [row.presion_24, row.presion_30, row.presion_35, row.presion_36]
                hora = row.hora  # Solo la hora (HH:MM:SS)
                fecha_completa = row.fecha_completa  # Fecha completa (YYYY-MM-DD HH:MM:SS)
                return pressures, hora, fecha_completa
            else:
                return [0, 0, 0, 0], None, None
                
        except Exception as e:
            print(f"❌ Error al leer datos: {e}")
            return None, None, None
    
    def get_pressure_data_simple(self, cursor):
        """Versión simple sin formato de fecha"""
        try:
            cursor.execute("""
                SELECT TOP 1 presion_24, presion_30, presion_35, presion_36, fecha
                FROM Presiones 
                ORDER BY fecha DESC
            """)
            
            row = cursor.fetchone()
            
            if row:
                pressures = [row.presion_24, row.presion_30, row.presion_35, row.presion_36]
                fecha = row.fecha
                
                # Si fecha es string, extraer solo la fecha (sin hora)
                if isinstance(fecha, str):
                    # Formato esperado: "2025-12-01" o "2025-12-01 00:00:00.000"
                    if ' ' in fecha:
                        # Tiene fecha y hora
                        fecha_parts = fecha.split(' ')
                        if len(fecha_parts) > 1:
                            fecha_str = fecha_parts[0]  # Solo la fecha
                        else:
                            fecha_str = fecha
                    else:
                        fecha_str = fecha
                else:
                    fecha_str = str(fecha)
                    
                return pressures, fecha_str
            else:
                return [0, 0, 0, 0], "Sin fecha"
                
        except Exception as e:
            print(f"❌ Error al leer datos: {e}")
            return None, None
        
    def update_data(self):
        def update():
            # Intentar conectar a la base de datos
            conn = None
            cursor = None
            
            while conn is None:
                conn = self.connect_to_database()
                if conn is None:
                    print("⚠️  Reintentando conexión en 5 segundos...")
                    time.sleep(5)
                else:
                    cursor = conn.cursor()
            
            # Bucle principal de actualización
            while True:
                try:
                    # Obtener datos de la base de datos (versión simple)
                    pressures, fecha_str = self.get_pressure_data_simple(cursor)
                    
                    if pressures is not None:
                        # Actualizar valores en la interfaz
                        for i in range(4):
                            self.pressure_values[i].value = str(pressures[i])
                        
                        # Actualizar hora actual
                        current_time = datetime.now().strftime('%H:%M:%S')
                        self.time_display.value = f"Hora actual: {current_time}"
                        
                        # Mostrar la fecha de la última actualización
                        if fecha_str:
                            self.last_update.value = f"Última medición: {fecha_str}"
                        else:
                            self.last_update.value = "Última medición: Sin fecha"
                        
                        # Actualizar estado de conexión
                        self.connection_status.value = f"✅ Conectado a SQL Server"
                        self.connection_status.color = ft.Colors.GREEN
                        
                    # Actualizar la página
                    self.page.update()
                    
                except Exception as e:
                    print(f"❌ Error en actualización: {e}")
                    error_msg = str(e)
                    self.connection_status.value = f"❌ Error: {error_msg[:30]}..."
                    self.connection_status.color = ft.Colors.RED
                    
                    # Mostrar detalles del error en consola
                    import traceback
                    traceback.print_exc()
                    
                    self.page.update()
                    
                    # Intentar reconectar
                    try:
                        if conn:
                            conn.close()
                    except:
                        pass
                    
                    conn = None
                    while conn is None:
                        print("🔄 Intentando reconexión...")
                        time.sleep(3)
                        conn = self.connect_to_database()
                        if conn:
                            cursor = conn.cursor()
                
                time.sleep(2)  # Esperar 2 segundos entre actualizaciones
        
        # Ejecutar actualización en un hilo separado
        thread = threading.Thread(target=update, daemon=True)
        thread.start()

def main(page: ft.Page):
    page.title = "Sistema de Monitoreo de Presiones"
    page.window.width = 1000
    page.window.height = 650
    page.window.resizable = True
    page.window.min_width = 800
    page.window.min_height = 500
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 20
    
    # Instalar pyodbc si no está instalado
    try:
        import pyodbc
    except ImportError:
        page.add(ft.Text("⚠️ Instalando pyodbc... Esto puede tomar un momento"))
        page.update()
        import subprocess
        subprocess.check_call(["pip", "install", "pyodbc"])
        import pyodbc
    
    # Crear y mostrar la interfaz
    ui = UI(page)

if __name__ == "__main__":
    ft.app(target=main)