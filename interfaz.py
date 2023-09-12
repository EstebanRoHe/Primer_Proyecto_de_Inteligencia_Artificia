import tkinter as tk
from tkinter import ttk
from astar import ClassAstar
from Breadth_First import ClassBreadth
from Depth_First import ClassDepth
from Dijkstra import ClassDijkstra
laberinto = 'laberinto.csv'
start = (0, 0)
end = (31, 39)
def run_algorithm():
    selected_algorithm = algorithm_combobox.get()
    if selected_algorithm == "A*":
        print("Opcion de Algoritmo de A*")
        astar_instance = ClassAstar(laberinto, start , end)
        astar_instance.astar_algorithm()
        
    elif selected_algorithm == "Breadth":
        print("Opcion de Algoritmo de Breadth")
        breadth_instance = ClassBreadth(laberinto, start , end)
        breadth_instance.breadth_algorithm()
        
    elif selected_algorithm == "Depth":
        print("Opcion de Algoritmo de Depth")
        depth_instance = ClassDepth(laberinto, start , end)
        depth_instance.depth()
    
        
    elif selected_algorithm == "Dijkstra":
        print("Opcion de Algoritmo de Dijkstra")
        dijkstra_instance = ClassDijkstra(laberinto, start , end)
        dijkstra_instance.dijkstra_algorithm()

window = tk.Tk()
window.title("Algoritmos de busqueda")
window.geometry("600x400")
label = ttk.Label(window, text="Selecciona un algoritmo:")
label.pack(pady=10)
algorithms = ["A*", "Breadth", "Depth", "Dijkstra"]
algorithm_combobox = ttk.Combobox(window, values=algorithms)
algorithm_combobox.pack()
run_button = ttk.Button(window, text="Ejecutar", command=run_algorithm)
run_button.pack(pady=10)

window.mainloop()
