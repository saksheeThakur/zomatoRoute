import tkinter as tk
from tkinter import messagebox
import heapq

class DeliveryRouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Optimization (A* Algorithm)")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f0")

        self.graph = {}

        # Title
        tk.Label(root, text="Delivery Route Finder", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        # Input Frame
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=5)

        tk.Label(self.frame, text="From:", bg="#f0f0f0").grid(row=0, column=0)
        self.start_entry = tk.Entry(self.frame, width=5)
        self.start_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="To:", bg="#f0f0f0").grid(row=0, column=2)
        self.end_entry = tk.Entry(self.frame, width=5)
        self.end_entry.grid(row=0, column=3)

        tk.Label(self.frame, text="Distance:", bg="#f0f0f0").grid(row=0, column=4)
        self.distance_entry = tk.Entry(self.frame, width=5)
        self.distance_entry.grid(row=0, column=5)

        self.add_button = tk.Button(self.frame, text="Add Route", command=self.add_route, bg="#4CAF50", fg="white")
        self.add_button.grid(row=0, column=6, padx=5)

        # Start and End Node Inputs
        tk.Label(root, text="Start Location:", bg="#f0f0f0").pack()
        self.start_location_entry = tk.Entry(root)
        self.start_location_entry.pack()

        tk.Label(root, text="Destination:", bg="#f0f0f0").pack()
        self.destination_entry = tk.Entry(root)
        self.destination_entry.pack()

        # Buttons
        self.find_button = tk.Button(root, text="Find Best Route", command=self.find_best_route, bg="#008CBA", fg="white")
        self.find_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0", fg="black")
        self.result_label.pack(pady=10)

        self.graph_text = tk.Text(root, height=10, width=50)
        self.graph_text.pack()

    def add_route(self):
        node1 = self.start_entry.get().strip()
        node2 = self.end_entry.get().strip()
        distance = self.distance_entry.get().strip()

        if not node1 or not node2 or not distance.isdigit():
            messagebox.showerror("Input Error", "Please enter valid locations and a numeric distance.")
            return

        distance = int(distance)

        # Adding the route to the graph (Bidirectional)
        if node1 not in self.graph:
            self.graph[node1] = {}
        if node2 not in self.graph:
            self.graph[node2] = {}

        self.graph[node1][node2] = distance
        self.graph[node2][node1] = distance

        # Update the graph display
        self.graph_text.insert(tk.END, f"{node1} --({distance} km)--> {node2}\n")

        # Clear input fields
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)

    def a_star(self, start, goal):
        open_list = [(0, start)]
        g_costs = {node: float('inf') for node in self.graph}
        g_costs[start] = 0
        came_from = {}

        while open_list:
            current_cost, current_node = heapq.heappop(open_list)

            if current_node == goal:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(start)
                path.reverse()
                return path, g_costs[goal]

            for neighbor, weight in self.graph[current_node].items():
                new_cost = g_costs[current_node] + weight
                if new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    priority = new_cost
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current_node

        return None, float('inf')

    def find_best_route(self):
        start_node = self.start_location_entry.get().strip()
        destination = self.destination_entry.get().strip()

        if start_node not in self.graph or destination not in self.graph:
            messagebox.showerror("Input Error", "Start or Destination not found in the graph!")
            return

        path, cost = self.a_star(start_node, destination)
        
        if path:
            result_text = f"Best Route: {' → '.join(path)}\nTotal Distance: {cost} km"
        else:
            result_text = "No route found!"

        self.result_label.config(text="Optimal Delivery Route:")
        self.graph_text.delete(1.0, tk.END)
        self.graph_text.insert(tk.END, result_text)

# Run the Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryRouteApp(root)
    root.mainloop()