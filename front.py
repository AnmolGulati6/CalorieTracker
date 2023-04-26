import tkinter as tk
from tkinter import messagebox
import csv

# read data from CSV file into a dictionary
foods = {}
with open('food.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        foods[row['food']] = int(row['calories'])

# create a Tkinter window
root = tk.Tk()
root.title("Calorie Tracker")

# create labels and entry fields for food name and quantity
food_label = tk.Label(root, text="Food:")
food_label.grid(row=0, column=0, padx=5, pady=5)
food_var = tk.StringVar()
food_var.set('Select a food')
food_options = list(foods.keys())
food_options.insert(0, 'Select a food')
food_dropdown = tk.OptionMenu(root, food_var, *food_options)
food_dropdown.grid(row=0, column=1, padx=5, pady=5)

quantity_label = tk.Label(root, text="Quantity (in grams):")
quantity_label.grid(row=1, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=1, column=1, padx=5, pady=5)

# create a listbox to display the meal items and calorie count
meal_list = tk.Listbox(root, height=10)
meal_list.grid(row=2, column=0, columnspan=3, padx=5, pady=5)


# create a function to add the food item and its calorie count to the meal list
def add_food():
    food_name = food_var.get()
    quantity = quantity_entry.get()
    # check if the quantity is a valid integer
    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a valid integer.")
        return
    # check if the quantity is greater than 0
    if quantity <= 0:
        messagebox.showerror("Error", "Quantity must be greater than 0.")
        return
    # check if the food item is in the database
    if food_name in foods:
        calories = foods[food_name] * quantity / 100
        meal_list.insert(tk.END, f"{food_name} ({quantity}g) - {calories:.0f} calories")
    else:
        messagebox.showerror("Error", f"Food item '{food_name}' not found in database.")


# create a button to add the food item to the meal list
add_button = tk.Button(root, text="Add", command=add_food)
add_button.grid(row=1, column=2, padx=5, pady=5)


# create a function to delete the selected item from the meal list
def delete_food():
    selection = meal_list.curselection()
    if selection:
        meal_list.delete(selection)


# create a button to delete the selected item from the meal list
delete_button = tk.Button(root, text="Delete", command=delete_food)
delete_button.grid(row=3, column=0, padx=5, pady=5)


# create a function to calculate and display the total calorie count for the meal
def calculate_calories():
    total_calories = 0
    for item in meal_list.get(0, tk.END):
        item_calories = int(item.split("-")[1].strip()[:-9])
        total_calories += item_calories
    total_calories_label.config(text=f"Total calories: {total_calories:.0f}")


# create a button to calculate the total calorie count for the meal
calculate_button = tk.Button(root, text="Calculate", command=calculate_calories)
calculate_button.grid(row=4, column=0, padx=5, pady=5)

# create a label to display the total calorie count for the meal
total_calories_label = tk.Label(root, text="")
total_calories_label.grid(row=4, column=1, padx=5, pady=5)

# run the Tkinter event loop
root.mainloop()
