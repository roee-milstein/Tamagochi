import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox


# מחלקת חיית המחמד הבסיסית
class Tamagotchi(ABC):
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.hunger = 5
        self.happiness = 5
        self.health = 5
        self.energy = 5

    @abstractmethod
    def display_status(self):
        pass


# תתי-מחלקות של חיות המחמד השונות
class Dog(Tamagotchi):
    def __init__(self, name: str):
        super().__init__(name, "Dog")

    def display_status(self):
        return f"{self.name} the {self.species}\nHunger: {self.hunger}\nHappiness: {self.happiness}\nHealth: {self.health}\nEnergy: {self.energy}"


class Cat(Tamagotchi):
    def __init__(self, name: str):
        super().__init__(name, "Cat")

    def display_status(self):
        return f"{self.name} the {self.species}\nHunger: {self.hunger}\nHappiness: {self.happiness}\nHealth: {self.health}\nEnergy: {self.energy}"


# מחלקת Command עבור הפעולות
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# פעולות של החיה
class EatCommand(Command):
    def __init__(self, pet: Tamagotchi, game_window):
        self.pet = pet
        self.game_window = game_window

    def execute(self):
        self.pet.hunger = max(0, self.pet.hunger - 3)
        messagebox.showinfo("Tamagotchi", f"{self.pet.name} ate food. Hunger is now {self.pet.hunger}.")
        self.game_window.update_status()


class SleepCommand(Command):
    def __init__(self, pet: Tamagotchi, game_window):
        self.pet = pet
        self.game_window = game_window

    def execute(self):
        self.pet.energy = min(10, self.pet.energy + 3)
        messagebox.showinfo("Tamagotchi", f"{self.pet.name} slept. Energy is now {self.pet.energy}.")
        self.game_window.update_status()


class PlayCommand(Command):
    def __init__(self, pet: Tamagotchi, game_window):
        self.pet = pet
        self.game_window = game_window

    def execute(self):
        self.pet.happiness = min(10, self.pet.happiness + 3)
        self.pet.energy = max(0, self.pet.energy - 1)
        messagebox.showinfo("Tamagotchi",
                            f"{self.pet.name} played. Happiness is now {self.pet.happiness} and energy is now {self.pet.energy}.")
        self.game_window.update_status()


class ExerciseCommand(Command):
    def __init__(self, pet: Tamagotchi, game_window):
        self.pet = pet
        self.game_window = game_window

    def execute(self):
        self.pet.health = min(10, self.pet.health + 2)
        self.pet.hunger = min(10, self.pet.hunger + 1)
        messagebox.showinfo("Tamagotchi",
                            f"{self.pet.name} exercised. Health is now {self.pet.health} and hunger is now {self.pet.hunger}.")
        self.game_window.update_status()


# מחלקה לניהול המשחק
class GameWindow(tk.Tk):
    def __init__(self, pet: Tamagotchi):
        super().__init__()
        self.pet = pet
        self.title(f"Tamagotchi - {self.pet.name}")
        self.geometry("300x400")

        # תווית סטטוס של חיית המחמד
        self.status_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=20)

        # כפתורים
        self.feed_button = tk.Button(self, text="Feed", command=self.feed)
        self.feed_button.pack(pady=5)

        self.sleep_button = tk.Button(self, text="Sleep", command=self.sleep)
        self.sleep_button.pack(pady=5)

        self.play_button = tk.Button(self, text="Play", command=self.play)
        self.play_button.pack(pady=5)

        self.exercise_button = tk.Button(self, text="Exercise", command=self.exercise)
        self.exercise_button.pack(pady=5)

        # עדכון הסטטוס הראשוני
        self.update_status()

    def update_status(self):
        self.status_label.config(text=self.pet.display_status())

    def feed(self):
        EatCommand(self.pet, self).execute()

    def sleep(self):
        SleepCommand(self.pet, self).execute()

    def play(self):
        PlayCommand(self.pet, self).execute()

    def exercise(self):
        ExerciseCommand(self.pet, self).execute()


# חלון בחירת החיה
class PetSelectionWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tamagotchi - Pet Selection")
        self.geometry("300x200")

        self.label = tk.Label(self, text="Enter the name of your pet:")
        self.label.pack(pady=10)

        self.pet_name_entry = tk.Entry(self)
        self.pet_name_entry.pack(pady=5)

        self.choose_dog_button = tk.Button(self, text="Choose Dog", command=self.choose_dog)
        self.choose_dog_button.pack(pady=5)

        self.choose_cat_button = tk.Button(self, text="Choose Cat", command=self.choose_cat)
        self.choose_cat_button.pack(pady=5)

    def choose_dog(self):
        pet_name = self.pet_name_entry.get()
        if pet_name:
            self.destroy()
            game_window = GameWindow(Dog(pet_name))
            game_window.mainloop()

    def choose_cat(self):
        pet_name = self.pet_name_entry.get()
        if pet_name:
            self.destroy()
            game_window = GameWindow(Cat(pet_name))
            game_window.mainloop()


# הפעלת המשחק עם חלון בחירת חיה
if __name__ == "__main__":
    pet_selection_window = PetSelectionWindow()
    pet_selection_window.mainloop()
