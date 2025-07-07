import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys

class InventarioVivero:
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

    # Función para registrar entrada de insumos (compra)
    def registrar_entrada(self, id_producto, cantidad, motivo, id_factura=None):
        try:
            cursor = self.connection.cursor()
            
            # Ayuda a registrar el movimiento
            query = """
            INSERT INTO movimientos (Id_producto, Existencias, Fecha_movimiento, 
                    Tipo_movimiento, Cantidad_movimiento, Motivo_movimiento)
            VALUES (%s, 0, %s, 'Entrada', %s, %s)
            """
            fecha_actual = datetime.now().date()
            cursor.execute(query, (id_producto, fecha_actual, cantidad, motivo))
            
            # Si hay factura asociada, registrar en detalles_facturas
            if id_factura:
                # Obtener precio unitario del producto
                cursor.execute("SELECT Unidad_precio FROM producto WHERE Id_producto = %s", (id_producto,))
                precio_unitario = cursor.fetchone()[0]
                total = precio_unitario * cantidad
                
                # Obtener proveedor (asumimos que el último proveedor es el que hizo esta compra)
                cursor.execute("""
                SELECT id_proveedor FROM detalles_facturas 
                WHERE id_producto = %s ORDER BY id_factura DESC LIMIT 1
                """, (id_producto,))
                proveedor = cursor.fetchone()
                id_proveedor = proveedor[0] if proveedor else 1  # Default a 1 si no hay proveedor
                
                # Obtener unidad de medida del producto
                cursor.execute("SELECT Id_unidad_medida FROM producto WHERE Id_producto = %s", (id_producto,))
                id_unidad = cursor.fetchone()[0]
                
                # Registrar en detalles_facturas
                query = """
                INSERT INTO detalles_facturas (id_factura, id_producto, id_proveedor, 
                        cantidad_producto, id_unidad_medida, total_por_producto)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (id_factura, id_producto, id_proveedor, cantidad, id_unidad, total))
            
            self.connection.commit()
            print(f"Entrada de {cantidad} unidades registrada para el producto ID {id_producto}")
            return True
        except Error as e:
            print(f"Error al registrar entrada: {e}")
            self.connection.rollback()
            return False

    # Función para registrar salida de insumos
    def registrar_salida(self, id_producto, cantidad, motivo):
        try:
            cursor = self.connection.cursor()
            
            # Verificar si hay suficiente stock
            cursor.execute("""
            SELECT Existencias FROM movimientos 
            WHERE Id_producto = %s 
            ORDER BY Id_movimiento DESC LIMIT 1
            """, (id_producto,))
            resultado = cursor.fetchone()
            
            if not resultado or resultado[0] < cantidad:
                print("Error: No hay suficiente stock para realizar esta salida")
                return False
                
            # Registrar el movimiento
            query = """
            INSERT INTO movimientos (Id_producto, Existencias, Fecha_movimiento, 
                    Tipo_movimiento, Cantidad_movimiento, Motivo_movimiento)
            VALUES (%s, 0, %s, 'Salida', %s, %s)
            """
            fecha_actual = datetime.now().date()
            cursor.execute(query, (id_producto, fecha_actual, cantidad, motivo))
            
            self.connection.commit()
            print(f"Salida de {cantidad} unidades registrada para el producto ID {id_producto}")
            return True
        except Error as e:
            print(f"Error al registrar salida: {e}")
            self.connection.rollback()
            return False

    # Función para ver historial de movimientos
    def ver_historial_movimientos(self, id_producto=None, fecha_inicio=None, fecha_fin=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT m.Id_movimiento, p.Nombre as Producto, m.Tipo_movimiento, 
                   m.Cantidad_movimiento, m.Existencias, m.Fecha_movimiento, 
                   m.Motivo_movimiento
            FROM movimientos m
            JOIN producto p ON m.Id_producto = p.Id_producto
            """
            params = []
            
            where_clauses = []
            if id_producto:
                where_clauses.append("m.Id_producto = %s")
                params.append(id_producto)
            if fecha_inicio:
                where_clauses.append("m.Fecha_movimiento >= %s")
                params.append(fecha_inicio)
            if fecha_fin:
                where_clauses.append("m.Fecha_movimiento <= %s")
                params.append(fecha_fin)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            query += " ORDER BY m.Fecha_movimiento DESC, m.Id_movimiento DESC"
            
            cursor.execute(query, tuple(params))
            movimientos = cursor.fetchall()
            
            if not movimientos:
                print("No se encontraron movimientos con los criterios especificados")
            else:
                print("\nHistorial de Movimientos:")
                print("-" * 80)
                for mov in movimientos:
                    print(f"ID: {mov['Id_movimiento']} | Producto: {mov['Producto']} | Tipo: {mov['Tipo_movimiento']}")
                    print(f"Cantidad: {mov['Cantidad_movimiento']} | Stock resultante: {mov['Existencias']}")
                    print(f"Fecha: {mov['Fecha_movimiento']} | Motivo: {mov['Motivo_movimiento']}")
                    print("-" * 80)
            
            return movimientos
        except Error as e:
            print(f"Error al obtener historial de movimientos: {e}")
            return []

    # Función para verificar y mostrar alertas de stock bajo
    def verificar_alertas_stock(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Consulta para productos con stock bajo
            query = """
            SELECT p.Id_producto, p.Nombre, m.Existencias, 
                   c.categorias as Categoria, um.Unidades as Unidad
            FROM producto p
            JOIN (
                SELECT Id_producto, MAX(Id_movimiento) as max_id
                FROM movimientos
                GROUP BY Id_producto
            ) ultimo ON p.Id_producto = ultimo.Id_producto
            JOIN movimientos m ON ultimo.max_id = m.Id_movimiento
            JOIN categorias c ON p.Id_categoria = c.Id_categoria
            JOIN unidad_medida um ON p.Id_unidad_medida = um.Id_unidad_medida
            WHERE m.Existencias < 5  # Umbral de stock mínimo
            AND p.Consumible = 'Consumible'
            ORDER BY m.Existencias ASC
            """
            
            cursor.execute(query)
            productos_bajo_stock = cursor.fetchall()
            
            if not productos_bajo_stock:
                print("No hay productos con stock bajo en este momento")
            else:
                print("\nALERTA: Productos con stock bajo")
                print("=" * 80)
                for producto in productos_bajo_stock:
                    print(f"ID: {producto['Id_producto']} | Producto: {producto['Nombre']}")
                    print(f"Categoría: {producto['Categoria']} | Stock actual: {producto['Existencias']} {producto['Unidad']}")
                    print("-" * 80)
            
            return productos_bajo_stock
        except Error as e:
            print(f"Error al verificar alertas de stock: {e}")
            return []

    # Función para cerrar la conexión
    def cerrar_conexion(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión a MySQL cerrada")

#USALO PACO PENDEJO
if __name__ == "__main__":
    inventario = InventarioVivero()
    
    try:
        # Ejemplo: Registrar una entrada 
        inventario.registrar_entrada(1, 10, "Compra semanal de huevos", 1)
        
        # Ejemplo: Registrar una salida
        inventario.registrar_salida(1, 2, "Uso en preparación de quesadillas")
        
        # Ejemplo: Ver historial de un producto
        inventario.ver_historial_movimientos(id_producto = 1)
        
        # Ejemplo: Verificar alertas de stock
        inventario.verificar_alertas_stock()
        
    finally:
        inventario.cerrar_conexion()