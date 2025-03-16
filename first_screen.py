import tkinter as tk
from tkinter import messagebox, simpledialog
import sql
from udp import udp_sender
from udp import IP
import countdown

class firstScreen:
    def __init__(self, window):
        window.title("Entry Terminal")
        window.geometry("800x700")
        window.configure(bg="black")
        self.player_entries = {}  #  Key-value dictionary with key=PlayerID_entry and value=name_label
        self.equipment_entries = []  # List holding EquipmentID Tkinter entries
        self.assigned_players = {} # Dictionary to track assigned players

        title = tk.Label(window, text="Edit Game", bg="blue", fg="white", font=("Arial", 27, "bold"))
        title.pack()

        main_frame = tk.Frame(window, bg="gray")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=200, pady=40)
        main_frame.bind("<Button-1>", lambda event: window.focus_set())

        red_frame = tk.Frame(main_frame, bg="red", width=500, height=900)
        red_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.make_rows(red_frame, "red", 15)

        green_frame = tk.Frame(main_frame, bg="green", width=500, height=900)
        green_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.make_rows(green_frame, "green", 15)

        button_frame = tk.Frame(main_frame, bg="gray", width=200, height=300, highlightbackground="black", highlightthickness=4)
        button_frame.pack(pady=5, padx=5)
        button_frame.pack_propagate(False)

        editButton = tk.Button(button_frame, text="F1 Edit Game", bg="black", fg="white", width=100)
        editButton.pack(padx=5, pady=5)
        startButton = tk.Button(button_frame, text="F5 Start Game", bg="black", fg="white", width=100, command=self.start_game)
        startButton.pack(padx=5, pady=5)
        viewButton = tk.Button(button_frame, text="F8 View Game", bg="black", fg="white", width=100)
        viewButton.pack(padx=5, pady=5)
        networkButton = tk.Button(button_frame, text="F11 Change Network", bg="black", fg="white", width=100, command=self.change_network)
        networkButton.pack(padx=5, pady=5)
        clearButton = tk.Button(button_frame, text="F12 Clear Game", bg="black", fg="white", width=100, command=self.clear_game)
        clearButton.pack(padx=5, pady=5)

        #F5 opens action display, F11 changes network, 12 clears game
        window.bind("<F5>", lambda event: self.start_game())
        window.bind("<F11>", lambda event: self.change_network())
        window.bind("<F12>", lambda event: self.clear_game())

    def change_network(self):
        new_network = simpledialog.askstring("Input", "Enter new network")
        IP = new_network
        print("The new network is: ", IP)

    def clear_game(self):
        for entry, (name_label, team) in self.player_entries.items():
            entry.delete(0, tk.END)
            name_label.config(text="")

        for entry in self.equipment_entries:
            entry.delete(0, tk.END)

    def make_headers(self, frame, bg_color):
        row_frame = tk.Frame(frame, bg=bg_color)
        row_frame.pack(fill=tk.X, padx=5, pady=1)
        tk.Label(row_frame, text="  ", bg=bg_color, font=("Helvetica", 20)).pack(side=tk.LEFT, padx=5)
        tk.Label(row_frame, text="Player ID", bg=bg_color, font=("Helvetica", 14, "bold")).pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)
        tk.Label(row_frame, text="Equipment ID", bg=bg_color, font=("Helvetica", 14, "bold")).pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)
        tk.Label(row_frame, text="Name", bg=bg_color, font=("Helvetica", 14, "bold")).pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=5)

    def make_rows(self, frame, bg_color, num_rows):
        # Create rows and headers for each team
        self.make_headers(frame, bg_color)

        team = "red" if bg_color == "red" else "green"  # Assign team based on color

        for row in range(num_rows):
            row_frame = tk.Frame(frame, bg=bg_color)
            row_frame.pack(fill=tk.X, padx=5, pady=1)

            tk.Label(row_frame, text=f"{row+1}", bg=bg_color, font=("Helvetica", 20)).pack(side=tk.LEFT, padx=5)

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

            # Store Player ID entry and team in dictionary
            self.player_entries[player_id_entry] = (name_label, team)

            player_id_entry.bind("<Return>", lambda event, e=player_id_entry, t=team: self.submit_player_id(e, t))
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

    def submit_player_id(self, entry, team):
        # Get entry value. If empty, clear name label and exit function. If in use, also exit.
        value = entry.get().strip()
        try:
            if value == "":
                return
            value = int(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid submission. Enter an integer ID")
            entry.delete(0, tk.END)
            return

        # Fetch players in database, and store them in-memory
        players = sql.fetch_players()
        existing_players = {data[0]: data[1] for data in players}  # {PlayerID: Codename}

        if value in existing_players.keys():
            # Check if player ID exists; if so, get the codename. Assumes unique IDs.
            try:
                codename = existing_players[value]
                messagebox.showinfo("Info", f"Player ID {value} with codename '{codename}' found")
                # Remove from previous team if necessary
                if value in self.assigned_players:
                    prev_team = self.assigned_players[value]
                    if prev_team != team:
                        for entry_widget, (name_label, _) in self.player_entries.items():
                            if name_label.cget("text").startswith(codename):
                                name_label.config(text="")  # Clear from previous team
                                break

                # Assign to the new team
                self.assigned_players[value] = team  # Update stored team
                self.player_entries[entry][0].config(text=f"{codename}")  # Update UI
                # messagebox.showinfo("Info", f"Player {value} assigned to {team}")
            
            except Exception as e:
                print("Error fetching codename: ", e)

        else:
            # In this case, player ID does not exist, so create new codename and database entry.
            try:
                # Create new player
                new_codename = simpledialog.askstring("Input", "Enter new codename")

                if not new_codename:
                    entry.delete(0, tk.END)  # Clear the entry field
                    return
                
                if new_codename in existing_players.values():
                    messagebox.showerror("Error", "Codename already exists. Try again.")
                    return

                # Store new player in database
                sql.create_player(player_id=value, codename=new_codename)
                self.assigned_players[value] = team  # Store assigned team
                self.player_entries[entry][0].config(text=f"{new_codename}")
                # messagebox.showinfo("Info", f"New Player {value} assigned to {team}")

            except Exception as e:
                print("Error creating new player entry: ", e)

        sql.fetch_players()

    def start_game(self):
        players = {}  # Store {PlayerID: {codename, team}}

        for entry, (name_label, team) in self.player_entries.items():
            player_id = entry.get().strip()
            if player_id:
                try:
                    player_id = int(player_id)
                    name_text = name_label.cget("text")  # Get label text
                    if name_text:
                        players[player_id] = {"codename": name_text, "team": team}
                except ValueError:
                    continue  # Ignore invalid entries

        countdown.open_window(players)

def open_window():
    window = tk.Tk()
    firstScreen(window)
    window.mainloop()
