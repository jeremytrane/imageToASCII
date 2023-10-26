import tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image

def image_to_ascii(image_path, output_width):
    ascii_chars = "@%#*+=-:. "
    img = Image.open(image_path)
    width, height = img.size
    aspect_ratio = height / float(width)
    output_height = int(output_width * aspect_ratio)
    img = img.resize((output_width, output_height))
    img = img.convert('L')
    pixels = list(img.getdata())
    normalized_pixels = [int((pixel / 255) * (len(ascii_chars) - 1)) for pixel in pixels]

    grayscale_chars = [ascii_chars[pixel] for pixel in normalized_pixels]
    ascii_image = [grayscale_chars[index: index + output_width] for index in range(0, len(grayscale_chars), output_width)]
    return "\n".join(["".join(row) for row in ascii_image])


def select_image():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif")])
    if file_path:
        image_path.set(file_path)
        img = Image.open(file_path)
        width, height = img.size
        aspect_ratio = height / float(width)
        output_width_entry.delete(0, tk.END)
        output_width_entry.insert(0, str(int(100 * aspect_ratio)))

def save_ascii_to_file():
    output = ascii_output.get("1.0", tk.END).strip()
    if not output:
        messagebox.showerror("Error", "No ASCII art to save.")
        return

    save_path = filedialog.asksaveasfilename(title="Save ASCII Art", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(output)
        messagebox.showinfo("Info", f"ASCII art saved to {save_path}")

def generate_ascii():
    path = image_path.get()
    if not path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    width = int(output_width_entry.get())
    ascii_result = image_to_ascii(path, width)
    ascii_output.delete("1.0", tk.END)
    ascii_output.insert(tk.END, ascii_result)

app = tk.Tk()
app.title("Image to ASCII Converter")

image_path = tk.StringVar()

controls_frame = tk.Frame(app)
controls_frame.pack(pady=20)

tk.Button(controls_frame, text="Select Image", command=select_image).grid(row=0, column=0, padx=10)
tk.Label(controls_frame, text="Output Width:").grid(row=0, column=1, padx=10)
output_width_entry = tk.Entry(controls_frame)
output_width_entry.grid(row=0, column=2, padx=10)
tk.Button(controls_frame, text="Generate ASCII", command=generate_ascii).grid(row=0, column=3, padx=10)

ascii_output_frame = tk.Frame(app)
ascii_output_frame.pack(pady=20)

scrollbar = tk.Scrollbar(ascii_output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

small_font = font.Font(size=8)
ascii_output = tk.Text(ascii_output_frame, wrap=tk.WORD, width=100, height=30, font=small_font, yscrollcommand=scrollbar.set)
ascii_output.pack(pady=20)

scrollbar.config(command=ascii_output.yview)

tk.Button(app, text="Save ASCII to File", command=save_ascii_to_file).pack()

app.mainloop()
