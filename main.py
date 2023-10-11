import pyttsx3
import PyPDF2
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from ctypes import windll


def upload_pdf():
    global text

    filetypes = [('PDF files', '*.pdf')]
    pdf_file = filedialog.askopenfile(initialdir="C:/Users/jayes/Downloads", filetypes=filetypes,
                                      title='Upload pdf file')
    try:
        path = pdf_file.name
    except AttributeError:
        pass
    else:
        if pdf_file:
            with open(path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                # number_of_pages = len(pdf.pages)
                for page in pdf.pages:
                    current_page_text = page.extract_text()
                    text += current_page_text
        else:
            messagebox.showinfo(title="Information window", message='No pdf file was uploaded')


def download_pdf():
    global text, download
    download.config(state='disabled')
    filetypes = [('Mp3 files', '*.mp3'), ("All Files", "*.*")]
    mp3_file_path = filedialog.asksaveasfilename(filetypes=filetypes,
                                                 title='Download Mp3 audio file', defaultextension=".mp3")
    if mp3_file_path and text != '':
        audio.save_to_file(text, mp3_file_path)
        audio.runAndWait()
        messagebox.showinfo(title='Download Information', message='Mp3 Successfully Downloaded')
        download.config(state='normal')
    else:
        messagebox.showinfo(title='Download Information', message='No mp3 file was saved')
        download.config(state='normal')


def play_audio():
    global download, upload, pdf_file
    if text != '':
        download.config(state='disabled')
        upload.config(state='disabled')
        audio.say(text)
        audio.runAndWait()
        download.config(state='normal')
        upload.config(state='normal')


# Download text for saving
text = ''

pdf_file = None  # to prevent play button from acting when there is no file


# reduce blurriness
windll.shcore.SetProcessDpiAwareness(1)

# Create window
window = Tk()
window.minsize(500, 500)
window.title('Pdf to audio convertor')

# create speech system
audio = pyttsx3.init()

# window widgets
img = Image.open('audio.jpg')
image = img.resize((500, 500), Image.LANCZOS)
background = ImageTk.PhotoImage(image)
canvas = Canvas()
canvas.pack(fill=BOTH, expand=True)
canvas.create_image(0, 0, anchor=NW, image=background)
canvas.create_text(250, 150, text='Pdf to Text Speech convertor', font=('arial', 20, 'bold'))

upload = Button(text='Upload pdf file', bg='#e5fcf5', command=upload_pdf)
canvas.create_window(150, 200, window=upload)

download = Button(text='Download Mp3', bg='#e5fcf5', command=download_pdf)
canvas.create_window(350, 200, window=download)

img1 = Image.open('play.jpg')
image1 = img1.resize((100, 100), Image.LANCZOS)
play1 = ImageTk.PhotoImage(image1)
download = Button(image=play1, command=play_audio)
play_button = canvas.create_window(250, 350, window=download)

window.mainloop()
