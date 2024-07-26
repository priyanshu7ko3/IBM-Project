import os
from tkinter import Tk, Label, Button, Text, Scrollbar, filedialog, messagebox, ttk
from PIL import Image
import pytesseract
from transformers import pipeline, logging

# Suppress unnecessary warnings
logging.set_verbosity_error()

# Function to extract text from an image
def extract_text(image_path):
    try:
        print(f"Opening image file: {image_path}")
        # Open the image file
        image = Image.open(image_path)
        
        print("Performing OCR on the image")
        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(image)
        return text
    except FileNotFoundError:
        print(f"The file {image_path} does not exist.")
        return None
    except PermissionError:
        print(f"Permission denied for the file {image_path}.")
        return None
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None

# Function to summarize text
def summarize_text(text):
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"An error occurred while summarizing text: {e}")
        return "Could not summarize text."

# Function to upload an image and process it
def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if file_path:
        progress_bar.start()
        text = extract_text(file_path)
        if text:
            print("Extracted Text: ", text)
            summary = summarize_text(text)
            print("Summary: ", summary)
            extracted_text_box.config(state='normal')
            extracted_text_box.delete(1.0, 'end')
            extracted_text_box.insert('end', text)
            extracted_text_box.config(state='disabled')
            summary_text_box.config(state='normal')
            summary_text_box.delete(1.0, 'end')
            summary_text_box.insert('end', summary)
            summary_text_box.config(state='disabled')
        else:
            messagebox.showerror("Error", "No text extracted from the image.")
    else:
        messagebox.showwarning("Warning", "No file selected.")
    progress_bar.stop()

# Set up the GUI
root = Tk()
root.title("Image Text Summarizer")
root.geometry("800x600")

# Upload Button
upload_button = Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
progress_bar.pack(pady=10, fill='x')

# Text Boxes
text_frame = ttk.Frame(root)
text_frame.pack(pady=10, fill='both', expand=True)

text_label = Label(text_frame, text="Extracted Text:")
text_label.pack(anchor='w')

extracted_text_box = Text(text_frame, wrap='word', height=10)
extracted_text_box.pack(pady=5, fill='both', expand=True)
extracted_text_box.config(state='disabled')

scrollbar = Scrollbar(text_frame)
scrollbar.pack(side='right', fill='y')
extracted_text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=extracted_text_box.yview)

summary_label = Label(text_frame, text="Summary:")
summary_label.pack(anchor='w')

summary_text_box = Text(text_frame, wrap='word', height=10)
summary_text_box.pack(pady=5, fill='both', expand=True)
summary_text_box.config(state='disabled')

scrollbar_summary = Scrollbar(text_frame)
scrollbar_summary.pack(side='right', fill='y')
summary_text_box.config(yscrollcommand=scrollbar_summary.set)
scrollbar_summary.config(command=summary_text_box.yview)

root.mainloop()

