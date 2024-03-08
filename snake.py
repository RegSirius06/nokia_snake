__all__ = ["SnakeGame"]

import random
import tkinter as tk

class SnakeGame:
    def __init__(self, master, *, width=600, height=600, scale=30, speed=100, \
                 area_apples=0):
        self.master = master

        self.cnt = 0
        self.process = True
        self.width = width
        self.height = height
        self.scale = scale
        self.delay = speed
        self.area_apples = area_apples

        self.generate_snake()
        self.food = self.generate_food_position()

        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        self.master.bind("<KeyPress>", self.change_direction)

        self.draw_snake()
        self.draw_food()
        self.move()

        self.master.update()

    def generate_direction(self):
        self.move_direction = random.choice(["Up", "Down", "Left", "Right"])
        self.prev_direction = None

    def generate_food_position(self):
        position = [random.randint(0 + self.area_apples, self.width // self.scale - 1 - self.area_apples), random.randint(0 + self.area_apples, self.height // self.scale - 1 - self.area_apples)]
        while position in self.snake:
            position = [random.randint(0 + self.area_apples, self.width // self.scale - 1 - self.area_apples), random.randint(0 + self.area_apples, self.height // self.scale - 1 - self.area_apples)]
        return position

    def generate_snake(self):
        self.cnt = 0
        self.process = True
        self.snake = [[random.randint(4, self.width // self.scale - 5), random.randint(4, self.height // self.scale - 5)]]
        self.generate_direction()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x*self.scale, y*self.scale, (x+1)*self.scale, (y+1)*self.scale, fill='green', tag="snake")

    def draw_food(self):
        x, y = self.food
        self.canvas.delete("food")
        self.canvas.create_oval(x*self.scale, y*self.scale, (x+1)*self.scale, (y+1)*self.scale, fill='red', tag="food")
        
    def change_direction(self, event):
        key = event.keysym
        if key in {"Up", "Down", "Left", "Right"}:
            if (key == "Up" and self.prev_direction != "Down") or \
                (key == "Down" and self.prev_direction != "Up") or \
                 (key == "Left" and self.prev_direction != "Right") or \
                  (key == "Right" and self.prev_direction != "Left"):
                self.prev_direction = self.move_direction if len(self.snake) > 1 else None
                self.move_direction = key

    def move(self):
        head = self.snake[0].copy()
        
        if self.move_direction == "Up":
            head[1] -= 1
        elif self.move_direction == "Down":
            head[1] += 1
        elif self.move_direction == "Left":
            head[0] -= 1
        elif self.move_direction == "Right":
            head[0] += 1
            
        if head[0] < 0 or head[0] >= self.width // self.scale or head[1] < 0 or head[1] >= self.height // self.scale or head in self.snake:
            self.canvas.create_text(self.width // 2, self.height // 2 - 80, text="Игра окончена", fill="white", font=("Helvetica", 60), tag="text")
            self.canvas.create_text(self.width // 2, self.height // 2 - 10, text=f"Счёт: {self.cnt}", fill="white", font=("Helvetica", 45), tag="text")
            retry_text = self.canvas.create_text(self.width // 2 - 80, self.height // 2 + 45, text="Повторить", fill="white", font=("Helvetica", 30), tag="text")
            exit_text = self.canvas.create_text(self.width // 2 + 100, self.height // 2 + 45, text="Выйти", fill="white", font=("Helvetica", 30), tag="text")
            self.canvas.tag_bind(retry_text, '<Button-1>', self.restart_game)
            self.canvas.tag_bind(exit_text, '<Button-1>', self.exit_game)
            self.process = False
            return
        
        self.prev_direction = self.move_direction if self.prev_direction else None
        
        self.snake.insert(0, head)
        
        if head == self.food:
            self.food = self.generate_food_position()
            self.cnt += 1
            if self.prev_direction is None:
                self.prev_direction = self.move_direction
        else:
            tail = self.snake.pop()
            self.canvas.delete(tail)
            
        self.draw_snake()
        self.draw_food()
        
        self.master.after(self.delay, self.move)

    def restart_game(self, event):
        self.generate_snake()
        self.food = self.generate_food_position()
        self.canvas.delete("snake")
        self.canvas.delete("food")
        self.canvas.delete("text")
        self.move()

    def exit_game(self, event):
        self.master.destroy()

    def start_new_game(self, width=600, height=600, scale=30, speed=100, area_apples=0):
        self.width = width
        self.height = height
        self.scale = scale
        self.delay = speed
        self.area_apples = area_apples
        self.generate_snake()
        self.food = self.generate_food_position()
        self.canvas.delete("snake")
        self.canvas.delete("food")
        self.canvas.delete("text")
        self.move()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
