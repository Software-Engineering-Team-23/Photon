import tkinter as tk
from tkinter import Frame, Label, Text
import udp
import playsound

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
        self.team_scores = {"red": 0, "green": 0}
        self.cached_rankings = []

        Label(self.window, text="Current Scores", fg="cyan", bg="black", font=("Arial", 16, "bold")).pack(side=tk.TOP, pady=(10, 2), anchor="n")

        self.setup_ui()

        # Start 6-minute gameplay timer
        self.setup_timer()

        # Iterating over the dictionary to add players
        if players:
            self.players = players
            for player_id, data in players.items():
                self.add_player(data["team"], data["codename"], data["score"])

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

        #Adding colors each team member in event log
        self.log_text.tag_config("RedPlayer", foreground="red")
        self.log_text.tag_config("GreenPlayer", foreground="green")
        self.log_text.tag_config("Normal", foreground="white")

    def flash_teamscore(self):
        # Flash team score with highest value
        if self.team_scores["green"] > self.team_scores["red"]:
            current_color = self.green_total_score.cget("fg")
            self.green_total_score.config(fg=("black" if current_color == "yellow" else "yellow"))
            self.red_total_score.config(fg="yellow")
        elif self.team_scores["red"] > self.team_scores["green"]:   
            current_color = self.red_total_score.cget("fg")
            self.red_total_score.config(fg=("black" if current_color == "yellow" else "yellow"))
            self.green_total_score.config(fg="yellow")
        else:
            self.green_total_score.config(fg="yellow")
            self.red_total_score.config(fg="yellow")

        # Keep looping indefinitely until game ends
        if self.remaining_seconds >= 0:
            self.window.after(500, self.flash_teamscore)

    def setup_timer(self):
        self.remaining_seconds = 360  # 6 minutes
        self.timer_label = Label(self.window, text="", fg="white", bg="black", font=("Arial", 18, "bold"))
        self.timer_label.pack(side=tk.TOP, pady=5)
        self.flash_teamscore()
        self.update_timer()
 
    def update_timer(self):
        if self.remaining_seconds >= 0:
            mins = self.remaining_seconds // 60
            secs = self.remaining_seconds % 60
            self.timer_label.config(text=f"Game Time Remaining: {mins:02}:{secs:02}")
            self.remaining_seconds -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.end_game()
 
    def end_game(self):
        def ignore_tags(*args, **kwargs):
            pass
        udp.set_tagged_callback(ignore_tags)

        # Result panel
        result_panel = Frame(self.window, bg="black", bd=4, relief="ridge", highlightbackground="white", highlightthickness=2)
        result_panel.place(relx=0.5, rely=0.5, anchor="center")

        # Game over label
        game_over_label = Label(result_panel, text="GAME OVER", fg="red", bg="black", font=("Arial", 48, "bold"))
        game_over_label.pack(pady=(10, 2))

        # Winner decision
        red_score = self.team_scores["red"]
        green_score = self.team_scores["green"]
        if red_score > green_score:
            winner_text = "RED TEAM WINS!"
            winner_color = "red"
        elif green_score > red_score:
            winner_text = "GREEN TEAM WINS!"
            winner_color = "green"
        else:
            winner_text = "IT'S A TIE!"
            winner_color = "white"

        #winner label 
        winner_label = Label(result_panel, text=winner_text, fg=winner_color, bg="black", font=("Arial", 20, "bold"))
        winner_label.pack(pady=(0, 5))

        self.display_back_button(result_panel)

        for i in range(3):
            # Send code 221 three times to signal game end
            udp.udp_sender(221)
    
    def display_back_button(self, container):
        import first_screen # import is local to avoid any possible conflict
        def go_back():
            self.window.destroy()
            # Save player data to reutilize
            saved_players = {
                player_id: {
                            "codename": data["codename"],
                            "team": data["team"],
                            "equipment_id": player_id,
                            "player_id": data.get("player_id", player_id)
                        }
            for player_id, data in self.players.items()
            }
            first_screen.open_window(preload_players=saved_players)# Added to get back to the first screen
        
        back_button = tk.Button(container, text="BACK", fg="cyan", bg="black", font=("Arial", 16, "bold"), command=go_back)
        back_button.pack(pady=(10, 5))

        back_button.bind("<Enter>", lambda e: back_button.config(fg="#cc33ff"))
        back_button.bind("<Leave>", lambda e: back_button.config(fg="cyan"))
            
    def add_player(self, team, name, score=0):
        frame = self.red_frame if team.lower() == "red" else self.green_frame

        player_row = Frame(frame, bg="black")
        player_row.pack(fill=tk.X, padx=5, pady=2)

        name_label = Label(player_row, text=name, fg="white", bg="black", font=("Arial", 15), anchor="w")
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        score_label = Label(player_row, text=str(score), fg="yellow", bg="black", font=("Arial", 15, "bold"), anchor="e")
        score_label.pack(side=tk.RIGHT, padx=10)

        if team.lower() == "red":
            self.red_players[name] = {"name": name_label, "score": score_label, "row": player_row}
        else:
            self.green_players[name] = {"name": name_label, "score": score_label, "row": player_row}

    def log_event(self, message, tagger_name=None, tagger_team=None, tagged_name=None, tagged_team=None):
        def safe_insert():
            self.log_text.insert(tk.END, "\n")

            if all([tagger_name, tagger_team, tagged_name, tagged_team]):
                self.log_text.insert(tk.END, f"{tagger_name}", "RedPlayer" if tagger_team.lower() == "red" else "GreenPlayer")
                self.log_text.insert(tk.END, " tagged ", "Normal")
                self.log_text.insert(tk.END, f"{tagged_name}", "RedPlayer" if tagged_team.lower() == "red" else "GreenPlayer")
            else:
                self.log_text.insert(tk.END, message, "Normal")

            self.log_text.see(tk.END)

        self.log_text.after(0, safe_insert)

    def update_scoreboard(self, tagger_team):
        # Updates scoreboard display for player
        sorted_players = sorted(self.players.items(), key=lambda x: x[1]["score"], reverse=True)
        current_rankings = [tup[0] for tup in sorted_players]

        # Update cumulative team scores
        if tagger_team.lower() == "red":
            self.red_total_score.config(text=self.team_scores["red"])
        else:
            self.green_total_score.config(text=self.team_scores["green"])
        
        # Update and sort individual player scores as needed
        for _, player_info in sorted_players:
            sorted_teamname = player_info["team"].lower()
            sorted_codename = player_info["codename"]
            sorted_score = player_info["score"]
            if sorted_teamname == "red":
                name_label = self.red_players[sorted_codename]["name"]
                score_label = self.red_players[sorted_codename]["score"]
                name_label.config(text=sorted_codename)
                score_label.config(text=sorted_score)
                row = self.red_players[sorted_codename]["row"]      
            else:
                name_label = self.green_players[sorted_codename]["name"]
                score_label = self.green_players[sorted_codename]["score"]
                name_label.config(text=sorted_codename)
                score_label.config(text=sorted_score)
                row = self.green_players[sorted_codename]["row"]

            row.pack_forget()
            row.pack(in_=self.red_frame if sorted_teamname == "red" else self.green_frame, fill=tk.X, padx=5, pady=2)
        
        # Save the rankings of player IDs
        self.cached_rankings = current_rankings
        
    def handle_tagged(self, tagger_id, tagged_id):
        try:
            tagger_id = int(tagger_id)
            tagged_id = int(tagged_id)

            tagger_info = self.players.get(tagger_id)
            tagged_info = self.players.get(tagged_id)

            if tagger_info and tagged_info:
                print(f"Handled tag: {tagger_info['codename']} tagged {tagged_info['codename']}") #Print the tag info into the console

            if tagged_id == 53:
                if tagger_info["team"].lower() == "green":
                    tagger_name = tagger_info["codename"]
                    self.players.get(tagger_id)["score"] += 100
                    self.team_scores["green"] += 100
                    self.update_scoreboard("green")
                    self.log_event(
                        message=None,
                        tagger_name=tagger_name,
                        tagger_team="green",
                        tagged_name="Red Base",
                        tagged_team="red"
                    )
                    self.blink_player_label(tagger_name, "green")
                    return
                
            if tagged_id == 43:
                if tagger_info["team"].lower() == "red":
                    tagger_name = tagger_info["codename"]
                    self.players.get(tagger_id)["score"] += 100
                    self.team_scores["red"] += 100
                    self.update_scoreboard("red")
                    self.log_event(
                        message=None,
                        tagger_name=tagger_name,
                        tagger_team="red",
                        tagged_name="Green Base",
                        tagged_team="green"
                    )
                    self.blink_player_label(tagger_name, "red")
                    return

            if not tagger_info or not tagged_info:
                self.log_event(f"Unknown tag event: {tagger_id} → {tagged_id}")
                return

            tagger_name = tagger_info["codename"]
            tagged_name = tagged_info["codename"]

            tagger_team = tagger_info["team"].capitalize()
            tagged_team = tagged_info["team"].capitalize()

            if tagger_team != tagged_team:
                # Add points for hitting enemy
                self.players.get(tagger_id)["score"] += 10
                self.team_scores[tagger_team.lower()] += 10
            else:
                # Deduct points for friendly-fire
                self.players.get(tagger_id)["score"] -= 10
                self.team_scores[tagger_team.lower()] -= 10

            self.update_scoreboard(tagger_team)    

            #Log with colored player names
            self.log_event(
                message="", 
                tagger_name=tagger_name,
                tagger_team=tagger_team,
                tagged_name=tagged_name,
                tagged_team=tagged_team
            )

        except Exception as e:
            self.log_event(f"Error processing hit: {e}")

    #Element to score base (B)
    def blink_player_label(self, player_name, team_color, interval=500):
        duration = self.remaining_seconds * 1000
        team_dict = self.green_players if team_color.lower() == "green" else self.red_players
        label_entry = team_dict.get(player_name)
        if not label_entry:
            return

        name_label = label_entry["name"]
        original_text = name_label.cget("text")
        player_row = name_label.master

        #Remove the original name label
        name_label.pack_forget()

        #Frame aspects for B
        blink_frame = Frame(player_row, bg="black")
        blink_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        b_label = Label(blink_frame, text="B", fg="#cc33ff", font=("Courier New", 15, "bold"), bg="black")
        name_label_new = Label(blink_frame, text=original_text, fg="white", font=("Arial", 15), bg="black")

        b_label.pack(side=tk.LEFT, padx=(0, 5))
        name_label_new.pack(side=tk.LEFT)

        def toggle_color(count):
            if count <= 0:
                blink_frame.destroy()
                name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
                return
            current = b_label.cget("fg")
            b_label.config(fg="#cc33ff" if current == "cyan" else "cyan")
            self.window.after(interval, toggle_color, count - 1)

        blink_count = duration // interval
        toggle_color(blink_count)  
            
def open_window(players=None):
    window = tk.Tk()
    display = actionDisplay(window, players)
    playsound.random_music()
    #Set the UDP callback to the action display's method
    udp.set_tagged_callback(display.handle_tagged)    
    window.mainloop()
