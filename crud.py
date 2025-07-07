# db.py
import mysql.connector
from mysql.connector import Error
import sys

# Funciones backend para la aplicación

class CrudInventario:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect (
                host='localhost',
                user='root',  
                password='root',  
                database='inventario - vivero cafe el arco',
                port = 3307
            )
            print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            sys.exit(1)

    def agregar_producto(self, idproducto, idcategoria, idunidad, nombre, precio, consumible):
        try:
            
        
            cursor = self.connection.cursor()
            
            query = """INSERT INTO `inventario - vivero cafe el arco`.producto 
            (Id_producto, Id_categoria, Id_unidad_medida, Nombre, Unidad_precio, Consumible)   
            VALUES (%s, %s, %s, %s, %s, %s)"""

            cursor.execute(query, (idproducto, idcategoria, idunidad, nombre, precio, consumible))
            self.connection.commit()
            print("📦 Producto agregado correctamente")
            return True

        except Error as e:
            print(f"❌ Error al agregar producto: {e}")
            self.connection.rollback()
            return False
    
    def eliminar_producto(self, idproducto):
        try:
            
            cursor = self.connection.cursor()
            query = """
            DELETE FROM `inventario - vivero cafe el arco`.producto
            WHERE Id_producto = %s
            """
            cursor.execute(query, (idproducto,))
            self.connection.commit()
            print("📦 Producto eliminado correctamente")
        except Error as e:
            print(f"❌ Error al eliminar producto: {e}")
            print(e)
        
    def obtener_datos_producto(self):
        try:
            
            cursor = self.connection.cursor()
            print("🔍 Ejecutando consulta SQL...")
            cursor.execute("select * from `inventario - vivero cafe el arco`.producto p")

            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            print("Resultados: ", resultados)
            print("📦 Datos obtenidos correctamente.")
            return columnas, resultados
    
        except Error as e:
            print("❌ Error al conectar a MySQL")
            print(e)
            return [], []

    def buscar_producto_por_id(self, id_producto):
        try:
            cursor = self.connection.cursor()
            query = """
            select * from `inventario - vivero cafe el arco`.producto p where p.Id_producto = %s  
            """
            cursor.execute(query, (id_producto,))
            resultado = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            print("Resultados: ", resultado)
            return columnas, resultado
        except Error as e:
            print(f"❌ Error al buscar producto por ID: {e}")
            return None

    # Gestión de proveedores
    def agregar_proveedor(self, idprovedor, nombre, telefono, correo, direccion, proveedor_credio):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO `inventario - vivero cafe el arco`.proveedor
            (Id_proveedor, Proveedor_nombre, Proveedor_telefono, Proveedor_correo, Proveedor_direccion, Proveedor_credito_fiscal)  
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (idprovedor, nombre, telefono, correo, direccion, proveedor_credio))
            self.connection.commit()
            print("📦 Proveedor agregado correctamente")
            return True
        except Error as e:
            print(f"❌ Error al agregar proveedor: {e}")
            self.connection.rollback()
            return False

    def eliminar_proveedor(self, idprovedor):
        try:
            cursor = self.connection.cursor()
            query = """
            DELETE FROM `inventario - vivero cafe el arco`.proveedor
            WHERE Id_proveedor = %s
            """
            cursor.execute(query, (idprovedor,))
            self.connection.commit()
            print("📦 Proveedor eliminado correctamente")
        except Error as e:
            print(f"❌ Error al eliminar proveedor: {e}")
            self.connection.rollback()
            return False

    def obtener_datos_proveedor(self):
        try:
            cursor = self.connection.cursor()
            print("🔍 Ejecutando consulta SQL...")
            cursor.execute("select * from `inventario - vivero cafe el arco`.proveedor p")
    
            # Obtener nombres de columnas
            columnas = [desc[0] for desc in cursor.description]
            resultado = cursor.fetchall()
    
            # Determinar el ancho máximo de cada columna
            col_widths = []
            for i in range(len(columnas)):
                ancho_columna = max(len(str(row[i])) for row in resultado) if resultado else 0
                col_widths.append(max(ancho_columna, len(columnas[i])) + 2)
    
            # Imprimir encabezados alineados
            header = ""
            for i, col in enumerate(columnas):
                header += col.ljust(col_widths[i])
            print(header)
    
            # Separador
            print("-" * len(header))
    
            # Imprimir filas
            for row in resultado:
                linea = ""
                for i, col in enumerate(row):
                    linea += str(col).ljust(col_widths[i])
                print(linea)
    
        except Error as e:
            print("❌ Error al conectar a MySQL")
            print(e)     

    # Recetas        
    def agregar_receta(self, idreceta, nombre, descripcion, precio):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO `inventario - vivero cafe el arco`.receta
            (Id_receta, Nombre, Descripcion, Precio_receta)  
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (idreceta, nombre, descripcion, precio))
            self.connection.commit()
            print("📦 Receta agregada correctamente")
            return True
        
        except Error as e:
            print(f"❌ Error al agregar receta: {e}")
            self.connection.rollback()
            return False

    def eliminar_receta(self, idreceta):
        try:
            cursor = self.connection.cursor()
            query = """
            DELETE FROM `inventario - vivero cafe el arco`.receta
            WHERE Id_receta = %s
            """
            cursor.execute(query, (idreceta,))
            self.connection.commit()
            print("📦 Receta eliminada correctamente")
        except Error as e:
            print(f"❌ Error al eliminar receta: {e}")
            self.connection.rollback()
            return False
        
    def obtener_datos_receta(self):
        try:
            cursor = self.connection.cursor()
            print("🔍 Ejecutando consulta SQL...")
            cursor.execute("select * from `inventario - vivero cafe el arco`.receta r")
            
            columnas = [desc[0] for desc in cursor.description]
            resultado = cursor.fetchall()

            col_widths = []
            for i in range(len(columnas)):
                ancho_columna = max(len(str(row[i])) for row in resultado) if resultado else 0
                col_widths.append(max(ancho_columna, len(columnas[i])) + 2)

            header = ""
            for i, col in enumerate(columnas):
                header += col.ljust(col_widths[i])
            print(header)

            print("-" * len(header))

            for row in resultado:
                linea = ""
                for i, col in enumerate(row):
                    linea += str(col).ljust(col_widths[i])
                print(linea)

        except Error as e:
            print("❌ Error al conectar a MySQL")
            print(e)

    def obtener_productos_para_receta(self, id_receta): #Pendiente
        try:
            cursor = self.connection.cursor()
        
            # 1. Verificar si la receta existe y obtener su nombre
            cursor.execute("SELECT Nombre FROM receta WHERE Id_receta = %s", (id_receta,))
            receta = cursor.fetchone()
        
            if not receta:
                print(f"❌ No existe una receta con el ID {id_receta}")
                return None
        
            nombre_receta = receta[0]
            print(f"\n📋 Receta: {nombre_receta} (ID: {id_receta})")
            print("=" * 50)
        
            # 2. Obtener todos los productos con sus cantidades y costos
            query = """
            select
	            p.Nombre as Producto,
	            rp.Cantidad_receta as Cantidad,
	            um.Unidades  as Unidad_medida,
	            rp.Costo_por_ingrediente as Costo_individual,
	            p.Unidad_precio as Precio_unitario
            from `inventario - vivero cafe el arco`.receta_producto  rp
            join `inventario - vivero cafe el arco`.producto p on rp.Id_producto = p.Id_producto
            join `inventario - vivero cafe el arco`.unidad_medida um on rp.Id_unidad_medida = um.Id_unidad_medida
            where 
	            rp.Id_receta = %s
            order by 
	            p.Nombre
            """
            cursor.execute(query, (id_receta,))
            ingredientes = cursor.fetchall()
        
            if not ingredientes:
                print("ℹ️ Esta receta no tiene ingredientes registrados")
                return None
        
            # 3. Mostrar tabla formateada
            print(f"{'Producto':<25} | {'Cantidad':>10} | {'Unidad':<12} | {'Costo ingrediente':>12} | {'Precio Unitario':>15}")
            print("-" * 85)
        
            costo_total = 0
            for ing in ingredientes:
                producto, cantidad, unidad, costo_individual, precio_unitario = ing
                costo_total += costo_individual
                print(f"{producto:<25} | {cantidad:>10.2f} | {unidad:<12} | ${costo_individual:>10.4f} | ${precio_unitario:>14.2f}")
        
            # 4. Mostrar totales
            print("=" * 85)
            print(f"{'COSTO TOTAL DE LA RECETA':<60} ${costo_total:>10.4f}")
            print(f"{'PRECIO DE VENTA SUGERIDO':<60} ${costo_total*0.35:>10.2f}") 
        
            return {
                'nombre_receta': nombre_receta,
                'ingredientes': ingredientes,
                'costo_total': costo_total
            }
        
        except Error as e:
            print("❌ Error al conectar a MySQL")
            print(e)
            return None

    # CRUD para receta_producto
    def agregar_receta_producto(self, id_producto, id_receta, cantidad, id_unidad_medida, costo_por_ingrediente):
        try:
            cursor = self.connection.cursor()

            query = """
            INSERT INTO `inventario - vivero cafe el arco`.receta_producto
            (Id_producto, Id_receta, Cantidad_receta, Id_unidad_medida, Costo_por_ingrediente)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_producto, id_receta, cantidad, id_unidad_medida, costo_por_ingrediente))
            self.connection.commit()
            print("📦 Receta agregada correctamente")
            return True
        except Error as e:
            print(f"❌ Error al agregar receta: {e}")
            self.connection.rollback()
            return False

    def eliminar_columna_receta_producto(self, id_producto, id_receta): 
        try:
            cursor = self.connection.cursor()
            query = """
            delete from `inventario - vivero cafe el arco`.receta_producto
            where Id_producto = %s and Id_receta = %s 
            """
            cursor.execute(query, (id_producto, id_receta))
            self.connection.commit()
            print("📦 Receta eliminada correctamente")
        except Error as e:
            print(f"❌ Error al eliminar receta: {e}")
            self.connection.rollback()
            return False

    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión a MySQL cerrada")        
           

# Producto
"""
if __name__ == "__main__":
    inventario = CrudInventario()


    try:
        # Ejemplo: Agregar un producto
        inventario.agregar_producto(21, 10, 4, "MM", 1.65, "No Consumible")

        # Ejemplo: Eliminar un producto
        inventario.eliminar_producto(22)

        # Ejemplo: Obtener datos
        inventario.obtener_datos_producto()

    finally:
        inventario.cerrar_conexion()
"""
# Proveedor
"""
if __name__ == "__main__":
    inventario = CrudInventario()
    try:
        # Ejemplo: Agregar un proveedor
        inventario.agregar_proveedor(11, "Dolar", "7841-2269", "atencion@dollar.com", "Ex local de 3 puntos, P.º Gral. Escalón Block A, San Salvador", "CF-2025-00126")
        # Ejemplo: Eliminar un proveedor
        inventario.eliminar_proveedor(12)

        # Ejemplo: Obtener datos
        inventario.obtener_datos_proveedor()

    finally:
        inventario.cerrar_conexion()
"""

if __name__ == "__main__":
    inventario = CrudInventario()
    try:
        inventario.obtener_datos_producto()
        
    finally:
        inventario.cerrar_conexion()
