import numpy as np
import matplotlib.pyplot as plt
import time
import psutil
import csv
import os
class ClassDepth:
    def __init__(self, grid_file, start, goal):
        self.grid = np.genfromtxt(grid_file, delimiter=',')
        self.start = start
        self.goal = goal
        self.grid_name = os.path.splitext(os.path.basename(grid_file))[0]


    # para la estadísticas
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

    #depth
    def depth(self):
        def depth_recursive(array, current, goal, close_set, path):
            neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            if current == goal:
                return path + [current]
            
            #agrega a visitados
            close_set.add(current)

            #hacer movimientos
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j

                if (
                    0 <= neighbor[0] < array.shape[0]
                    and 0 <= neighbor[1] < array.shape[1]
                    and array[neighbor[0]][neighbor[1]] == 0
                    and neighbor not in close_set
                ):
                    new_path = depth_recursive(array, neighbor, goal, close_set, path + [current])
                    if new_path:
                        return new_path

            return False 


        route = depth_recursive(self.grid, self.start, self.goal, set(), [])
        result, elapsed_time, memory_used = self.time_and_memory(depth_recursive, self.grid, self.start, self.goal, set(), [])

        if route:
            print("La ruta más óptima con Depth-First")
            print(route)

            x_coords, y_coords = zip(*route)
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
            
            np.savetxt(f'depth_first{self.grid_name}.csv', result_matrix, delimiter=',', fmt='%d')
            stats = [{'Algorithm': 'Depth', 'Elapsed Time (s)': elapsed_time, 'Memory Used (bytes)': memory_used}]
            self.write_csv(f'depth_first_{self.grid_name}.txt', stats)
            
        else:
            print("No se encontró un camino hacia el objetivo.")











