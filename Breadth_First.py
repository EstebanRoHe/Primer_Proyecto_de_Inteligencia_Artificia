import numpy as np
import matplotlib.pyplot as plt
import time
import psutil
import csv
import os
class ClassBreadth:
    def __init__(self, grid_file, start, goal):
        self.grid = np.genfromtxt(grid_file, delimiter=',')
        self.start = start
        self.goal = goal
        self.grid_name = os.path.splitext(os.path.basename(grid_file))[0]


    #para la estadisticas
    def time_and_memory(self, func, *args, **kwargs):
        start_time = time.time()
        start_memory = psutil.virtual_memory().used
        result = func(*args, **kwargs)
        end_time = time.time()
        end_memory = psutil.virtual_memory().used
        elapsed_time = end_time - start_time
        memory_used = end_memory - start_memory

        return result, elapsed_time, memory_used


    def write_csv(self, filename, stats):
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for stat in stats:
                elapsed_time_formatted = '{:.6f}'.format(stat['Elapsed Time (s)'])
                memory_used_formatted = str(stat['Memory Used (bytes)'])
                formatted_data = f"Algoritmo = {stat['Algorithm']}, Tiempo = {elapsed_time_formatted}, Memoria = {memory_used_formatted}"
                writer.writerow([formatted_data])

    #breadth
    def breadth(self):
            neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            close_set = set()
            came_from = {}
            queue = [self.start]
            
            while queue:
                current = queue.pop(0)
                if current == self.goal:
                    path = []
                    #crea la ruta
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.append(self.start)
                    path.reverse()
                    return path
                #agrega a visitados
                close_set.add(current)
                #hacer movimientos
                for i, j in neighbors:
                    neighbor = current[0] + i, current[1] + j
                    
                    if (
                        0 <= neighbor[0] < self.grid.shape[0]
                        and 0 <= neighbor[1] < self.grid.shape[1]
                        and self.grid[neighbor[0]][neighbor[1]] == 0
                        and neighbor not in close_set
                        and neighbor not in queue
                    ):
                        queue.append(neighbor)
                        came_from[neighbor] = current
            
            return False

    def breadth_algorithm(self):
        route = self.breadth()
        result, elapsed_time, memory_used = self.time_and_memory(self.breadth)
        if route:
            print("La ruta mas optima con breadth")
            print(route)

            x_coords = []
            y_coords = []


            for i in (range(0,len(route))):
                x = route[i][0]
                y = route[i][1]
                x_coords.append(x)
                y_coords.append(y)

            fig, ax = plt.subplots(figsize=(20, 20))
            ax.imshow(self.grid, cmap=plt.cm.Dark2)
            ax.scatter(self.start[1], self.start[0], marker="*", color="yellow", s=200)
            ax.scatter(self.goal[1], self.goal[0], marker="*", color="red", s=200)
            ax.plot(y_coords, x_coords, color="black")
            plt.show()
            
            result_matrix = np.zeros_like(self.grid)
            for punto in route:
                x, y = punto
                result_matrix[x][y] = 5
            result_matrix[self.grid == 1] = 1
            result_matrix[self.start] = 2
            result_matrix[self.goal] = 3
            
            np.savetxt(f'breadth_first{self.grid_name}.csv', result_matrix, delimiter=',', fmt='%d')
            stats = [{'Algorithm': 'Breadth', 'Elapsed Time (s)': elapsed_time, 'Memory Used (bytes)': memory_used}]
            self.write_csv(f'breadth_first_{self.grid_name}.txt', stats)
        else:
            print("No se encontró un camino hacia el objetivo.")

