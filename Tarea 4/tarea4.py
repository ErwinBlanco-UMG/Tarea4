import csv
import graphviz
import os #importa el modulo os para eliminar archivos
class NodoABB:
    def __init__(self, clave): #Se inicializa el arbol binario de busqueda ABB
        self.clave = clave   #valor que se va ingresando
        self.izquierda = None #apuntador/hijo izquierdo
        self.derecha = None   #apuntador/hijo derecho
        self.altura = 1 #altura de balanceo 

class ABB:  #Inserta un nuevo nodo en el árbol binario de búsqueda.

    def insertar(self, raiz, clave):
        if not raiz: #La raíz del árbol o subárbol
            return NodoABB(clave)
        elif clave < raiz.clave: #El valor agregado.
            raiz.izquierda = self.insertar(raiz.izquierda, clave)
        else:
            raiz.derecha = self.insertar(raiz.derecha, clave)
        return raiz
        # Después de insertar, recalculamos la altura de cada nodo.
    
    def buscar(self, raiz, clave): #Busca un valor en el árbol binario de búsqueda.
        if not raiz or raiz.clave == clave:
            return raiz
        if clave < raiz.clave: #El valor a buscar
            return self.buscar(raiz.izquierda, clave)
        return self.buscar(raiz.derecha, clave)
    
    def eliminar(self, raiz, clave): #Elimina nodo por nodo 
        if not raiz:
            return raiz
        if clave < raiz.clave: #El valor a eliminar
            raiz.izquierda = self.eliminar(raiz.izquierda, clave)
        elif clave > raiz.clave:
            raiz.derecha = self.eliminar(raiz.derecha, clave)
        else:
            if not raiz.izquierda:
                return raiz.derecha
            elif not raiz.derecha:
                return raiz.izquierda
            temp = self.min_valor_nodo(raiz.derecha)
            raiz.clave = temp.clave
            raiz.derecha = self.eliminar(raiz.derecha, temp.clave)
        return raiz
    
    def min_valor_nodo(self, nodo):     #def minimo, encuentra el minimo del arbol izquierdo o nodo con un solo hijo o sin hijos
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual
     # elimina el arbol completo y la imagen creada si es que queda guardada 
    def borrar_arbol(self):
        self.raiz = None #referencia de donde se borrara 
        print("SE ELIMINO EL ARBOLITO/anterior de registros :)")
        try:
            os.remove("avl_tree.png")
            print("Archivo 'avl_tree.png' eliminado.")
        except FileNotFoundError:
            print("El archivo 'avl_tree.png' no existe.")
        except Exception as e:
            print(f"Error al eliminar el archivo 'avl_tree.png': {e}")


class AVL(ABB):
    #la clase obtener altura, demuestra si es viable o no el arbol dependiendo los nodos a donde van
    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0
    
    #se obtiene un balance para saber si hay que rotar o no, el rango estimado es de (-1, 0, 1)
    def obtener_balance(self, nodo):  #se aplica correctamente el balanceo 
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha) if nodo else 0
    
    #si el arbol no esta balanceado por la derecha se hara una rotación simple, restandole uno a la izquierda obteniendo correcta
    #mente una altura del rango dicho anteriormente
    def rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha)) + 1
        y.altura = max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha)) + 1
        return y
    #si el arbol no esta balanceado por la izquierda se hara una rotación simple, restandole uno a la derecha obteniendo correcta
    #mente una altura del rango dicho anteriormente
    def rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha)) + 1
        y.altura = max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha)) + 1
        return y
    #se inserta el nuevo nodo dependiendo el balance
    def insertar(self, raiz, clave):
        if not raiz:
            return NodoABB(clave)
        elif clave < raiz.clave:
            raiz.izquierda = self.insertar(raiz.izquierda, clave)
        else:
            raiz.derecha = self.insertar(raiz.derecha, clave)
        
        raiz.altura = max(self.obtener_altura(raiz.izquierda), self.obtener_altura(raiz.derecha)) + 1
        balance = self.obtener_balance(raiz)
        
        if balance > 1 and clave < raiz.izquierda.clave:
            return self.rotar_derecha(raiz)
        if balance < -1 and clave > raiz.derecha.clave:
            return self.rotar_izquierda(raiz)
        if balance > 1 and clave > raiz.izquierda.clave:
            raiz.izquierda = self.rotar_izquierda(raiz.izquierda)
            return self.rotar_derecha(raiz)
        if balance < -1 and clave < raiz.derecha.clave:
            raiz.derecha = self.rotar_derecha(raiz.derecha)
            return self.rotar_izquierda(raiz)
        
        return raiz
    #visualizar/Graphviz:
    def visualizar(self, raiz):
        dot = graphviz.Digraph() # Se guarda en self.dot
        def recorrer(nodo):
            if nodo:
                dot.node(str(nodo.clave))
                if nodo.izquierda:
                    dot.edge(str(nodo.clave), str(nodo.izquierda.clave))
                    recorrer(nodo.izquierda)
                if nodo.derecha:
                    dot.edge(str(nodo.clave), str(nodo.derecha.clave))
                    recorrer(nodo.derecha)
        recorrer(raiz)
        dot.render('avl_tree', format='png', view=True)
    #cargar archivos desde cvs
    def cargar_archivos(self, nombre_archivo, raiz):
        try:
           print(f"Intentando abrir el archivo: {nombre_archivo}")
           with open(nombre_archivo, newline='', encoding='utf-8') as archivo:  # utf 8 para garantizar compatibilidad de sistemas y programas
              reader = csv.reader(archivo)
              for fila in reader:
                  print(f"Fila leída: {fila}")  # Depuración: mostrar la fila leída
                  try:
                     clave = int(fila[0])
                     print(f"Clave convertida: {clave}")  # Depuración: mostrar la clave convertida
                     raiz = self.insertar(raiz, clave)
                  except ValueError as ve:
                      print(f"Error de valor en fila {fila}: {ve}")
                  except IndexError as ie:
                      print(f"Error de índice en fila {fila}: {ie}")
                  except Exception as e:
                      print(f"Error inesperado en fila {fila}: {e}")
        except FileNotFoundError:
         print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        except Exception as e:
         print(f"Error inesperado al abrir el archivo: {e}")
        return raiz
#clase del menu
def menu():
    avl = AVL()
    raiz = None
    while True:
        print("\n1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde CSV")
        print("5. Visualizar árbol")
        print("6. Eliminar Todo el arbol")
        print("7. Salir")
        try:
            opcion = input("Seleccione una opción: ")
   
            if opcion == '1':
                num = int(input("Número a insertar: "))
                raiz = avl.insertar(raiz, num)
            elif opcion == '2':
                num = int(input("Número a buscar: "))
                print("Encontrado" if avl.buscar(raiz, num) else "No encontrado")
            elif opcion == '3':
                num = int(input("Número a eliminar: "))
                raiz = avl.eliminar(raiz, num)
            elif opcion == '4':
                archivo = input("Nombre del archivo CSV: ")
                raiz = avl.cargar_archivos(archivo, raiz)  # Se usa el método de la clase
            elif opcion == '5':
              if raiz:
                 avl.visualizar(raiz)
              else:
                 print("El árbol está vacío.")
            elif opcion == '6':  # Opción agregada
                avl.borrar_arbol()
                raiz = None  # Reiniciar la raíz a None
            elif opcion == '7':
              break
            else:
               print("Opción inválida.")
        except ValueError:
            print("ERROR: Ingresaste un valor inválido.")
        except Exception as e:
            print(f"Error inesperado: {e}")
menu()