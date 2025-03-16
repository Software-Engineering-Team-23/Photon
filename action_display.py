import tkinter as tk
from tkinter import Frame, Label, Text

class actionDisplay:
    def __init__(self, window, players=None):
        self.window = window
        self.window.geometry((f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0"))
        #self.window.state("zoomed") Commented out due to Debian incompatibility
        self.window.title("Game Display")
        self.window.configure(bg="black")
        self.window.minsize(600, 500)

        # Player storage
        self.red_players = {}
        self.green_players = {}
        self.red_score = 0
        self.green_score = 0

        Label(self.window, text="Current Scores", fg="cyan", bg="black", font=("Arial", 16, "bold")).pack(side=tk.TOP, pady=(10, 2), anchor="n")

        self.setup_ui()

        # Iterating over the dictionary to add players
        if players:
            for player_id, data in players.items():
                self.add_player(data["team"], data["codename"], 0)

    def setup_ui(self):
        # Team Scores Elements
        self.team_frame = Frame(self.window, bg="black")
        self.team_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, expand=True)

        # Red Team display
        self.red_team = Frame(self.team_frame, bg="black", bd=2, relief="solid", highlightbackground="red",
                              highlightcolor="red", highlightthickness=2)
        self.red_team.pack_propagate(False)
        self.red_team.configure(height=300)
        self.red_team.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        Label(self.red_team, text="RED TEAM", fg="red", bg="black", font=("Arial", 16, "bold")).pack()
        self.red_frame = Frame(self.red_team, bg="black")
        self.red_frame.pack(fill=tk.BOTH, expand=True)
        self.red_frame.pack_propagate(False)

        self.red_bottom_frame = Frame(self.red_team, bg="black")
        self.red_bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Green Team display
        self.green_team = Frame(self.team_frame, bg="black", bd=2, relief="solid", highlightbackground="green",
                                highlightcolor="green", highlightthickness=2)
        self.green_team.pack_propagate(False)
        self.green_team.configure(height=300)
        self.green_team.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        Label(self.green_team, text="GREEN TEAM", fg="green", bg="black", font=("Arial", 16, "bold")).pack()
        self.green_frame = Frame(self.green_team, bg="black")
        self.green_frame.pack(fill=tk.BOTH, expand=True)
        self.green_frame.pack_propagate(False)

        self.green_bottom_frame = Frame(self.green_team, bg="black")
        self.green_bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Total scores
        self.red_total_score = Label(self.red_bottom_frame, text="0", fg="yellow", bg="black",
                                     font=("Arial", 16, "bold"), anchor="e")
        self.red_total_score.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.green_total_score = Label(self.green_bottom_frame, text="0", fg="yellow", bg="black",
                                       font=("Arial", 16, "bold"), anchor="e")
        self.green_total_score.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Even log (White frame)
        self.log_frame = Frame(self.window, bg="black")
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=5, expand=True)

        self.log_frame_property = Frame(self.log_frame, bg="black",
                                        highlightbackground="white", highlightcolor="white",
                                        highlightthickness=2, bd=2, relief="solid")
        self.log_frame_property.pack_propagate(False)
        self.log_frame_property.configure(height=150)
        self.log_frame_property.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        Label(self.log_frame_property, text="Current Game Action", fg="cyan", bg="black", font=("Arial", 16, "bold")).pack(
            side=tk.TOP, pady=2)

        self.log_text = Text(self.log_frame_property, height=8, width=50, bg="black", fg="white",
                             font=("Arial", 12, "italic"), bd=3, relief="solid")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
    def add_player(self, team, name, score=0):
        frame = self.red_frame if team.lower() == "red" else self.green_frame

        player_row = Frame(frame, bg="black")
        player_row.pack(fill=tk.X, padx=5, pady=2)

        name_label = Label(player_row, text=name, fg="white", bg="black", font=("Arial", 15), anchor="w")
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        score_label = Label(player_row, text=str(score), fg="yellow", bg="black", font=("Arial", 15, "bold"), anchor="e")
        score_label.pack(side=tk.RIGHT, padx=10)

        if team.lower() == "red":
            self.red_players[name] = score_label
        else:
            self.green_players[name] = score_label


def open_window(players=None):
    window = tk.Tk()
    display = actionDisplay(window, players)
    window.mainloop()
