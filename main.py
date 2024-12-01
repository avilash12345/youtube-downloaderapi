import tkinter
import customtkinter
from pytubefix import YouTube
from pytubefix.cli import on_progress

def startdownload():
   try:
       ytlink = link.get()
       ytObject=YouTube(ytlink, on_progress_callback=on_progress)
       video= ytObject.streams.get_audio_only()
       title.configure(text=ytObject.title, text_color="white")
       finishLabel.configure(text="")
       video.download()
       finishLabel.configure(text="Downloaded Successfully....")
   except:
       finishLabel.configure(text="Download error", text_color="red")

def on_progress(stream, chunk, bytes_remaining):
     total_size=stream.filesize
     bytes_downloaded=total_size - bytes_remaining
     percentage_of_completion= bytes_downloaded / total_size * 100
     per=str(int(percentage_of_completion))
     pPercentage.configure(text=per + '%')
     pPercentage.update()
     progessBar.set(float(percentage_of_completion) / 100)
#System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


# app frame
app=customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

#Adding UI Elements
title=customtkinter.CTkLabel(app, text="Insert Youtube Link here")
title.pack(padx=10, pady=10)

# link input
url_var=tkinter.StringVar()
link= customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# finished downloading
finishLabel=customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# progress percentages
pPercentage=customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()
progessBar=customtkinter.CTkProgressBar(app, width=400)
progessBar.set(0)
progessBar.pack(padx=10, pady=10)
# download button
download=customtkinter.CTkButton(app, text="Download", command=startdownload)
download.pack(padx=10, pady=10)


# Run app
app.mainloop()