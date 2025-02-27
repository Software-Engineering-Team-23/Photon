import tkinter as tk
from tkinter import messagebox, simpledialog
import sql
from udp import udp_sender
from udp import IP

class firstScreen:
    def __init__(self, window):
        window.title("Entry Terminal")
        window.geometry("800x700")
        window.configure(bg="black")
        self.player_entries = {}  # Key-value dictionary with key=PlayerID_entry and value=name_label
        self.equipment_entries = []  # List holding EquipmentID Tkinter entries

        title = tk.Label(window, text="Edit Game", bg="blue", fg="white", font=("Arial", 27, "bold"))
        title.pack()

        main_frame = tk.Frame(window, bg="gray")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=200, pady=40)

        red_frame = tk.Frame(main_frame, bg="red", width=500, height=900)
        red_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.make_rows(red_frame, "red", 20)

        green_frame = tk.Frame(main_frame, bg="green", width=500, height=900)
        green_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.make_rows(green_frame, "green", 20)

        button_frame = tk.Frame(main_frame, bg="gray", width=200, height=300, highlightbackground="black", highlightthickness=4)
        button_frame.pack(pady=5, padx=5)
        button_frame.pack_propagate(False)

        button = tk.Button(button_frame, text="F1 Edit Game", bg="black", fg="white", width=100)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F3 Start Game", bg="black", fg="white", width=100)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F8 View Game", bg="black", fg="white", width=100)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F11 Change Network", bg="black", fg="white", width=100, command=self.change_network)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F12 Clear Game", bg="black", fg="white", width=100, command=self.clear_game)
        button.pack(padx=5, pady=5)

    def change_network(self):
        new_network = simpledialog.askstring("Input", "Enter new network")
        IP = new_network
        print("The new network is:", IP)

    def clear_game(self):
        sql.delete_table("players")
        sql.create_table()
        print("Cleared game successfully")

        for entry, name_label in self.player_entries.items():
            entry.delete(0, tk.END)
            name_label.config(text="")
        
        for entry in self.equipment_entries:
            entry.delete(0, tk.END)
    
    def make_headers(self, frame, bg_color):
        row_frame = tk.Frame(frame, bg=bg_color)
        row_frame.pack(fill=tk.X, padx=5, pady=1)
        label = tk.Label(row_frame, text="  ", bg=bg_color, font=("Helvetica", 20))
        label.pack(side=tk.LEFT, padx=5)
        player_id_header = tk.Label(row_frame, text="Player ID", bg=bg_color, font=("Helvetica", 14, "bold"))
        player_id_header.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)
        equipment_id_header = tk.Label(row_frame, text="Equipment ID", bg=bg_color, font=("Helvetica", 14, "bold"))
        equipment_id_header.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)
        name_header = tk.Label(row_frame, text="Name", bg=bg_color, font=("Helvetica", 14, "bold"))
        name_header.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)

    def make_rows(self, frame, bg_color, num_rows):
            # Create rows and headers for each team
            self.make_headers(frame, bg_color)

            for row in range(num_rows):
                row_frame = tk.Frame(frame, bg=bg_color)
                row_frame.pack(fill=tk.X, padx=5, pady=1)

                label = tk.Label(row_frame, text=f"{row}", bg=bg_color, font=("Helvetica", 20))
                label.pack(side=tk.LEFT, padx=5)

                # Entry fields for player ID
                player_id_entry = tk.Entry(row_frame, bg="white", fg="black", width=5)
                player_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                # Entry fields for equipment ID
                equipment_id_entry = tk.Entry(row_frame, bg="white", fg="black", width=5)
                equipment_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                self.equipment_entries.append(equipment_id_entry)

                # Display codename to the right of player ID
                name_label = tk.Label(row_frame, bg="white", fg="black")
                name_label.pack(side=tk.LEFT, fill=tk.X, expand=False, padx=5)
                self.player_entries[player_id_entry] = name_label

                player_id_entry.bind("<Return>", lambda event, e=player_id_entry, r=row: self.submit_player_id(e))
                equipment_id_entry.bind("<Return>", lambda event, e=equipment_id_entry, r=row: self.submit_equipment_id(e))



    def submit_equipment_id(self, entry):
        # Get entry value. If in use, exit the function.
        value = entry.get().strip()
        try:
            if value == "":
                return
            elif value in map(lambda e: e.get().strip() if e != entry else "", self.equipment_entries): # Checks if value is in entered IDs
                messagebox.showerror("Error", "Invalid submission. Equipment ID currently in use")
                entry.delete(0, tk.END)
                return
            value = int(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid submission. Enter an integer ID")
            entry.delete(0, tk.END)
            return
        udp_sender(value)
        messagebox.showinfo("Info", f"Equipment ID {value} transmitted")

    def submit_player_id(self, entry):
        # Get entry value. If empty, clear name label and exit function. If in use, also exit.
        value = entry.get().strip()
        try:
            if value == "":
                self.player_entries[entry].config(text="")
                return
            elif value in map(lambda e: e.get().strip() if e != entry else "", self.player_entries.keys()): # Checks if value is in entered IDs
                messagebox.showerror("Error", "Invalid submission. Player ID currently in use")
                entry.delete(0, tk.END)
                return
            value = int(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid submission. Enter an integer ID")
            entry.delete(0, tk.END)
            return

        # Fetch players in database, and store them in-memory
        players = sql.fetch_players()
        existing_players = {data[0]: data[1] for data in players} # Keys: playerIDs, Values: Codenames

        if value in existing_players.keys():
            # Check if player ID exists; if so, get the codename. Assumes unique IDs.
            try:
                codename = existing_players[value]
                messagebox.showinfo("Info", f"Player ID {value} with codename '{codename}' found")
                self.player_entries[entry].config(text=codename)
            except Exception as e:
                print("Error fetching codename: ", e)
        else:
            # In this case, player ID does not exist, so create new codename and database entry.
            try:
                while True:
                    new_codename = simpledialog.askstring("Input", "Enter new codename").strip()
                    if new_codename and new_codename not in existing_players.values():
                        sql.create_player(player_id=value, codename=new_codename)
                        messagebox.showinfo("Info", f"Player ID {value} assigned to '{new_codename}'")
                        self.player_entries[entry].config(text=new_codename)
                        break
                    else:
                        messagebox.showerror("Error", "Invalid or duplicate codename")
            except Exception as e:
                print("Error creating new player entry: ", e)
        sql.fetch_players()

window = tk.Tk()
gui = firstScreen(window)
window.mainloop()
