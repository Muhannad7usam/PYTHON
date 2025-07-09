import customtkinter as ctk
import random
from PIL import Image, ImageTk

class ModernHangman:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root.title("Modern Hangman")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Game variables
        self.word_list = ["PYTHON", "JAVASCRIPT", "DEVELOPER", "KEYBOARD", "GAMING", "ALGORITHM"]
        self.chosen_word = random.choice(self.word_list)
        self.correct_letters = set()
        self.wrong_letters = set()
        self.lives = 6
        self.hangman_images = []
        
        # Load assets
        self.load_images()
        
        # Create UI
        self.create_widgets()
        self.update_display()

    def load_images(self):
        """Load hangman progression images"""
        for i in range(7):
            try:
                img = ctk.CTkImage(Image.open(f"assets/hangman_{i}.png"), size=(300, 300))
                self.hangman_images.append(img)
            except:
                # Fallback if images not found
                self.hangman_images.append(None)

    def create_widgets(self):
        """Create all UI components"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Header
        self.header = ctk.CTkLabel(
            self.main_frame, 
            text="MODERN HANGMAN",
            font=("Arial", 24, "bold"),
            text_color="#4CC9F0"
        )
        self.header.pack(pady=20)
        
        # Hangman image
        self.image_label = ctk.CTkLabel(self.main_frame, text="", image=self.hangman_images[0])
        self.image_label.pack(pady=10)
        
        # Word display
        self.word_display = ctk.CTkLabel(
            self.main_frame,
            text="_ _ _ _ _",
            font=("Consolas", 36, "bold"),
            text_color="#F72585"
        )
        self.word_display.pack(pady=20)
        
        # Wrong letters
        self.wrong_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.wrong_frame.pack()
        
        ctk.CTkLabel(
            self.wrong_frame,
            text="Wrong Letters:",
            font=("Arial", 14),
            text_color="#7209B7"
        ).pack(side="left")
        
        self.wrong_display = ctk.CTkLabel(
            self.wrong_frame,
            text="",
            font=("Arial", 14, "bold"),
            text_color="#F72585"
        )
        self.wrong_display.pack(side="left", padx=5)
        
        # Lives counter
        self.lives_display = ctk.CTkLabel(
            self.main_frame,
            text=f"❤️ Lives: {self.lives}",
            font=("Arial", 16),
            text_color="#4CC9F0"
        )
        self.lives_display.pack(pady=10)
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(pady=20)
        
        self.guess_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter a letter",
            width=200,
            height=40,
            font=("Arial", 16)
        )
        self.guess_entry.pack(side="left", padx=5)
        
        self.guess_button = ctk.CTkButton(
            self.input_frame,
            text="Guess",
            command=self.process_guess,
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#7209B7",
            hover_color="#3A0CA3"
        )
        self.guess_button.pack(side="left", padx=5)
        
        self.word_button = ctk.CTkButton(
            self.input_frame,
            text="Guess Word",
            command=self.guess_word,
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4361EE",
            hover_color="#3A0CA3"
        )
        self.word_button.pack(side="left", padx=5)
        
        # Restart button
        self.restart_button = ctk.CTkButton(
            self.main_frame,
            text="New Game",
            command=self.restart_game,
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4CC9F0",
            hover_color="#4895EF"
        )
        self.restart_button.pack(pady=20)

    def update_display(self):
        """Update all game displays"""
        # Update word display
        display_word = ' '.join([letter if letter in self.correct_letters else '_' for letter in self.chosen_word])
        self.word_display.configure(text=display_word)
        
        # Update wrong letters
        self.wrong_display.configure(text=', '.join(sorted(self.wrong_letters)))
        
        # Update lives
        self.lives_display.configure(text=f"❤️ Lives: {self.lives}")
        
        # Update hangman image
        if self.hangman_images and len(self.hangman_images) > (6 - self.lives):
            self.image_label.configure(image=self.hangman_images[6 - self.lives])
        
        # Check game status
        if all(letter in self.correct_letters for letter in self.chosen_word):
            self.show_victory()
        elif self.lives <= 0:
            self.show_defeat()

    def process_guess(self):
        """Process a single letter guess"""
        guess = self.guess_entry.get().upper()
        self.guess_entry.delete(0, 'end')
        
        if not guess.isalpha() or len(guess) != 1:
            self.show_error("Invalid Input", "Please enter a single letter")
            return
            
        if guess in self.correct_letters or guess in self.wrong_letters:
            self.show_error("Already Guessed", f"You've already tried '{guess}'")
            return
            
        if guess in self.chosen_word:
            self.correct_letters.add(guess)
        else:
            self.wrong_letters.add(guess)
            self.lives -= 1
            
        self.update_display()

    def guess_word(self):
        """Process a whole word guess"""
        guess = self.guess_entry.get().upper()
        self.guess_entry.delete(0, 'end')
        
        if not guess.isalpha():
            self.show_error("Invalid Input", "Please enter letters only")
            return
            
        if guess == self.chosen_word:
            self.correct_letters.update(set(self.chosen_word))
            self.show_victory()
        else:
            self.lives -= 1
            self.show_error("Incorrect", f"'{guess}' is not the correct word")
            self.update_display()

    def show_victory(self):
        """Show victory message"""
        self.disable_input()
        dialog = ctk.CTkInputDialog(
            text=f"🎉 You won! The word was: {self.chosen_word}\nPlay again?",
            title="Victory!"
        )
        if dialog.get_input() is not None:
            self.restart_game()

    def show_defeat(self):
        """Show defeat message"""
        self.disable_input()
        dialog = ctk.CTkInputDialog(
            text=f"☠️ Game Over! The word was: {self.chosen_word}\nTry again?",
            title="Defeat"
        )
        if dialog.get_input() is not None:
            self.restart_game()

    def show_error(self, title, message):
        """Show error message"""
        error = ctk.CTkToplevel()
        error.title(title)
        error.geometry("300x150")
        error.resizable(False, False)
        
        ctk.CTkLabel(
            error,
            text=message,
            font=("Arial", 14)
        ).pack(pady=20)
        
        ctk.CTkButton(
            error,
            text="OK",
            command=error.destroy,
            fg_color="#7209B7"
        ).pack(pady=10)

    def disable_input(self):
        """Disable input after game ends"""
        self.guess_entry.configure(state="disabled")
        self.guess_button.configure(state="disabled")
        self.word_button.configure(state="disabled")

    def restart_game(self):
        """Start a new game"""
        self.chosen_word = random.choice(self.word_list)
        self.correct_letters = set()
        self.wrong_letters = set()
        self.lives = 6
        self.guess_entry.configure(state="normal")
        self.guess_button.configure(state="normal")
        self.word_button.configure(state="normal")
        self.update_display()

if __name__ == "__main__":
    root = ctk.CTk()
    game = ModernHangman(root)
    root.mainloop()