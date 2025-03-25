import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Event:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"{self.name} ({self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')})"

def merge_sort(events):
    if len(events) > 1:
        mid = len(events) // 2
        left_half = events[:mid]
        right_half = events[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i].start_time < right_half[j].start_time:
                events[k] = left_half[i]
                i += 1
            else:
                events[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            events[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            events[k] = right_half[j]
            j += 1
            k += 1

    return events

def schedule_events(events):
    return merge_sort(events)

class EventSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Scheduler")
        self.events = []

        tk.Label(root, text="Event Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Start Time (e.g., 2:00 PM)").grid(row=1, column=0)
        self.start_time_entry = tk.Entry(root)
        self.start_time_entry.grid(row=1, column=1)

        tk.Label(root, text="End Time (e.g., 3:00 PM)").grid(row=2, column=0)
        self.end_time_entry = tk.Entry(root)
        self.end_time_entry.grid(row=2, column=1)

        tk.Button(root, text="Add Event", command=self.add_event).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Sort Events", command=self.sort_events).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Delete Event", command=self.delete_event).grid(row=6, column=0)
        tk.Button(root, text="Edit Event", command=self.edit_event).grid(row=6, column=1)

        self.events_listbox = tk.Listbox(root, width=50)
        self.events_listbox.grid(row=5, column=0, columnspan=2)

    def add_event(self):
        name = self.name_entry.get()
        try:
            start_time = datetime.strptime(self.start_time_entry.get(), "%I:%M %p")
            end_time = datetime.strptime(self.end_time_entry.get(), "%I:%M %p")

            if start_time >= end_time:
                raise ValueError("Start time must be less than end time")

            if name:
                event = Event(name, start_time, end_time)
                self.events.append(event)
                self.events_listbox.insert(tk.END, event)
                self.clear_entries()
            else:
                messagebox.showwarning("Input Error", "Please enter all event details.")

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")

    def sort_events(self):
        self.events = schedule_events(self.events)
        self.events_listbox.delete(0, tk.END)
        for event in self.events:
            self.events_listbox.insert(tk.END, event)

    def delete_event(self):
        try:
            selected_index = self.events_listbox.curselection()[0]
            del self.events[selected_index]
            self.events_listbox.delete(selected_index)
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an event to delete.")

    def edit_event(self):
        try:
            selected_index = self.events_listbox.curselection()[0]
            event = self.events[selected_index]

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, event.name)
            self.start_time_entry.delete(0, tk.END)
            self.start_time_entry.insert(0, event.start_time.strftime("%I:%M %p"))
            self.end_time_entry.delete(0, tk.END)
            self.end_time_entry.insert(0, event.end_time.strftime("%I:%M %p"))

            self.delete_event()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an event to edit.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EventSchedulerApp(root)
    root.mainloop()
