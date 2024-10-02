import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Extensión del gráfico
y_max = 161
x_max = 101

#Condición de corte
epsilon_convergencia = 1
max_dif = float('inf')

bornes = [
    {'pot': 12, 'x': 50, 'y': 120}, # Borne con potencial "pot" expresado en V, con posición (x,y)
    {'pot': -12, 'x': 51, 'y': 100}
]

# Auxiliares para comprobar si un punto es borne (no será actualizado)
bornes_x = np.zeros(x_max)
bornes_y = np.zeros(y_max)

def es_borne(coord_x, coord_y): # Debería ser O(1)
    #return next((True for borne in bornes if (borne['x'] == coord_x and borne['y'] == coord_y)), False)
    return (bornes_x[coord_x] != 0 and bornes_y[coord_y] != 0) and (bornes_x[coord_x] == bornes_y[coord_y])

# Creación de una malla de puntos en 2D
x = np.linspace(0, x_max, x_max)
y = np.linspace(0, y_max, y_max)
X, Y = np.meshgrid(x, y)

# Inicialización del potencial eléctrico (matriz)
V_total = np.zeros_like(X)

# Actualizo la matriz con los bornes ya definidos
for id_borne, borne in enumerate(bornes):
    V_total[borne['y'], borne['x']] = borne['pot']
    bornes_x[borne['x']] = id_borne+1 # estructuras auxiliares para "detectar" bornes
    bornes_y[borne['y']] = id_borne+1

# Función para calcular el promedio entre los vecinos
def promedio_vecinos(coord_y, coord_x):
    cant_vecinos = 0 # la cantidad de vecinos puede variar, e.g. 1) esquina tendrá sólo dos vecinos 2) elemento en borde tendrá sólo tres
    suma_vecinos = 0
    if (coord_x-1 >= 0): # si hay vecino izq
        cant_vecinos += 1
        suma_vecinos += V_total[coord_y, coord_x-1]
    if (coord_x+1 < V_total.shape[1]): # si hay vecino der
        cant_vecinos += 1
        suma_vecinos += V_total[coord_y, coord_x+1]
    if (coord_y-1 >= 0): # si hay vecino inf
        cant_vecinos += 1
        suma_vecinos += V_total[coord_y-1, coord_x]
    if (coord_y+1 < V_total.shape[0]): # si hay vecino der
        cant_vecinos += 1
        suma_vecinos += V_total[coord_y+1, coord_x]
    return suma_vecinos/cant_vecinos

# Ciclo principal
while max_dif >= epsilon_convergencia:
    max_iteracion = 0
    for iy, ix in np.ndindex(V_total.shape): # Iteración de cálculo de promedios para la grilla entera
        if not es_borne(ix, iy): # Los bornes tendrán sus valores de potencial siempre fijos, entonces para cada elemento no-borne
            nuevo_valor = promedio_vecinos(iy, ix)
            dif = abs(nuevo_valor - V_total[iy, ix])
            if dif > max_iteracion:
                max_iteracion = dif
            V_total[iy, ix] = nuevo_valor # se actualiza el valor
    max_dif = max_iteracion # se actualiza la máxima diferencia por iteración

# Generación de gráficos
plot_base = plt.figure(figsize=(16,9))
plot = plot_base.add_subplot(121)

# Graficar: ejes y grilla
plot.set_xlabel('$x$')
plot.set_ylabel('$y$')
plot.set_xlim(0,x_max)
plot.set_ylim(0,y_max)
plot.set_aspect('equal')
plot.grid(True)

# Graficar: Potencial eléctrico
plt.contourf(X, Y, V_total, 20, cmap='seismic')

#Títulos y barra de colores de potencial
plt.title("Potencial eléctrico")
plt.colorbar(label="Potencial (V)")

#plt.figure(figsize=(10, 10))
plot = plot_base.add_subplot(122, projection='3d')
sup_potencial= plot.plot_surface(X,Y,V_total, rstride=1, cstride=1,cmap='seismic',edgecolor='none')
#sup_potencial = plt.axes(projection='3d').plot_surface(X,Y,V_total, rstride=1, cstride=1,cmap='seismic',edgecolor='none')
plt.colorbar(sup_potencial,label="Potencial (V)")

plt.savefig("labo2_combinado_1.jpg", bbox_inches='tight')
#plt.show()

# Notas del asistente:
    # Debería manejar bornes con formas, no puntuales
    # Informe es igual que el anterior: explicar la física de lo que se ve en los gráficos
    # Recomendó explicar un poco de la algoritmia
