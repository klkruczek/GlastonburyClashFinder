import tkinter as tk
import pandas as pd
from tkinter import ttk


class ItemSelectionApp:
    def __init__(self, items):
        self.items = items
        self.filtered_items = items
        self.selected_items = []

        self.root = tk.Tk()
        self.root.title("Item Selection")

        self.create_widgets()
        self.update_list()

    def create_widgets(self):
        # Create a canvas with a scrollbar
        canvas = tk.Canvas(self.root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas
        self.frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Filter options
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(pady=10)

        title_label = tk.Label(self.filter_frame, text="Title:")
        title_label.pack(side=tk.LEFT)

        self.title_entry = tk.Entry(self.filter_frame, width=20)
        self.title_entry.pack(side=tk.LEFT)

        stage_label = tk.Label(self.filter_frame, text="Stage:")
        stage_label.pack(side=tk.LEFT)

        stages = list(set(item['stage'] for item in self.items))
        stages.insert(0, "All")
        stages.sort()
        self.stage_combobox = ttk.Combobox(self.filter_frame, values=stages, state="readonly")
        self.stage_combobox.current(0)
        self.stage_combobox.pack(side=tk.LEFT)

        apply_filter_button = tk.Button(self.filter_frame, text="Apply Filter", command=self.apply_filter)
        apply_filter_button.pack(side=tk.LEFT, padx=10)


        # Done button
        done_button = tk.Button(self.root, text="Done", command=self.finish_selection)
        done_button.pack(pady=10)

    def update_list(self):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        sorted_items = sorted(self.filtered_items, key=lambda item: (item['date'], item['start_time']))

        for i, item in enumerate(sorted_items):
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self.frame, text=f"{item['title']} - Stage: {item['stage']} - Date: {item['date']} - Start Time: {item['start_time']} - End Time: {item['end_time']}",
                                      variable=checkbox_var, command=lambda i=i: self.toggle_selection(i))
            checkbox.pack(anchor=tk.W)

    def toggle_selection(self, index):
        item = self.filtered_items[index]
        if item in self.selected_items:
            self.selected_items.remove(item)
        else:
            self.selected_items.append(item)

    def apply_filter(self):
        selected_title = self.title_entry.get().lower()
        selected_stage = self.stage_combobox.get()

        self.filtered_items = [item for item in self.items if
                               selected_title in item['title'].lower() and
                               (selected_stage == "All" or selected_stage == item['stage'])]

        self.update_list()

    def add_item(self):
        new_item = {
            'title': self.add_title_entry.get(),
            'stage': self.add_stage_entry.get(),
            'date': self.add_date_entry.get(),
            'start_time': self.add_start_time_entry.get(),
            'end_time': self.add_end_time_entry.get()
        }
        self.items.append(new_item)
        self.filtered_items.append(new_item)
        self.selected_items.append(new_item)
        self.update_list()

    def finish_selection(self):
        self.root.destroy()



dataset = pd.read_csv('glastonbury_2023_schedule.csv', header=0)

my_list = dataset.to_dict("records")

app = ItemSelectionApp(my_list)
app.root.mainloop()

selected_items = sorted(app.selected_items, key=lambda item: (item['date'], item['start_time']))

print("Selected items:")
for item in selected_items:
     print(f"{item['title']} - Date: {item['date']} - Stage: {item['stage']} - Time: {item['start_time']}-{item['end_time']}")



df = pd.DataFrame(selected_items)
df.to_csv('MyGlastoList.csv')