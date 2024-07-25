import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

class ImageSelector(tk.Tk):
    def __init__(self, groundtruth_path, image_paths):
        super().__init__()
        self.title("Select an Image")
        self.geometry("900x1000")
        self.selected_image = None

        self.images = []
        self.image_labels = []
        self.image_paths = image_paths

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        self.groundtruth_image = Image.open(groundtruth_path)
        self.groundtruth_image = self.groundtruth_image.resize((300, 300), Image.LANCZOS)
        self.groundtruth_photo = ImageTk.PhotoImage(self.groundtruth_image)
        self.groundtruth_label = tk.Label(self.main_frame, image=self.groundtruth_photo)
        self.groundtruth_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.instruction_label = tk.Label(self.main_frame, text="Which of the following images looks most similar to the one above?", font=("Helvetica", 14))
        self.instruction_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.load_images()

        self.numbers_list = []

        # Separate frame for averages label
        self.averages_frame = tk.Frame(self)
        self.averages_frame.pack(fill="x", side="bottom")
        self.averages_label = tk.Label(self.averages_frame, text="Averages: N/A", font=("Helvetica", 16))
        self.averages_label.pack(pady=20)

    def load_images(self):
        for idx, path in enumerate(self.image_paths):
            image = Image.open(path)
            image = image.resize((200, 200), Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            self.images.append(photo_image)

            label = tk.Label(self.main_frame, image=photo_image, cursor="hand2")
            label.bind("<Button-1>", lambda e, i=idx: self.select_image(i))
            label.grid(row=(idx//2) + 2, column=idx%2, padx=20, pady=20)
            self.image_labels.append(label)

    def select_image(self, index):
        selected_path = self.image_paths[index]
        numbers = self.extract_numbers_from_filename(selected_path)
        if numbers:
            self.numbers_list.append(numbers)
            average_values = self.calculate_averages(self.numbers_list)
            self.averages_label.config(text=f"Averages: {average_values}")
        self.reset_selection()

    def extract_numbers_from_filename(self, path):
        filename = os.path.basename(path)
        name, _ = os.path.splitext(filename)
        try:
            numbers = [int(n) for n in name.split(',')]
            if len(numbers) == 4:
                return numbers
            else:
                raise ValueError("Filename does not contain exactly four numbers")
        except ValueError as e:
            messagebox.showerror("Error", f"Error processing file {filename}: {e}")
            return None

    def calculate_averages(self, numbers_list):
        if not numbers_list:
            return [0, 0, 0, 0]
        sums = [0, 0, 0, 0]
        for numbers in numbers_list:
            for i in range(4):
                sums[i] += numbers[i]
        count = len(numbers_list)
        averages = [s / count for s in sums]
        return averages

    def reset_selection(self):
        self.selected_image = None
        self.image_paths = get_random_image_paths(directory, 4)
        self.clear_images()
        self.load_images()

    def clear_images(self):
        for label in self.image_labels:
            label.destroy()
        self.images.clear()
        self.image_labels.clear()

def get_random_image_paths(directory, n):
    all_images = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return random.sample(all_images, n)

if __name__ == "__main__":
    directory = "./poolstatmetamer_output"
    groundtruth_path = "./poolstatmetamer_output/groundtruth.png"  # Groundtruth image path
    image_paths = get_random_image_paths(directory, 4)  # Adjust the number of images as needed

    app = ImageSelector(groundtruth_path, image_paths)
    app.mainloop()