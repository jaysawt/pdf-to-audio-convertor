import PyPDF2
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from ctypes import windll
import os
import requests
import sys

API_KEY_VOICE = os.environ.get('API_KEY_VOICE_RSS')
url_voice = 'http://api.voicerss.org/'
text = ''
pdf_file = None


def upload_pdf():
    global text, pdf_file
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
                for page in pdf.pages:
                    current_page_text = page.extract_text()
                    text += current_page_text
                print(sys.getsizeof(text) / 1024)
            messagebox.showinfo(title='Information window', message='Files added successfully')
        else:
            messagebox.showinfo(title="Information window", message='No pdf file was uploaded')


def play_audio():
    global download, upload, pdf_file
    if text != '':
        #The below is used for large file content as POST requests send data in the request body rather than as part
        # of the URL, which can help avoid the URL length limitation.
        header = {'Content-Type': 'application/x-www-form-urlencoded'} # The headers dictionary specifies the content type as application/x-www-form-urlencoded.
        datas = {
            'key': API_KEY_VOICE,
            'hl': 'en-us',
            'src': text.strip(),
            'c': 'MP3',
        }
        response = requests.get(url=url_voice, data=datas, headers=header)

        #ONLY APPLICABLE IF FILES ARE SMALL
        # parameters = {
        #     'key': API_KEY_VOICE,
        #     'hl': 'en-us',
        #     'src': text.strip(),
        #     'c': 'MP3',
        # }
        # response = requests.get(url=url_voice, params=parameters)
        # response.raise_for_status()
        if response.status_code == 200:
            with open('speech2text.mp3', 'wb') as f:
                f.write(response.content)
            messagebox.showinfo(title='File Information',
                                message='Your file has been successfully downloaded')
        else:
            messagebox.showinfo(title='File Information',
                                message='Failed to generate audio')
    else:
        messagebox.showinfo(title='File Information', message='No File has been uploaded, Please provide a Pdf file')


#reduce blurness
windll.shcore.SetProcessDpiAwareness(1)

#Create window
window = Tk()
window.minsize(500, 500)
window.title('Pdf to audio convertor')



#window widgets
img = Image.open('mountain.jpg')
image = img.resize((500, 500), Image.LANCZOS)
background = ImageTk.PhotoImage(image)
canvas = Canvas()
canvas.pack(fill=BOTH, expand=True)
canvas.create_image(0, 0, anchor=NW, image=background)
canvas.create_text(250, 100, text='Pdf to Text Speech convertor', font=('arial', 20, 'bold'), fill='white')

upload = Button(text='Upload pdf file', bg='#f6debf', command=upload_pdf, height=1, width=15)
canvas.create_window(250, 250, window=upload)

download = Button(text='Download Mp3', bg='#82a4b3', command=play_audio, height=1, width=15)
canvas.create_window(250, 350, window=download)

window.mainloop()
