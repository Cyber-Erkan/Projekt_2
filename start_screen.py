import tkinter as tk
from main import run_game


def start_game(root):
    root.destroy()  # stänger startskärmen
    run_game()      # startar spelet


def create_start_screen():

    root = tk.Tk()
    root.title("Deckbuilder Game")
    root.geometry("400x300")

    title = tk.Label(
        root,
        text="Deckbuilder Game",
        font=("Arial", 24)
    )
    title.pack(pady=40)

    start_button = tk.Button(
        root,
        text="Start Game",
        font=("Arial", 16),
        width=15,
        command=lambda: start_game(root)
    )
    start_button.pack(pady=20)

    quit_button = tk.Button(
        root,
        text="Quit",
        font=("Arial", 12),
        command=root.destroy
    )
    quit_button.pack()

    root.mainloop()


if __name__ == "__main__":
    create_start_screen()