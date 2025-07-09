import json
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox

import os
import pyautogui as au
import time


def uploadTT():

    webbrowser.open_new_tab('https://www.tiktok.com/tiktokstudio/upload?from=webapp')
    au.PAUSE = 1
    target='targets/uploadTT.png'
    time.sleep(5)
    try:
        location=au.locateCenterOnScreen(target,confidence=0.8)
        au.click(location)
        time.sleep(0.5)
        target='targets/uploadChrome.png'
        location=au.locateCenterOnScreen(target,confidence=0.8)
        new_x=location.x+400
        new_y=location.y+30
        au.click(new_x,new_y)
    except Exception as e:
        print(e)

    with open('date_upload.json','r') as f:
        data = json.load(f)
    path=os.path.dirname(data['path'])
    au.write(path)
    au.press('enter')
    au.press('tab',presses=5)
    fisier=os.path.basename(data['path'])
    au.write(fisier)
    au.press('enter')
    au.hotkey('ctrl','a')
    au.press('backspace')
    #ne aflam in descriere la tt


class VideoUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Uploader de videoclipuri")

        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack()
        # Etichete și câmpuri

        tk.Label(self.main_frame, text="Titlu:").grid(row=0, column=0, sticky="e", pady=5)
        self.title_entry = tk.Entry(self.main_frame, width=50)
        self.title_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.main_frame, text="Descriere:").grid(row=1, column=0, sticky="ne", pady=5)
        self.description_text = tk.Text(self.main_frame, width=50, height=5)
        self.description_text.grid(row=1, column=1, pady=5)

        tk.Label(self.main_frame, text="Hashtag-uri:").grid(row=2, column=0, sticky="ne", pady=5)
        self.hashtags_text = tk.Text(self.main_frame, width=50, height=2)
        self.hashtags_text.grid(row=2, column=1, pady=5)

        tk.Label(self.main_frame, text="Fișier video:").grid(row=3, column=0, sticky="e", pady=5)
        self.video_path_label = tk.Label(self.main_frame, text="Neselectat", fg="gray", anchor="w", width=50,
                                         wraplength=400, justify="left")
        self.video_path_label.grid(row=3, column=1, sticky="w", pady=5)

        tk.Button(self.main_frame, text="Selectează fișierul", command=self.select_video).grid(row=4, column=1,
                                                                                               sticky="w", pady=10)
        tk.Button(self.main_frame, text="Salvează și continuă", command=self.submit).grid(row=5, column=1, sticky="e",
                                                                                          pady=10)


        self.video_path = ""
        self.default_video_folder = 'F:\\clipuri tt'

    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="Selectează un fișier video",
            initialdir=self.default_video_folder,
            filetypes=[("Fișiere video", "*.mp4 *.mov *.avi *.mkv")]
        )
        if file_path:
            self.video_path = file_path
            self.video_path_label.config(text=file_path, fg="black")
    def close_app_and_continue(self):
        uploadTT()
    def submit(self):
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        hashtags = self.hashtags_text.get("1.0", tk.END).strip()

        if not title or not description or not hashtags or not self.video_path:
            messagebox.showerror("Eroare", "Toate câmpurile sunt obligatorii.")
            return

        data={
            "titlu": title,
            "descriere": description,
            "hashtags": hashtags,
            "path": self.video_path
        }
        # Aici poți salva datele într-un fișier sau le poți trimite mai departe
        with open("date_upload.json", "w", encoding="utf-8") as f:
            json.dump(data, f,ensure_ascii=False, indent=4)

        messagebox.showinfo("Succes", "Datele au fost preluate cu succes!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoUploaderApp(root)
    root.mainloop()

    app.close_app_and_continue()
