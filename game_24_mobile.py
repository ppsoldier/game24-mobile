from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.widget import Widget
import random
import itertools
import math
import threading
import time

try:
    from kivy.core.audio import SoundLoader
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

class CardWidget(Widget):
    number = NumericProperty(0)
    used = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 140)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        
        if self.used:
            self.draw_used_card()
        else:
            self.draw_card()
    
    def draw_card(self):
        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=(self.x + 4, self.y + 4), size=self.size)
            
            Color(1, 1, 0.94, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            Color(0.83, 0.69, 0.22, 1)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=3)
            
            Color(1, 0.84, 0, 1)
            Line(rectangle=(self.x + 3, self.y + 3, self.width - 6, self.height - 6), width=2)
            
            Color(0.72, 0.53, 0.04, 1)
            Line(rectangle=(self.x + 6, self.y + 6, self.width - 12, self.height - 12), width=1)
            
            Color(1, 0.98, 0.86, 1)
            Rectangle(pos=(self.x + 8, self.y + 8), size=(self.width - 16, self.height - 16))
            
            Color(1, 0.98, 0.94, 1)
            Line(points=[self.x + 8, self.y + 8, self.x + self.width - 8, self.y + 8], width=2)
            Line(points=[self.x + 8, self.y + 8, self.x + 8, self.y + self.height - 8], width=2)
            
            Color(0.75, 0.75, 0.75, 1)
            Line(points=[self.x + 8, self.y + self.height - 8, self.x + self.width - 8, self.y + self.height - 8], width=2)
            Line(points=[self.x + self.width - 8, self.y + 8, self.x + self.width - 8, self.y + self.height - 8], width=2)
            
            card_names = {1: "A", 11: "J", 12: "Q", 13: "K"}
            display_name = card_names.get(self.number, str(self.number))
            
            if self.number <= 4:
                suit = "♠"
                color = (0, 0, 0, 1)
            elif self.number <= 8:
                suit = "♥"
                color = (1, 0, 0, 1)
            elif self.number <= 12:
                suit = "♦"
                color = (1, 0, 0, 1)
            else:
                suit = "♣"
                color = (0, 0, 0, 1)
            
            Color(*color)
            
            from kivy.core.text import Label as CoreLabel
            label = CoreLabel(text=display_name, font_size=20, font_name='Roboto', color=color)
            label.refresh()
            texture = label.texture
            self.canvas.add(Rectangle(texture=texture, pos=(self.x + 15, self.y + self.height - 35), size=texture.size))
            
            label_suit = CoreLabel(text=suit, font_size=18, font_name='Roboto', color=color)
            label_suit.refresh()
            texture_suit = label_suit.texture
            self.canvas.add(Rectangle(texture=texture_suit, pos=(self.x + 15, self.y + self.height - 55), size=texture_suit.size))
            
            label_big = CoreLabel(text=suit, font_size=45, font_name='Roboto', color=color)
            label_big.refresh()
            texture_big = label_big.texture
            self.canvas.add(Rectangle(texture=texture_big, pos=(self.center_x - texture_big.size[0]/2, self.center_y - texture_big.size[1]/2), size=texture_big.size))
            
            label_bottom = CoreLabel(text=display_name, font_size=20, font_name='Roboto', color=color)
            label_bottom.refresh()
            texture_bottom = label_bottom.texture
            self.canvas.add(Rectangle(texture=texture_bottom, pos=(self.x + self.width - 35, self.y + 20), size=texture_bottom.size))
            
            label_suit_bottom = CoreLabel(text=suit, font_size=18, font_name='Roboto', color=color)
            label_suit_bottom.refresh()
            texture_suit_bottom = label_suit_bottom.texture
            self.canvas.add(Rectangle(texture=texture_suit_bottom, pos=(self.x + self.width - 35, self.y + 40), size=texture_suit_bottom.size))
    
    def draw_used_card(self):
        with self.canvas:
            Color(0.46, 0.46, 0.46, 1)
            Rectangle(pos=(self.x + 4, self.y + 4), size=self.size)
            
            Color(0.88, 0.88, 0.88, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            Color(0.62, 0.62, 0.62, 1)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=3)
            
            Color(0.74, 0.74, 0.74, 1)
            Line(rectangle=(self.x + 3, self.y + 3, self.width - 6, self.height - 6), width=1)
            
            Color(0.46, 0.46, 0.46, 1)
            label = CoreLabel(text="已使用", font_size=16, font_name='Roboto', color=(0.46, 0.46, 0.46, 1))
            label.refresh()
            texture = label.texture
            self.canvas.add(Rectangle(texture=texture, pos=(self.center_x - texture.size[0]/2, self.center_y - texture.size[1]/2), size=texture.size))
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.used:
            if hasattr(self.parent, 'on_card_click'):
                index = self.parent.cards.index(self)
                self.parent.on_card_click(index)
        return super().on_touch_down(touch)

class FireworkParticle(Widget):
    def __init__(self, x, y, color, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x, y)
        self.size = (6, 6)
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(20, 40)
        self.max_life = self.life
        
        with self.canvas:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1
        
        if self.life > 0:
            size = max(1, self.life // 5)
            self.size = (size, size)
            self.rect.pos = self.pos
            self.rect.size = self.size
            return True
        return False

class FireworkWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.active = False
    
    def start_fireworks(self):
        self.active = True
        self.particles = []
        
        for _ in range(8):
            x = random.randint(50, Window.width - 50)
            y = random.randint(50, Window.height - 50)
            color = random.choice([
                (1, 0, 0, 1),
                (1, 0.84, 0, 1),
                (0, 1, 0, 1),
                (1, 0, 1, 1),
                (0, 1, 1, 1),
                (1, 0.65, 0, 1)
            ])
            
            for _ in range(30):
                particle = FireworkParticle(x, y, color)
                self.add_widget(particle)
                self.particles.append(particle)
        
        Clock.schedule_interval(self.update_fireworks, 0.03)
    
    def update_fireworks(self, dt):
        if not self.active:
            return False
        
        alive = False
        for particle in self.particles:
            if particle.update():
                alive = True
            else:
                self.remove_widget(particle)
        
        if not alive:
            self.active = False
            return False
        
        return True

class Game24App(App):
    numbers = ListProperty([])
    used_cards = ListProperty([False, False, False, False])
    expression = StringProperty("")
    solution = StringProperty("")
    players = ListProperty(["玩家1", "玩家2", "玩家3"])
    scores = ListProperty([0, 0, 0])
    current_player = NumericProperty(0)
    
    def build(self):
        Window.size = (400, 700)
        Window.clearcolor = (0.18, 0.49, 0.2, 1)
        
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title_label = Label(
            text='24点扑克牌游戏',
            font_size=24,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50
        )
        self.main_layout.add_widget(title_label)
        
        self.players_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=5)
        self.player_labels = []
        colors = [(1, 0.34, 0.13, 1), (0.13, 0.59, 0.95, 1), (0.61, 0.15, 0.69, 1)]
        
        for i, player in enumerate(self.players):
            player_box = BoxLayout(orientation='vertical', size_hint_x=1, padding=5)
            player_box.canvas.before.add(Color(*colors[i]))
            player_box.canvas.before.add(Rectangle(pos=player_box.pos, size=player_box.size))
            
            name_label = Label(
                text=player,
                font_size=14,
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=30
            )
            score_label = Label(
                text=f'得分: 0',
                font_size=12,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=30
            )
            
            player_box.add_widget(name_label)
            player_box.add_widget(score_label)
            self.players_layout.add_widget(player_box)
            self.player_labels.append((name_label, score_label))
        
        self.main_layout.add_widget(self.players_layout)
        
        self.current_player_label = Label(
            text='',
            font_size=16,
            bold=True,
            color=(1, 0.76, 0.03, 1),
            size_hint_y=None,
            height=30
        )
        self.main_layout.add_widget(self.current_player_label)
        
        self.cards_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, spacing=10)
        self.cards = []
        for i in range(4):
            card = CardWidget()
            self.cards_layout.add_widget(card)
            self.cards.append(card)
        self.main_layout.add_widget(self.cards_layout)
        
        expression_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        Label(
            text='当前表达式:',
            font_size=14,
            color=(1, 1, 1, 1),
            size_hint_x=0.4
        ).__self__
        expression_layout.add_widget(Label(text='当前表达式:', font_size=14, color=(1, 1, 1, 1), size_hint_x=0.4))
        
        self.expression_label = Label(
            text='',
            font_size=18,
            bold=True,
            color=(0.1, 0.37, 0.13, 1),
            size_hint_x=0.6
        )
        with self.expression_label.canvas.before:
            Color(1, 1, 1, 1)
            self.expression_label.bg_rect = Rectangle(pos=self.expression_label.pos, size=self.expression_label.size)
        self.expression_label.bind(pos=self.update_expression_bg, size=self.update_expression_bg)
        expression_layout.add_widget(self.expression_label)
        self.main_layout.add_widget(expression_layout)
        
        operators_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        operators = ['+', '-', '*', '/', '(', ')']
        for op in operators:
            btn = Button(
                text=op,
                font_size=20,
                bold=True,
                background_color=(1, 0.76, 0.03, 1),
                color=(0.1, 0.37, 0.13, 1)
            )
            btn.bind(on_press=lambda instance, o=op: self.add_operator(o))
            operators_layout.add_widget(btn)
        self.main_layout.add_widget(operators_layout)
        
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        
        clear_btn = Button(
            text='清空',
            font_size=14,
            background_color=(1, 0.34, 0.13, 1),
            color=(1, 1, 1, 1)
        )
        clear_btn.bind(on_press=self.clear_expression)
        control_layout.add_widget(clear_btn)
        
        check_btn = Button(
            text='验证',
            font_size=14,
            bold=True,
            background_color=(0.29, 0.69, 0.31, 1),
            color=(1, 1, 1, 1)
        )
        check_btn.bind(on_press=self.check_answer)
        control_layout.add_widget(check_btn)
        
        hint_btn = Button(
            text='提示',
            font_size=14,
            background_color=(0.13, 0.59, 0.95, 1),
            color=(1, 1, 1, 1)
        )
        hint_btn.bind(on_press=self.show_hint)
        control_layout.add_widget(hint_btn)
        
        skip_btn = Button(
            text='跳过',
            font_size=14,
            background_color=(0.61, 0.15, 0.69, 1),
            color=(1, 1, 1, 1)
        )
        skip_btn.bind(on_press=self.skip_question)
        control_layout.add_widget(skip_btn)
        
        leaderboard_btn = Button(
            text='排行',
            font_size=14,
            background_color=(0.38, 0.49, 0.55, 1),
            color=(1, 1, 1, 1)
        )
        leaderboard_btn.bind(on_press=self.show_leaderboard)
        control_layout.add_widget(leaderboard_btn)
        
        self.main_layout.add_widget(control_layout)
        
        self.result_label = Label(
            text='',
            font_size=14,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40
        )
        self.main_layout.add_widget(self.result_label)
        
        self.firework_widget = FireworkWidget()
        self.main_layout.add_widget(self.firework_widget)
        
        self.new_game()
        
        return self.main_layout
    
    def update_expression_bg(self, instance, value):
        self.expression_label.bg_rect.pos = instance.pos
        self.expression_label.bg_rect.size = instance.size
    
    def update_player_display(self):
        colors = [(1, 0.34, 0.13, 1), (0.13, 0.59, 0.95, 1), (0.61, 0.15, 0.69, 1)]
        for i, (name_label, score_label) in enumerate(self.player_labels):
            if i == self.current_player:
                name_label.text = f"★ {self.players[i]} ★"
                name_label.font_size = 16
            else:
                name_label.text = self.players[i]
                name_label.font_size = 14
            score_label.text = f"得分: {self.scores[i]}"
        
        self.current_player_label.text = f"当前回合: {self.players[self.current_player]}"
    
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
        self.expression_label.text = ""
        self.result_label.text = ""
        
        self.solution = self.find_solution(self.numbers)
        
        for i, card in enumerate(self.cards):
            card.number = self.numbers[i]
            card.used = self.used_cards[i]
            card.update_canvas()
        
        self.update_player_display()
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % 3
        self.update_player_display()
    
    def on_card_click(self, index):
        if not self.used_cards[index]:
            self.expression += str(self.numbers[index])
            self.used_cards[index] = True
            self.expression_label.text = self.expression
            self.cards[index].used = True
            self.cards[index].update_canvas()
    
    def add_operator(self, operator):
        self.expression += operator
        self.expression_label.text = self.expression
    
    def clear_expression(self):
        self.expression = ""
        self.used_cards = [False, False, False, False]
        self.expression_label.text = ""
        self.result_label.text = ""
        
        for i, card in enumerate(self.cards):
            card.used = self.used_cards[i]
            card.update_canvas()
    
    def check_answer(self, instance):
        if not self.expression:
            self.show_popup("提示", "请先输入表达式！")
            return
        
        if not all(self.used_cards):
            self.show_popup("提示", "请使用所有4张牌！")
            return
        
        try:
            result = eval(self.expression)
            if abs(result - 24) < 1e-6:
                self.scores[self.current_player] += 10
                self.result_label.text = f"{self.players[self.current_player]}答对了！+10分"
                self.result_label.color = (0.29, 0.69, 0.31, 1)
                self.play_cheer_sound()
                self.firework_widget.start_fireworks()
                self.show_popup("成功", f"恭喜！{self.players[self.current_player]}答对了！\n{self.expression} = 24\n获得10分！")
                self.next_player()
                self.new_game()
            else:
                self.result_label.text = f"结果是 {result:.2f}，不是24，请再试一次"
                self.result_label.color = (1, 0.34, 0.13, 1)
        except:
            self.result_label.text = "表达式无效，请检查输入"
            self.result_label.color = (1, 0.34, 0.13, 1)
    
    def show_hint(self, instance):
        if self.solution:
            self.show_popup("提示", f"参考答案: {self.solution} = 24")
        else:
            self.show_popup("提示", "这组数字无解，请换一题")
    
    def skip_question(self, instance):
        self.result_label.text = f"{self.players[self.current_player]}跳过本题"
        self.result_label.color = (1, 0.76, 0.03, 1)
        self.next_player()
        self.new_game()
    
    def show_leaderboard(self, instance):
        sorted_players = sorted(enumerate(self.scores), key=lambda x: x[1], reverse=True)
        leaderboard_text = "=== 排行榜 ===\n\n"
        medals = ["🥇", "🥈", "🥉"]
        
        for rank, (player_idx, score) in enumerate(sorted_players):
            medal = medals[rank] if rank < 3 else f"{rank + 1}."
            leaderboard_text += f"{medal} {self.players[player_idx]}: {score}分\n"
        
        self.show_popup("排行榜", leaderboard_text)
    
    def show_popup(self, title, content):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content_label = Label(
            text=content,
            font_size=16,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=200,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        content_label.bind(texture_size=content_label.setter('size'))
        
        close_btn = Button(
            text='关闭',
            font_size=16,
            size_hint_y=None,
            height=50,
            background_color=(0.13, 0.59, 0.95, 1),
            color=(1, 1, 1, 1)
        )
        
        popup_layout.add_widget(content_label)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.5),
            title_align='center'
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def play_cheer_sound(self):
        if not SOUND_AVAILABLE:
            print("声音功能不可用")
            return
        
        try:
            from kivy.core.audio import SoundLoader
            import os
            
            sound = SoundLoader.load('cheer.mp3')
            if sound:
                sound.play()
            else:
                print("声音文件未找到")
        except Exception as e:
            print(f"播放声音失败: {e}")

if __name__ == '__main__':
    Game24App().run()
