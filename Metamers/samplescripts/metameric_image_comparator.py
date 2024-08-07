import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot as plt

class ImageSelector(tk.Tk):
    def __init__(self, directories):
        super().__init__()
        self.title("Select an Image")
        self.geometry("1500x1400")
        self.selected_image = None

        self.images = []
        self.image_labels = []
        self.directories = directories
        self.results = {"correct": 0, "wrong": 0, "too_similar": 0}
        self.accuracy_history = []

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Result display label
        self.result_label = tk.Label(self, text="Correct: 0 | Wrong: 0 | Too Similar: 0 | Accuracy: N/A", font=("Helvetica", 14))
        self.result_label.pack(side="bottom", pady=10)

        # Button to mark the images as too similar
        self.skip_button = tk.Button(self, text="Too Similar", command=self.skip_selection, font=("Helvetica", 14))
        self.skip_button.pack(side="bottom", pady=10)

        # Button to quit and save results
        self.quit_button = tk.Button(self, text="Quit and Save", command=self.quit_and_save, font=("Helvetica", 14))
        self.quit_button.pack(side="bottom", pady=10)

        self.reset_selection()

    def load_images(self, image_paths, groundtruth_path):
        self.clear_images()

        # Instruction label
        self.instruction_label = tk.Label(self.main_frame, text="Which of the following images looks most similar to the one in the center?", font=("Helvetica", 14))
        self.instruction_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Load and display candidate images
        for idx, path in enumerate(image_paths):
            image = Image.open(path)
            image = image.resize((300, 300), Image.LANCZOS)
            photo_image = self.add_red_dot(image)
            self.images.append(photo_image)

            label = tk.Label(self.main_frame, image=photo_image, cursor="hand2")
            label.bind("<Button-1>", lambda e, i=idx: self.select_image(i))
            label.bind("<Enter>", lambda e, i=idx: self.show_hover_image(i))
            label.bind("<Leave>", lambda e: self.show_groundtruth_image())
            label.grid(row=1 + idx, column=0, padx=20, pady=20, sticky="n")
            self.image_labels.append(label)

        # Load and display groundtruth image
        self.groundtruth_image = Image.open(groundtruth_path)
        self.groundtruth_image = self.groundtruth_image.resize((1080, 1080), Image.LANCZOS)
        self.groundtruth_photo = self.add_red_dot(self.groundtruth_image)
        self.groundtruth_label = tk.Label(self.main_frame, image=self.groundtruth_photo)
        self.groundtruth_label.grid(row=1, column=1, rowspan=2, padx=20, pady=20)

    def add_red_dot(self, image):
        # Add a red dot to the center of the image
        image_with_dot = image.copy()
        draw = ImageDraw.Draw(image_with_dot)
        x, y = image_with_dot.size
        center = (x // 2, y // 2)
        radius = 5
        draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill='red', outline='red')
        return ImageTk.PhotoImage(image_with_dot)

    def show_hover_image(self, index):
        # Show the hover image with a red dot when the mouse is over the candidate image
        image_path = self.image_paths[index]
        hover_image = Image.open(image_path)
        hover_image = hover_image.resize((1080, 1080), Image.LANCZOS)
        hover_photo_image = self.add_red_dot(hover_image)
        self.groundtruth_label.config(image=hover_photo_image)
        self.groundtruth_label.image = hover_photo_image

    def show_groundtruth_image(self):
        # Restore the groundtruth image when the mouse leaves the candidate image
        self.groundtruth_label.config(image=self.groundtruth_photo)
        self.groundtruth_label.image = self.groundtruth_photo

    def select_image(self, index):
        # Handle image selection and update results
        selected_path = self.image_paths[index]
        result = self.calculate_result(selected_path)
        if result == "correct":
            self.results["correct"] += 1
        else:
            self.results["wrong"] += 1
        self.update_result_label()
        self.reset_selection()

    def skip_selection(self):
        # Mark the selection as too similar
        self.results["too_similar"] += 1
        self.update_result_label()
        self.reset_selection()

    def calculate_result(self, path):
        # Calculate whether the selected image is correct or wrong based on predefined criteria
        filename = os.path.basename(path)
        name, _ = os.path.splitext(filename)
        numbers = [int(n) for n in name.split(',')]
        differences = [10 * abs(numbers[0] - 6), abs(numbers[1] - 35), 0.1 * abs(numbers[2] - 600)]
        total_difference = sum(differences)

        other_path = self.image_paths[1] if self.image_paths[0] == path else self.image_paths[0]
        other_filename = os.path.basename(other_path)
        other_name, _ = os.path.splitext(other_filename)
        other_numbers = [int(n) for n in other_name.split(',')]
        other_differences = [abs(other_numbers[0] - 6), abs(other_numbers[1] - 30), abs(other_numbers[2] - 650)]
        other_total_difference = sum(other_differences)

        if total_difference < other_total_difference:
            return "correct"
        else:
            return "wrong"

    def update_result_label(self):
        # Update the result label with the current statistics
        correct = self.results['correct']
        wrong = self.results['wrong']
        accuracy = (correct / (correct + wrong) * 100) if (correct + wrong) > 0 else 0
        self.accuracy_history.append(accuracy)
        self.result_label.config(text=f"Correct: {correct} | Wrong: {wrong} | Too Similar: {self.results['too_similar']} | Accuracy: {accuracy:.2f}%")

    def reset_selection(self):
        # Reset the selection and load new images
        self.selected_image = None
        selected_folder = random.choice(self.directories)
        groundtruth_path = os.path.join(selected_folder, 'groundtruth.png')
        self.image_paths = get_random_image_paths(selected_folder, 2)
        self.load_images(self.image_paths, groundtruth_path)

    def clear_images(self):
        # Clear the currently displayed images
        for label in self.image_labels:
            label.destroy()
        self.images.clear()
        self.image_labels.clear()
        if hasattr(self, 'groundtruth_label'):
            self.groundtruth_label.destroy()

    def quit_and_save(self):
        # Save the accuracy plot and quit the application
        self.save_accuracy_plot()
        self.quit()

    def save_accuracy_plot(self):
        # Save the accuracy history plot as an image file
        plt.figure()
        plt.plot(self.accuracy_history, marker='o', linestyle='-', color='b')
        plt.title('Accuracy Over Time')
        plt.xlabel('Attempt Number')
        plt.ylabel('Accuracy (%)')
        plt.savefig('accuracy_plot.png')
        plt.show()

def get_random_image_paths(selected_folder, n):
    # Get n random image paths from the selected folder
    all_images = [os.path.join(selected_folder, f) for f in os.listdir(selected_folder) if f.endswith(('.png', '.jpg', '.jpeg')) and f != 'groundtruth.png']
    return random.sample(all_images, n)

if __name__ == "__main__":
    directories = ["./Dataset/bigben-1080", "./Dataset/Einstein-1080"]

    app = ImageSelector(directories)
    app.mainloop()