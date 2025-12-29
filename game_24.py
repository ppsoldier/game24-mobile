import tkinter as tk
from tkinter import messagebox
import random
import itertools
import threading
import time
import math
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

class Card24Game:
    def __init__(self, root):
        self.root = root
        self.root.title("24点扑克牌游戏 - 3人对战")
        self.root.geometry("1800x1500")
        self.root.configure(bg="#2E7D32")
        
        self.numbers = []
        self.used_cards = [False, False, False, False]
        self.expression = ""
        self.solution = ""
        
        self.players = ["玩家1", "玩家2", "玩家3"]
        self.scores = [0, 0, 0]
        self.current_player = 0
        
        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):
        title_label = tk.Label(
            self.root, 
            text="24点扑克牌游戏 - 3人对战", 
            font=("Arial", 24, "bold"),
            bg="#2E7D32", 
            fg="white"
        )
        title_label.pack(pady=10)
        
        self.players_frame = tk.Frame(self.root, bg="#2E7D32")
        self.players_frame.pack(pady=10)
        
        self.player_labels = []
        colors = ["#FF5722", "#2196F3", "#9C27B0"]
        for i, player in enumerate(self.players):
            frame = tk.Frame(self.players_frame, bg=colors[i], padx=20, pady=10, relief="raised", bd=2)
            frame.pack(side=tk.LEFT, padx=15)
            
            name_label = tk.Label(
                frame,
                text=player,
                font=("Arial", 14, "bold"),
                bg=colors[i],
                fg="white"
            )
            name_label.pack()
            
            score_label = tk.Label(
                frame,
                text=f"得分: 0",
                font=("Arial", 12),
                bg=colors[i],
                fg="white"
            )
            score_label.pack()
            
            self.player_labels.append((name_label, score_label))
        
        self.current_player_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 16, "bold"),
            bg="#2E7D32",
            fg="#FFC107"
        )
        self.current_player_label.pack(pady=5)
        
        self.cards_frame = tk.Frame(self.root, bg="#2E7D32")
        self.cards_frame.pack(pady=15)
        
        self.card_canvases = []
        for i in range(4):
            canvas = tk.Canvas(
                self.cards_frame, 
                width=120, 
                height=160, 
                bg="white", 
                highlightthickness=2,
                highlightbackground="#1B5E20",
                relief="raised",
                cursor="hand2"
            )
            canvas.grid(row=0, column=i, padx=15)
            canvas.bind("<Button-1>", lambda e, idx=i: self.on_card_click(idx))
            self.card_canvases.append(canvas)
        
        self.expression_frame = tk.Frame(self.root, bg="#2E7D32")
        self.expression_frame.pack(pady=15)
        
        tk.Label(
            self.expression_frame, 
            text="当前表达式:", 
            font=("Arial", 14),
            bg="#2E7D32", 
            fg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        self.expression_label = tk.Label(
            self.expression_frame, 
            text="", 
            font=("Arial", 18, "bold"),
            bg="white", 
            fg="#1B5E20",
            width=30,
            relief="sunken"
        )
        self.expression_label.pack(side=tk.LEFT)
        
        self.operators_frame = tk.Frame(self.root, bg="#2E7D32")
        self.operators_frame.pack(pady=10)
        
        operators = ["+", "-", "*", "/", "(", ")"]
        for op in operators:
            btn = tk.Button(
                self.operators_frame,
                text=op,
                font=("Arial", 16, "bold"),
                width=4,
                height=1,
                bg="#FFC107",
                fg="#1B5E20",
                command=lambda o=op: self.add_operator(o)
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        self.control_frame = tk.Frame(self.root, bg="#2E7D32")
        self.control_frame.pack(pady=10)
        
        tk.Button(
            self.control_frame,
            text="清空",
            font=("Arial", 12),
            width=10,
            bg="#FF5722",
            fg="white",
            command=self.clear_expression
        ).pack(side=tk.LEFT, padx=8)
        
        tk.Button(
            self.control_frame,
            text="验证答案",
            font=("Arial", 12, "bold"),
            width=10,
            bg="#4CAF50",
            fg="white",
            command=self.check_answer
        ).pack(side=tk.LEFT, padx=8)
        
        tk.Button(
            self.control_frame,
            text="提示",
            font=("Arial", 12),
            width=10,
            bg="#2196F3",
            fg="white",
            command=self.show_hint
        ).pack(side=tk.LEFT, padx=8)
        
        tk.Button(
            self.control_frame,
            text="跳过/下一题",
            font=("Arial", 12),
            width=10,
            bg="#9C27B0",
            fg="white",
            command=self.skip_question
        ).pack(side=tk.LEFT, padx=8)
        
        tk.Button(
            self.control_frame,
            text="排行榜",
            font=("Arial", 12),
            width=10,
            bg="#607D8B",
            fg="white",
            command=self.show_leaderboard
        ).pack(side=tk.LEFT, padx=8)
        
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#2E7D32",
            fg="white"
        )
        self.result_label.pack(pady=10)
    
    def update_player_display(self):
        colors = ["#FF5722", "#2196F3", "#9C27B0"]
        for i, (name_label, score_label) in enumerate(self.player_labels):
            if i == self.current_player:
                name_label.config(text=f"★ {self.players[i]} ★")
                name_label.config(font=("Arial", 14, "bold"))
            else:
                name_label.config(text=self.players[i])
                name_label.config(font=("Arial", 12))
            score_label.config(text=f"得分: {self.scores[i]}")
        
        self.current_player_label.config(text=f"当前回合: {self.players[self.current_player]}")
    
    def draw_card(self, canvas, number, used=False):
        canvas.delete("all")
        
        if used:
            bg_color = "#E0E0E0"
            border_color = "#9E9E9E"
        else:
            bg_color = "#FFFEF0"
            border_color = "#D4AF37"
        
        card_names = {1: "A", 11: "J", 12: "Q", 13: "K"}
        display_name = card_names.get(number, str(number))
        
        suit = "♠"
        color = "black"
        
        if number <= 4:
            suit = "♠"
            color = "black"
        elif number <= 8:
            suit = "♥"
            color = "red"
        elif number <= 12:
            suit = "♦"
            color = "red"
        else:
            suit = "♣"
            color = "black"
        
        if not used:
            shadow_offset = 4
            canvas.create_rectangle(
                shadow_offset, shadow_offset, 
                120 + shadow_offset, 160 + shadow_offset,
                fill="#2C2C2C", outline="", width=0
            )
            
            canvas.create_rectangle(
                0, 0, 120, 160,
                fill="#FFFEF0", outline="#D4AF37", width=4
            )
            
            canvas.create_rectangle(
                3, 3, 117, 157,
                fill="", outline="#FFD700", width=2
            )
            
            canvas.create_rectangle(
                6, 6, 114, 154,
                fill="", outline="#B8860B", width=1
            )
            
            canvas.create_rectangle(
                8, 8, 112, 152,
                fill="#FFFEF0", outline="#D4AF37", width=1
            )
            
            canvas.create_rectangle(
                8, 8, 112, 152,
                fill="", outline="#FFF8DC", width=1
            )
            
            canvas.create_line(
                8, 8, 112, 8,
                fill="#FFFAF0", width=2
            )
            canvas.create_line(
                8, 8, 8, 152,
                fill="#FFFAF0", width=2
            )
            
            canvas.create_line(
                8, 152, 112, 152,
                fill="#C0C0C0", width=2
            )
            canvas.create_line(
                112, 8, 112, 152,
                fill="#C0C0C0", width=2
            )
            
            canvas.create_text(
                20, 25,
                text=display_name,
                font=("Times New Roman", 18, "bold"),
                fill=color,
                anchor="nw"
            )
            
            canvas.create_text(
                20, 48,
                text=suit,
                font=("Arial", 16),
                fill=color,
                anchor="nw"
            )
            
            canvas.create_text(
                60, 80,
                text=suit,
                font=("Arial", 40),
                fill=color
            )
            
            canvas.create_text(
                100, 135,
                text=display_name,
                font=("Times New Roman", 18, "bold"),
                fill=color,
                anchor="se"
            )
            
            canvas.create_text(
                100, 112,
                text=suit,
                font=("Arial", 16),
                fill=color,
                anchor="se"
            )
        else:
            canvas.create_rectangle(
                4, 4, 124, 164,
                fill="#757575", outline="", width=0
            )
            
            canvas.create_rectangle(
                0, 0, 120, 160,
                fill="#E0E0E0", outline="#9E9E9E", width=3
            )
            
            canvas.create_rectangle(
                3, 3, 117, 157,
                fill="", outline="#BDBDBD", width=1
            )
            
            canvas.create_text(
                60, 80,
                text="已使用",
                font=("Arial", 14),
                fill="#757575"
            )
    
    def generate_numbers(self):
        while True:
            numbers = [random.randint(1, 13) for _ in range(4)]
            if self.find_solution(numbers):
                return numbers
    
    def find_solution(self, numbers):
        ops = ['+', '-', '*', '/']
        num_perms = list(itertools.permutations(numbers))
        
        for perm in num_perms:
            for op1 in ops:
                for op2 in ops:
                    for op3 in ops:
                        expressions = [
                            f"(({perm[0]}{op1}{perm[1]}){op2}{perm[2]}){op3}{perm[3]}",
                            f"({perm[0]}{op1}({perm[1]}{op2}{perm[2]})){op3}{perm[3]}",
                            f"{perm[0]}{op1}(({perm[1]}{op2}{perm[2]}){op3}{perm[3]})",
                            f"{perm[0]}{op1}({perm[1]}{op2}({perm[2]}{op3}{perm[3]}))",
                            f"({perm[0]}{op1}{perm[1]}){op2}({perm[2]}{op3}{perm[3]})",
                        ]
                        
                        for expr in expressions:
                            try:
                                result = eval(expr)
                                if abs(result - 24) < 1e-6:
                                    return expr
                            except:
                                pass
        return None
    
    def new_game(self):
        self.numbers = self.generate_numbers()
        self.used_cards = [False, False, False, False]
        self.expression = ""
        self.expression_label.config(text="")
        self.result_label.config(text="")
        
        self.solution = self.find_solution(self.numbers)
        
        for i, canvas in enumerate(self.card_canvases):
            self.draw_card(canvas, self.numbers[i], self.used_cards[i])
        
        self.update_player_display()
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % 3
        self.update_player_display()
    
    def on_card_click(self, index):
        if not self.used_cards[index]:
            self.expression += str(self.numbers[index])
            self.used_cards[index] = True
            self.expression_label.config(text=self.expression)
            self.draw_card(self.card_canvases[index], self.numbers[index], True)
    
    def add_operator(self, operator):
        self.expression += operator
        self.expression_label.config(text=self.expression)
    
    def clear_expression(self):
        self.expression = ""
        self.used_cards = [False, False, False, False]
        self.expression_label.config(text="")
        self.result_label.config(text="")
        
        for i, canvas in enumerate(self.card_canvases):
            self.draw_card(canvas, self.numbers[i], self.used_cards[i])
    
    def check_answer(self):
        if not self.expression:
            messagebox.showwarning("提示", "请先输入表达式！")
            return
        
        if not all(self.used_cards):
            messagebox.showwarning("提示", "请使用所有4张牌！")
            return
        
        try:
            result = eval(self.expression)
            if abs(result - 24) < 1e-6:
                self.scores[self.current_player] += 10
                self.result_label.config(text=f"{self.players[self.current_player]}答对了！+10分", fg="#4CAF50")
                self.play_cheer_sound()
                self.create_fireworks()
                messagebox.showinfo("成功", f"恭喜！{self.players[self.current_player]}答对了！\n{self.expression} = 24\n获得10分！")
                self.next_player()
                self.new_game()
            else:
                self.result_label.config(text=f"结果是 {result:.2f}，不是24，请再试一次", fg="#FF5722")
        except:
            self.result_label.config(text="表达式无效，请检查输入", fg="#FF5722")
    
    def show_hint(self):
        if self.solution:
            messagebox.showinfo("提示", f"参考答案: {self.solution} = 24")
        else:
            messagebox.showinfo("提示", "这组数字无解，请换一题")
    
    def skip_question(self):
        self.result_label.config(text=f"{self.players[self.current_player]}跳过本题", fg="#FFC107")
        self.next_player()
        self.new_game()
    
    def show_leaderboard(self):
        sorted_players = sorted(enumerate(self.scores), key=lambda x: x[1], reverse=True)
        leaderboard_text = "=== 排行榜 ===\n\n"
        medals = ["🥇", "🥈", "🥉"]
        
        for rank, (player_idx, score) in enumerate(sorted_players):
            medal = medals[rank] if rank < 3 else f"{rank + 1}."
            leaderboard_text += f"{medal} {self.players[player_idx]}: {score}分\n"
        
        messagebox.showinfo("排行榜", leaderboard_text)
    
    def play_cheer_sound(self):
        if not SOUND_AVAILABLE:
            print("声音功能不可用")
            return
        
        def play_sound():
            try:
                melody = [
                    (523, 100), (659, 100), (784, 100), (1047, 200),
                    (784, 100), (1047, 100), (1319, 200)
                ]
                for freq, duration in melody:
                    winsound.Beep(freq, duration)
            except Exception as e:
                print(f"播放声音失败: {e}")
        
        thread = threading.Thread(target=play_sound)
        thread.daemon = True
        thread.start()
    
    def create_fireworks(self):
        def animate_firework():
            canvas = tk.Canvas(
                self.root,
                width=900,
                height=700,
                bg="#2E7D32",
                highlightthickness=0
            )
            canvas.place(x=0, y=0)
            
            fireworks = []
            for _ in range(8):
                x = random.randint(100, 800)
                y = random.randint(100, 500)
                color = random.choice(["#FF0000", "#FFD700", "#00FF00", "#FF00FF", "#00FFFF", "#FFA500"])
                particles = []
                for _ in range(30):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 6)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    particles.append({
                        'x': x,
                        'y': y,
                        'vx': vx,
                        'vy': vy,
                        'color': color,
                        'life': random.randint(20, 40)
                    })
                fireworks.append(particles)
            
            for frame in range(50):
                canvas.delete("all")
                
                for particles in fireworks:
                    for p in particles:
                        if p['life'] > 0:
                            p['x'] += p['vx']
                            p['y'] += p['vy']
                            p['vy'] += 0.1
                            p['life'] -= 1
                            
                            size = max(1, p['life'] // 5)
                            canvas.create_oval(
                                p['x'] - size, p['y'] - size,
                                p['x'] + size, p['y'] + size,
                                fill=p['color'], outline=""
                            )
                
                canvas.update()
                time.sleep(0.03)
            
            canvas.destroy()
        
        thread = threading.Thread(target=animate_firework)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    game = Card24Game(root)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 800
    window_height = 620
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
