import tkinter as tk
from tkinter import messagebox, PhotoImage
import os

# Sample store items (name, price, value, image)
items = [
    ("Laptop", 700, 90, "laptop.png"),
    ("Phone", 500, 80, "phone.png"),
    ("Headphones", 150, 40, "headphones.png"),
    ("Book", 100, 30, "book.png"),
    ("Bag", 200, 50, "bag.png"),
]

budget = 1000
selected_items = []

def update_selection():
    total_cost = sum(item[1] for item in selected_items)
    total_value = sum(item[2] for item in selected_items)
    selection_label.config(text=f"Total Cost: {total_cost} / {budget}\nTotal Value: {total_value}")

def select_item(index, btn):
    global selected_items
    item = items[index]
    total_cost = sum(i[1] for i in selected_items)
    
    if total_cost + item[1] <= budget:
        selected_items.append(item)
        update_selection()
    else:
        messagebox.showwarning("Budget Exceeded", "You can't afford this item!")

def reset_game():
    global selected_items
    selected_items = []
    update_selection()

def knapsack_optimal():
    n = len(items)
    w = budget
    dp = [[0 for _ in range(w + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item_name, item_weight, item_value, _ = items[i - 1]
        for j in range(w + 1):
            if item_weight <= j:
                dp[i][j] = max(dp[i - 1][j], item_value + dp[i - 1][j - item_weight])
            else:
                dp[i][j] = dp[i - 1][j]
    
    # Retrieve selected items
    optimal_selection = []
    j = w
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            optimal_selection.append(items[i - 1])
            j -= items[i - 1][1]
    
    messagebox.showinfo("Optimal Selection", f"Best items to buy: {', '.join(i[0] for i in optimal_selection)}")

def load_images():
    image_dict = {}
    for name, _, _, image in items:
        try:
            if os.path.exists(image):
                image_dict[name] = PhotoImage(file=image)
            else:
                print(f"Warning: {image} not found! Using placeholder.")
                image_dict[name] = PhotoImage(width=50, height=50)  # Placeholder image
        except Exception as e:
            print(f"Error loading image {image}: {e}")
            image_dict[name] = PhotoImage(width=50, height=50)  # Placeholder image
    return image_dict

# Create GUI window
root = tk.Tk()
root.title("Budget Shopping Assistant")
root.geometry("600x500")
root.configure(bg="lightblue")

# Load images
images = load_images()

# Create item buttons
for i, (name, price, value, image) in enumerate(items):
    frame = tk.Frame(root, bg="lightblue")
    frame.pack(pady=5)
    
    img_label = tk.Label(frame, image=images[name], bg="lightblue")
    img_label.pack(side="left")
    
    btn = tk.Button(frame, text=f"{name} (₹{price}, V:{value})", command=lambda i=i: select_item(i, btn))
    btn.pack(side="left", padx=10)

# Display selected items
selection_label = tk.Label(root, text="Total Cost: 0 / 1000\nTotal Value: 0", font=("Arial", 12), bg="lightblue")
selection_label.pack(pady=10)

# Reset button
reset_btn = tk.Button(root, text="Reset", command=reset_game, bg="red", fg="white")
reset_btn.pack(pady=10)

# Optimal selection button
optimal_btn = tk.Button(root, text="Find Best Selection", command=knapsack_optimal, bg="green", fg="white")
optimal_btn.pack(pady=10)

root.mainloop()
