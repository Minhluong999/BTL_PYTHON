import tkinter as tk
from tkinter import messagebox
import pygame

class TTTBoard:
    def __init__(self):
        self.board = [" "] * 9
        self.turn = "X"

    def make_move(self, index):
        if self.board[index] == " ":
            self.board[index] = self.turn
            return True
        return False

    def legal_moves(self):
        return [i for i, val in enumerate(self.board) if val == " "]

    def check_winner(self):
        WAYS = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in WAYS:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        if " " not in self.board:
            return "TIE"
        return None

    def switch_turn(self):
        self.turn = "O" if self.turn == "X" else "X"

    def reset(self):
        self.board = [" "] * 9
        self.turn = "X"

    def computer_move(self):
        board = self.board[:]
        moves = self.legal_moves()

        for move in moves:
            board[move] = "O"
            if self._check_winner(board) == "O":
                return move
            board[move] = " "
        for move in moves:
            board[move] = "X"
            if self._check_winner(board) == "X":
                return move
            board[move] = " "
        BEST = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for move in BEST:
            if move in moves:
                return move

    def _check_winner(self, temp_board):
        WAYS = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in WAYS:
            if temp_board[a] == temp_board[b] == temp_board[c] != " ":
                return temp_board[a]
        if " " not in temp_board:
            return "TIE"
        return None

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro với pygame ")
        self.board = TTTBoard()
        self.buttons = []
        self.game_over = False
        self.mode = self.ask_mode()

        pygame.init()
        pygame.mixer.init()

        self.build_grid()

        self.status_label = tk.Label(root, text="Lượt: X", font=("Arial", 14), bg="#f0f0ff")
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.reset_button = tk.Button(root, text="Chơi lại", command=self.reset_game, bg="#ddd", font=("Arial", 12))
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

    def ask_mode(self):
        answer = messagebox.askquestion("Chế độ chơi", "Bạn muốn chơi với máy?")
        return "AI" if answer == "yes" else "PVP"

    def build_grid(self):
        for i in range(9):
            btn = tk.Button(
                self.root, text=" ", font=("Helvetica", 28, "bold"), width=5, height=2,
                bg="#ffffff", activebackground="#dff6f0",
                command=lambda i=i: self.handle_click(i)
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    def play_sound(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
        except Exception as e:
            print("Lỗi âm thanh:", e)

    def handle_click(self, index):
        if self.game_over:
            return
        if self.board.make_move(index):
            self.buttons[index].config(
                text=self.board.turn,
                state="disabled",
                disabledforeground="blue" if self.board.turn == "X" else "red"
            )
            self.play_sound("click.mp3")
            winner = self.board.check_winner()
            if winner:
                self.end_game(winner)
            else:
                if self.mode == "PVP":
                    self.board.switch_turn()
                    self.status_label.config(text=f"Lượt: {self.board.turn}")
                else:
                    self.board.switch_turn()
                    self.status_label.config(text="Máy đang nghĩ...")
                    self.root.after(500, self.computer_play)

    def computer_play(self):
        if self.game_over:
            return
        move = self.board.computer_move()
        if move is not None:
            self.board.make_move(move)
            self.buttons[move].config(
                text="O", state="disabled", disabledforeground="red"
            )
            self.play_sound("click.mp3")
            winner = self.board.check_winner()
            if winner:
                self.end_game(winner)
            else:
                self.board.switch_turn()
                self.status_label.config(text=f"Lượt: {self.board.turn}")

    def end_game(self, winner):
        self.game_over = True
        if winner == "TIE":
            self.play_sound("tie.mp3")
            messagebox.showinfo("Kết quả", "Hòa!")
            self.status_label.config(text="Hòa!")
        else:
            self.play_sound("win.mp3")
            messagebox.showinfo("Kết quả", f"{winner} thắng!")
            self.status_label.config(text=f"{winner} thắng!")
        self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self):
        self.board.reset()
        self.game_over = False
        for btn in self.buttons:
            btn.config(text=" ", state="normal", bg="#ffffff")
        self.status_label.config(text="Lượt: X")
        self.mode = self.ask_mode()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#f0f0ff")
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(i, weight=1)
    game = TicTacToeGUI(root)
    root.mainloop()
