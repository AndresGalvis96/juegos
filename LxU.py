
#######################Importación de librerías################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from scipy.linalg import lu_factor, lu_solve
import numpy as np

#######################Creación de la clase################################
class MatrixSolver:

    #Función para iniciar la ventana 
    def __init__(self, master):
        self.master = master
        self.new_window = None
        #Color de fondo
        self.master.configure(background="#dadad9")
        #Título de la ventana
        self.master.title("Descomposición LU y solución de sistemas 3x3")

        # Creación del 'frame' de entrada para la matriz A
        self.input_frame = ttk.Frame(self.master, padding="10")
        #posición del frame usando puntos cardinales
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        # crear matriz de coef. A
        ttk.Label(self.input_frame, text="Matriz A").grid(row=0, column=1)
        self.coefficients = []
        for i in range(3):
            for j in range(3):
                #crear objeto de entrada para cada coef.
                coef = ttk.Entry(self.input_frame, width=5)
                #Configuración tamaño y posición de los objetos de entrada
                coef.grid(row=i+1, column=j, padx=5, pady=5)
                #Agregar los valores a la lista de cofeicientes.
                self.coefficients.append(coef)

        # Creamos entradas para los términos independientes
        self.independent_vars = []
        for i in range(3):
            #Objetos de entrada para cada var.
            var = ttk.Entry(self.input_frame, width=5)
            #posición y tamaño para cada var.
            var.grid(row=i+1, column=4, padx=5, pady=5)
            #Añadimos los valores a la lista de variables independientes.
            self.independent_vars.append(var)
            ttk.Label(self.input_frame, text="B =").grid(row=i+1, column=3)


        # creación del botón "Resolver" que llama al método 'calculate'
        self.solve_button = ttk.Button(self.master, text="Resolver", command=self.calculate)
        # Posición del botón Resolver
        self.solve_button.grid(row=1, column=0, padx=10, pady=10)

        #Creación del botón para Limpiar los campos de A y B
        self.btn_clear = ttk.Button(self.master, text="Limpiar", command=self.limpiar)
        #Pos de limpiar
        self.btn_clear.grid(row=1, column=1, pady=10)

    #Función para validar campos numéricos
    def validar_campos(self):
        for coef in self.coefficients:
            if not (coef.get().isdigit() or coef.get().lstrip('-').isdigit()):
                messagebox.showerror("Error", "Debe ingresar valores numéricos")
                return False
        for var in self.independent_vars:
            if not (var.get().isdigit() or var.get().lstrip('-').isdigit()):
                messagebox.showerror("Error", "Las variables independientes deben ser números")
                return False
        return True

    #######Función principal "Calcular"#########
    def calculate(self):
        #Llamada a validar_campos antes de calcular
        if not self.validar_campos():
            return

        # obtenemos y almacenamos los valores de las matrices

        coef_values = [float(coef.get()) for coef in self.coefficients]
        var_values = [float(var.get()) for var in self.independent_vars]

        # Crear A y B con forma de matrices
        A = np.array(coef_values).reshape((3, 3))
        B = np.array(var_values).reshape((3, 1))

        # Calcular el determinante de la matriz
        detA = np.linalg.det(A)

        # Verificar si la matriz tiene solución
        if detA != 0:
            print("La matriz tiene solución")
            # Calcular L y U a partir de A
            L, U = lu_factor(A)
            l = np.tril(A)
            u = np.triu(A)
            # Resolver y almacenar valores de las X
            X = lu_solve((L, U), B)

            #salidas de prueba.
            print("valores de U: ",u)
            print("Valores de L: " , l)

            ######################## Crear la ventana de salidas ############################
            root = tk.Tk()
            root.title("Matrices L y U")

            # Título para la matriz L
            lbl_L = tk.Label(root, text="Matriz L:")
            lbl_L.grid(row=0, column=0, padx=10, pady=10)

            # Título para la matriz U
            lbl_U = tk.Label(root, text="Matriz U:")
            lbl_U.grid(row=0, column=6, padx=10, pady=10)
        #######Calcular L y U por descomposición######

        #Declaración de las matrices para segundo método #
            matrizLl = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            matrizUu = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            vectorZ = [0, 0, 0]
            vectorX = [0, 0, 0]

            # Inicialización de variables complementarias
            n = 3
            suma = 0

            # Inicialización de matriz L y matriz U
            for i in range(n):
                matrizLl[i][i] = 1
            #Ciclo para filas
            for i in range(n):
                #ciclo para columnas
                for j in range(i, n):
                    suma = 0
                    #Ciclo para registrar valores L y U
                    for k in range(i):
                        suma += matrizLl[i][k] * matrizUu[k][j]
                        #Almacenar valores de U
                    matrizUu[i][j] = A[i][j] - suma

                    suma = 0
                    for k in range(i):
                        suma += matrizLl[j][k] * matrizUu[k][i]
                        #Almacenar valores de L
                    matrizLl[j][i] = (A[j][i] - suma) / matrizUu[i][i]

            # Mostrar resultados
            print("Matriz L:")
            for i in range(n):
                for j in range(n):
                    print(matrizLl[i][j], end=" ")
                print()

            print("Matriz U:")
            for i in range(n):
                for j in range(n):
                    print(matrizUu[i][j], end=" ")
                print()


            # Graficar la matriz L con la diagonal en 1 y la superior en ceros.
            for i in range(3):
                for j in range(3):
                    if j > i:
                        label = ttk.Label(root, text="0.0000", width=6, borderwidth=1, relief="solid")
                    elif j == i:
                        label = ttk.Label(root, text="1.0000", width=6, borderwidth=1, relief="solid")
                    else:
                        label = ttk.Label(root, text=f"{matrizLl[i][j]:.4f}", width=6, borderwidth=1, relief="solid")
                    label.grid(row=i + 1, column=j, padx=5, pady=5)


            # Convertir la matriz U en una matriz triangular superior completa
            U_tri = np.triu(U)

            #Graficar matriz U en una matriz triangular superior
            for i in range(3):
                for j in range(3):
                    if j < i:
                        lbl = tk.Label(root, text="0.0000", width=6, borderwidth=1, relief="solid")
                    else:
                        lbl = tk.Label(root, text=f"{matrizUu[i][j]:.4f}", width=6, borderwidth=1, relief="solid")
                    lbl.grid(row=i+1, column=j+6, padx=5, pady=5)
            #Salida de Z
            # Calcular valores del vector Z
            for i in range(n):
                suma = 0
                for j in range(i):
                    suma += matrizLl[i][j] * vectorZ[j]
                vectorZ[i] = (B[i] - suma) / matrizLl[i][i]


            # Título de la solución de X
            lbl_X = tk.Label(root, text="Solución X:")
            lbl_X.grid(row=4, column=0, padx=10, pady=10)

            #Graficar salida de X
            for i, x in enumerate(X):
                label = ttk.Label(root, text=str(f"{x[0]:.4f}"), width=6, borderwidth=1, relief="solid")
                label.grid(row=i + 5, column=0, padx=5, pady=5)

            lbl_Z = tk.Label(root, text="Matriz Z:")
            lbl_Z.grid(row=4, column=6, padx=10, pady=10)
            for j, z in enumerate(vectorZ):
                value = z
                ttk.Label(root, text=str(f"{z[0]:.4f}"), width=6, borderwidth=1, relief="solid").grid(row=j+5, column=6, padx=5, pady=5)
        else:
            print("La matriz no tiene solución")
            messagebox.showinfo(title="Sin Solución", message="La matriz no tiene solución")

    ##Limpiar campos##
    def limpiar(self):
        # Borra el contenido de los campos de entrada para los coeficientes
        for coef in self.coefficients:
            coef.delete(0, tk.END)

        # Borra el contenido de los campos de entrada para las variables independientes
        for var in self.independent_vars:
            var.delete(0, tk.END)

##Mantener la ventana principal Activa en bucle##
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixSolver(root)
    root.mainloop()

