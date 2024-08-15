import customtkinter
import tkinter
from yt_dlp import YoutubeDL
import re
from utils import bytes_to_mibs

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("System")
        # self.geometry("400x400")
        self.title("Yoututbe Downloader")
        self.linkvar = tkinter.StringVar(self)
        # self.iconphoto(True,'./banner.png')
        # self.iconphoto = customtkinter.CTkImage()
        self.label = customtkinter.CTkLabel(self,text="Please insert the link below to download the video.",font=customtkinter.CTkFont(size=20))
        self.label.pack(padx=10,pady=20)
        self.linkInput = customtkinter.CTkEntry(self,placeholder_text="https://www.youtube.com/watch?v=crCzoThnJFE",width=400,textvariable=self.linkvar)
        self.linkInput.pack(padx=10,pady=20)
        self.progressText = customtkinter.CTkLabel(self,text="")
        self.progressText.pack(padx=10,pady=20)
        self.progressBar = customtkinter.CTkProgressBar(self,width=400)
        self.progressBar.set(0.0)
        self.button = customtkinter.CTkButton(self, text="Download", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

    def button_callbck(self):
        print(f"Url Pasted: {self.linkvar.get()}")
        if(self.verify_link(link=self.linkvar.get())):
            self.download_video_single(link=self.linkvar.get(),progress_callback=self.progress_callback)
        else:
            print("Invalid Youtube URL")

    def progress_callback(self,progressMap):
        self.label.configure(text=progressMap['filename'])
        self.label.update()
        self.progressBar.pack(padx=10,pady=10)
        self.progressText.pack(padx=10,pady=10)
        if 'total_bytes' in progressMap.keys():
            per = str(round(progressMap['downloaded_bytes']/progressMap['total_bytes']*100,2))
            self.progressText.configure(text=per+ f"% at " + str(bytes_to_mibs(int(progressMap['speed'])))+f" MiB/s")
            self.progressText.update()
            self.progressBar.set(progressMap['downloaded_bytes']/progressMap['total_bytes'])
        else:
            per = str(round(progressMap['fragment_index']/progressMap['fragment_count']*100,2))
            self.progressText.configure(text=per+ f"% at " + str(bytes_to_mibs(int(progressMap['speed'])))+f" MiB/s")
            self.progressText.update()
            self.progressBar.set(progressMap['fragment_index']/progressMap['fragment_count'])

    def verify_link(self,link:str)->bool:
        regex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        return bool(re.match(regex,link))

    def download_video_single(self,link:str,progress_callback:callable):
        yt_dlp = YoutubeDL({
            'wait_for_video':(10,60),
            'format':self.format_selector,
            'progress_hooks': [progress_callback],
            },auto_init=True)
        yt_dlp.download(url_list=[link])

    def format_selector(self,ctx):
        """ Select the best video and the best audio that won't result in an mkv.
        NOTE: This is just an example and does not handle all cases """

        # formats are already sorted worst to best
        formats = ctx.get('formats')[::-1]

        # acodec='none' means there is no audio
        best_video = next(f for f in formats
                        if f['vcodec'] != 'none' and f['acodec'] == 'none')

        # find compatible audio extension
        audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
        # vcodec='none' means there is no video
        best_audio = next(f for f in formats if (
            f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

        # These are the minimum required fields for a merged format
        yield {
            'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
            'ext': best_video['ext'],
            'requested_formats': [best_video, best_audio],
            # Must be + separated list of protocols
            'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
        }

app = App()
app.mainloop()