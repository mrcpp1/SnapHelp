import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCoordinateFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Coordinate Finder")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.photo = None
        self.displayed_image = None

        self.coord_label = tk.Label(root, text="Coordinates: ")
        self.coord_label.pack()

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.canvas.bind("<Motion>", self.update_coordinates)
        self.root.bind("<Configure>", self.resize_image)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.resize_image()

    def resize_image(self, event=None):
        if self.image:
            # Get the current size of the canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate the scaling factor
            width_ratio = canvas_width / self.image.width
            height_ratio = canvas_height / self.image.height
            scale = min(width_ratio, height_ratio)

            # Resize the image
            new_width = int(self.image.width * scale)
            new_height = int(self.image.height * scale)
            resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)

            self.photo = ImageTk.PhotoImage(resized_image)
            if self.displayed_image:
                self.canvas.delete(self.displayed_image)
            self.displayed_image = self.canvas.create_image(canvas_width//2, canvas_height//2, anchor=tk.CENTER, image=self.photo)

    def update_coordinates(self, event):
        if self.image and self.photo:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Calculate the offset of the image
            image_width = self.photo.width()
            image_height = self.photo.height()
            x_offset = (canvas_width - image_width) // 2
            y_offset = (canvas_height - image_height) // 2

            # Adjust coordinates based on the image position
            x = event.x - x_offset
            y = event.y - y_offset

            if 0 <= x < image_width and 0 <= y < image_height:
                # Convert coordinates to original image scale
                orig_x = int(x * (self.image.width / image_width))
                orig_y = int(y * (self.image.height / image_height))
                rel_x = round(orig_x / self.image.width, 3)
                rel_y = round(orig_y / self.image.height, 3)
                coord_text = f"Coordinates: ({orig_x}, {orig_y}) | Relative: (width*{rel_x:.3f}, height*{rel_y:.3f})"
                self.coord_label.config(text=coord_text)
            else:
                self.coord_label.config(text="Coordinates: Outside image")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Set initial window size
    app = ImageCoordinateFinder(root)
    root.mainloop()