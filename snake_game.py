from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.core.audio import SoundLoader
import random

class SnakeSegment(Widget):
    pass

class Food(Widget):
    pass

class SnakeGame(Widget):
    snake_segments = ListProperty([])
    food = ObjectProperty(None)
    score = NumericProperty(0)
    game_over = False
    grid_size = 20
    snake_speed = 0.15
    
    direction_x = NumericProperty(1)
    direction_y = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake_segments = []
        self.food = Food()
        self.add_widget(self.food)
        self.reset_game()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_interval(self.update, self.snake_speed)
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.game_over:
            if keycode[1] == 'r' or keycode[1] == 'enter':
                self.reset_game()
            return True
        
        if keycode[1] == 'up' and self.direction_y == 0:
            self.direction_x = 0
            self.direction_y = 1
        elif keycode[1] == 'down' and self.direction_y == 0:
            self.direction_x = 0
            self.direction_y = -1
        elif keycode[1] == 'left' and self.direction_x == 0:
            self.direction_x = -1
            self.direction_y = 0
        elif keycode[1] == 'right' and self.direction_x == 0:
            self.direction_x = 1
            self.direction_y = 0
        return True
    
    def on_touch_down(self, touch):
        if self.game_over:
            self.reset_game()
            return True
        
        width = self.width
        height = self.height
        
        if touch.x < width / 3 and self.direction_x == 0:
            self.direction_x = -1
            self.direction_y = 0
        elif touch.x > width * 2 / 3 and self.direction_x == 0:
            self.direction_x = 1
            self.direction_y = 0
        elif touch.y < height / 3 and self.direction_y == 0:
            self.direction_x = 0
            self.direction_y = -1
        elif touch.y > height * 2 / 3 and self.direction_y == 0:
            self.direction_x = 0
            self.direction_y = 1
        return True
    
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.direction_x = 1
        self.direction_y = 0
        
        for segment in self.snake_segments:
            self.remove_widget(segment)
        self.snake_segments = []
        
        start_x = self.width / 2
        start_y = self.height / 2
        
        for i in range(3):
            segment = SnakeSegment()
            segment.size = (self.grid_size, self.grid_size)
            segment.pos = (start_x - i * self.grid_size, start_y)
            self.add_widget(segment)
            self.snake_segments.append(segment)
        
        self.spawn_food()
    
    def spawn_food(self):
        cols = int(self.width / self.grid_size)
        rows = int(self.height / self.grid_size)
        
        while True:
            col = random.randint(0, cols - 1)
            row = random.randint(0, rows - 1)
            x = col * self.grid_size
            y = row * self.grid_size
            
            valid = True
            for segment in self.snake_segments:
                if abs(segment.x - x) < 1 and abs(segment.y - y) < 1:
                    valid = False
                    break
            
            if valid:
                self.food.size = (self.grid_size, self.grid_size)
                self.food.pos = (x, y)
                break
    
    def update(self, dt):
        if self.game_over:
            return
        
        head = self.snake_segments[0]
        new_x = head.x + self.direction_x * self.grid_size
        new_y = head.y + self.direction_y * self.grid_size
        
        if (new_x < 0 or new_x >= self.width or 
            new_y < 0 or new_y >= self.height):
            self.game_over = True
            return
        
        for segment in self.snake_segments:
            if abs(segment.x - new_x) < 1 and abs(segment.y - new_y) < 1:
                self.game_over = True
                return
        
        new_segment = SnakeSegment()
        new_segment.size = (self.grid_size, self.grid_size)
        new_segment.pos = (new_x, new_y)
        self.add_widget(new_segment)
        self.snake_segments.insert(0, new_segment)
        
        if (abs(new_x - self.food.x) < 1 and abs(new_y - self.food.y) < 1):
            self.score += 10
            self.spawn_food()
        else:
            tail = self.snake_segments.pop()
            self.remove_widget(tail)
    
    def draw(self):
        pass

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game

if __name__ == '__main__':
    SnakeApp().run()
