import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

nombre_imagen_salida = "labo2_g14.png" # Aporta flexibilidad para generar distintos resultados y compararlos

# Condición de corte
epsilon_convergencia = .01

# Formas a dibujar. Considerar una malla de 101 en X y 161 en Y
rectangulos = [
    {'extremo_inf_x': 20, 'extremo_inf_y': 125, 'ancho': 10, 'alto': 10, 'valor_pot': 9},
    {'extremo_inf_x': 40, 'extremo_inf_y': 80, 'ancho': 15, 'alto': 10, 'valor_pot': 16}
]

circulos = [
   {'centro_x': 50, 'centro_y': 30, 'radio': 5, 'valor_pot': -16}
]

# Creación de una malla de puntos en 2D
# Extensión del gráfico
y_max = 161
x_max = 101
x = np.linspace(0, x_max, x_max)
y = np.linspace(0, y_max, y_max)
X, Y = np.meshgrid(x, y)

# Inicialización del potencial eléctrico (matriz)
V_total = np.zeros_like(X)
grilla_control = np.zeros_like(X) # Estructura auxiliar para "detectar" bornes (sus valores son fijos)

def es_borne(coord_x, coord_y):
    return grilla_control[coord_y, coord_x] == 1 # En la estructura auxiliar los bornes serán 1, sino serán 0

def dibujar_rectangulo(extremo_sup, ancho, alto, valor_pot):
    y1, x1 = extremo_sup
    y2, x2 = y1 + alto, x1 + ancho
    V_total[y1:y2, x1:x2] = valor_pot
    grilla_control[y1:y2, x1:x2] = 1

def dibujar_circulo(centro, radio, valor_pot):
    yc, xc = centro
    for y in range(V_total.shape[0]):
        for x in range(V_total.shape[1]):
            if (x - xc) ** 2 + (y - yc) ** 2 <= radio ** 2:
                V_total[y, x] = valor_pot
                grilla_control[y, x] = 1

# Se "dibujan" las formas con valores de potencial
for rectangulo in rectangulos:
    dibujar_rectangulo((rectangulo['extremo_inf_y'], rectangulo['extremo_inf_x']), rectangulo['ancho'], rectangulo['alto'], rectangulo['valor_pot'])

for circulo in circulos:
    dibujar_circulo((circulo['centro_y'], circulo['centro_x']), circulo['radio'], circulo['valor_pot'])

# Función para calcular el promedio entre los vecinos
def promedio_vecinos(coord_y, coord_x):
    suma_potencial_vecinos = 0
    cant_vecinos = 0 # la cantidad de vecinos puede variar
    # e.g. 1) esquina tendrá sólo dos vecinos 2) elemento en borde (gráfico) tendrá sólo tres
    if (coord_x-1 >= 0): # si hay vecino izq
        cant_vecinos += 1
        suma_potencial_vecinos += V_total[coord_y, coord_x-1]
    if (coord_x+1 < V_total.shape[1]): # si hay vecino der
        cant_vecinos += 1
        suma_potencial_vecinos += V_total[coord_y, coord_x+1]
    if (coord_y-1 >= 0): # si hay vecino inf
        cant_vecinos += 1
        suma_potencial_vecinos += V_total[coord_y-1, coord_x]
    if (coord_y+1 < V_total.shape[0]): # si hay vecino der
        cant_vecinos += 1
        suma_potencial_vecinos += V_total[coord_y+1, coord_x]
    return suma_potencial_vecinos/cant_vecinos

def indices(matriz):
    return np.ndindex(matriz.shape)

# Ciclo principal
max_dif = float('inf') # Maximo valor "real" dado por Python. Auxiliar para hallar la maxima diferencia
while max_dif >= epsilon_convergencia:
    maxdif_esta_iteracion = 0
    for iy, ix in indices(V_total): # Iteración para la grilla entera
        if not es_borne(ix, iy): # Sólo los puntos no-borne se actualizan
            nuevo_valor = promedio_vecinos(iy, ix)
            dif = abs(nuevo_valor - V_total[iy, ix])
            if dif > maxdif_esta_iteracion:
                maxdif_esta_iteracion = dif
            V_total[iy, ix] = nuevo_valor # se actualiza el valor
    max_dif = maxdif_esta_iteracion # se actualiza la máxima diferencia por iteración

# Generación de gráficos
plot_base = plt.figure(figsize=(16,9))
plot = plot_base.add_subplot(121)

# Graficar: ejes y gr120illa
plot.set_xlabel("$x$ \n Épsilon de convergencia: " + str(epsilon_convergencia))
plot.set_ylabel('$y$')
plot.set_xlim(0,x_max)
plot.set_ylim(0,y_max)
plot.set_aspect('equal')
plot.grid(True)

# Graficar: Potencial eléctrico
plt.contourf(X, Y, V_total, 25, cmap='seismic')

#Títulos y barra de colores de potencial
plt.title("Potencial eléctrico")
plt.colorbar(label="Potencial (V)")

plot = plot_base.add_subplot(122, projection='3d')
sup_potencial= plot.plot_surface(X,Y,V_total, rstride=1, cstride=1,cmap='seismic',edgecolor='none')
plt.colorbar(sup_potencial,label="Potencial (V)")

plt.savefig(nombre_imagen_salida, bbox_inches='tight')
plt.show()
plt.close()