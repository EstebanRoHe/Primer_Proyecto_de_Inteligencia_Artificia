import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import time
import psutil
import csv
import os
class ClassAstar:
    def __init__(self, grid_file, start, goal):
        self.grid = np.genfromtxt(grid_file, delimiter=',')
        self.start = start
        self.goal = goal
        self.grid_name = os.path.splitext(os.path.basename(grid_file))[0]
    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

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

    #astar
    def astar(self):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        close_set = set()
        came_from = {}
        gscore = {self.start:0}
        fscore = {self.start:self.heuristic(self.start, self.goal)}
        priority_queue = []
        heapq.heappush(priority_queue, (fscore[self.start], self.start))
    
        while priority_queue:
            current = heapq.heappop(priority_queue)[1]

            if current == self.goal:
                path = []
                #crear la ruta
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path.reverse()
                return path
            
            #agrega visitados
            close_set.add(current)

            #hacer movimientos
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
                if( 
                    0 <= neighbor[0] < self.grid.shape[0]
                    and 0 <= neighbor[1] < self.grid.shape[1]
                    and self.grid[neighbor[0]][neighbor[1]] == 0
                ):
                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue

                    if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in priority_queue]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                        heapq.heappush(priority_queue, (fscore[neighbor], neighbor))
    
        return False

    def astar_algorithm(self):
        route = self.astar()
        result, elapsed_time, memory_used = self.time_and_memory(self.astar)
        if route:
            x_coords = []
            y_coords = []
            print(self.grid_name)
            print("La ruta más óptima con A*")
            print(route)

            for i in range(len(route)):
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
            np.savetxt(f'a_start{self.grid_name}.csv', result_matrix, delimiter=',', fmt='%d')
            stats = [{'Algorithm': 'A*', 'Elapsed Time (s)': elapsed_time, 'Memory Used (bytes)': memory_used}]
            self.write_csv(f'a_start_{self.grid_name}.txt', stats)

        else:
            print("No se encontró un camino hacia el objetivo.")
