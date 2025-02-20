import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ColorPicker:
    #Initializing Front-End 
    def __init__(self, root):
        self.root = root
        self.root.title("Image Color Picker")
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.btn_upload = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.btn_upload.pack()
        self.color_label = tk.Label(root, text="Hex Color: #FFFFFF", font=("Arial", 14))
        self.color_label.pack()
        self.copy_button = tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack()
        self.image = None  
        self.photo = None  
        self.hex_color = "#FFFFFF"
        self.root.bind("<Configure>", self.resize_image)
        self.canvas.bind("<Button-1>", self.get_color)
    
    #Upload an image
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.convert("RGB")
            # Resize after uploading
            self.resize_image()  

    #Resizes the image to always fit inside the window screen
    def resize_image(self, event=None):
        if self.image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 0 and canvas_height > 0:
                img_width, img_height = self.image.size
                # Calculate the new size maintaining the aspect ratio
                ratio = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                # Resize the image while maintaining its aspect ratio
                resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(resized_image)
                self.canvas.delete("all")
                self.canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=self.photo)

    #Obtain the Hex code by clicking on the image
    def get_color(self, event):
        if self.image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_width, img_height = self.photo.width(), self.photo.height()
            x_offset = (canvas_width - img_width) // 2
            y_offset = (canvas_height - img_height) // 2
            x, y = event.x - x_offset, event.y - y_offset
            if 0 <= x < img_width and 0 <= y < img_height:
                orig_x = int(x * (self.image.width / img_width))
                orig_y = int(y * (self.image.height / img_height))
                rgb = self.image.getpixel((orig_x, orig_y))
                self.hex_color = "#{:02X}{:02X}{:02X}".format(*rgb)
                self.color_label.config(text=f"Hex Color: {self.hex_color}", bg=self.hex_color)

    #Copy the Hex code to your clipboard
    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.hex_color)
        self.root.update()  # Required for clipboard to work properly

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPicker(root)
    root.mainloop()
