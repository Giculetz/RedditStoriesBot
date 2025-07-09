import json
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox

import os
import pyautogui as au
import time


def uploadYT():
    webbrowser.open_new_tab('https://studio.youtube.com/channel/UCTkPmvy4bIQNKrDX0OEfgdw/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D')
    au.PAUSE = 1
    target='targets/uploadYT.png'
    time.sleep(5)
    try:
        location=au.locateCenterOnScreen(target,confidence=0.8)
        au.click(location)
        target = 'targets/uploadChrome.png'
        location = au.locateCenterOnScreen(target, confidence=0.8)
        new_x = location.x + 400
        new_y = location.y + 30
        au.click(new_x, new_y)
    except Exception as e:
        print(e)
    with open('date_upload.json', 'r') as f:
        data = json.load(f)
    path = os.path.dirname(data['path'])
    au.write(path)
    au.press('enter')
    au.press('tab', presses=5)
    fisier = os.path.basename(data['path'])
    au.write(fisier)
    au.press('enter')
    time.sleep(5)
    au.hotkey('ctrl','a')
    au.press('backspace')
    #titlu
    cuvinte = data['hashtags'].split()  # separă cuvintele după spațiu

    hashtaguri = ""
    for cuvant in cuvinte:
        hashtaguri += f"#{cuvant} "
    titlu = f"{data['titlu']} {hashtaguri}"
    descriere = f"{data['descriere']} {hashtaguri}"
    au.write(titlu,interval=0.05)
    au.press('tab',presses=8)
    au.write(descriere,interval=0.05)
    au.press('tab',presses=5)
    au.press('down')
    au.press('tab',presses=2)
    au.press('enter')
    au.press('tab',presses=13)
    for cuvant in cuvinte:
        au.write(cuvant)
        au.press('enter')
    au.press('tab',presses=22)
    au.press('enter')
    au.press('tab',presses=6)
    au.press('enter')
    au.press('tab',presses=6)
    au.press('enter')
    au.press('tab')
    au.press('down',presses=2)
    au.press('tab',presses=12)
    au.press('enter')

    print("S-a postat pe youtube")
    time.sleep(5)

def uploadInsta():
    webbrowser.open_new_tab('https://www.instagram.com/')
    au.PAUSE = 1
    target='targets/uploadInsta.png'
    time.sleep(5)
    try:
        location=au.locateCenterOnScreen(target,confidence=0.8)
        au.click(location)
        time.sleep(0.5)
        target='targets/uploadInsta2.png'
        location=au.locateCenterOnScreen(target,confidence=0.8)
        au.click(location)
        time.sleep(0.5)
        target = 'targets/uploadChrome.png'
        location = au.locateCenterOnScreen(target, confidence=0.8)
        new_x = location.x + 400
        new_y = location.y + 30
        au.click(new_x, new_y)
    except Exception as e:
        print(e)

    with open('date_upload.json', 'r') as f:
        data = json.load(f)
    path = os.path.dirname(data['path'])
    au.write(path)
    au.press('enter')
    au.press('tab', presses=5)
    fisier = os.path.basename(data['path'])
    au.write(fisier)
    au.press('enter')
    time.sleep(4)
    au.press('tab', presses=3)
    au.press('enter')
    au.press('tab', presses=7)
    au.press('enter')
    au.press('tab', presses=6)
    au.press('enter')
    au.press('tab', presses=2)
    au.press('enter')
    au.press('tab', presses=4)
    #descrierea insta
    cuvinte = data['hashtags'].split()  # separă cuvintele după spațiu

    hashtaguri = ""
    for cuvant in cuvinte:
        hashtaguri += f"#{cuvant} "
    descriere = f"{data['descriere']} {hashtaguri}"
    au.write(descriere, interval=0.05)

    au.press('tab', presses=7)
    au.press('enter')

    print("S-a postat pe INSTA")
    time.sleep(5)

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
    au.press('tab')
    au.hotkey('ctrl','a')
    au.press('backspace')
    #ne aflam in descriere la tt

    cuvinte = data['hashtags'].split()  # separă cuvintele după spațiu

    hashtaguri = ""
    for cuvant in cuvinte:
        hashtaguri += f"#{cuvant} "
    descriere=f"{data['descriere']} {hashtaguri}"
    au.write(descriere,interval=0.05)
    time.sleep(4)
    au.press('escape')
    au.press('tab')
    au.press('end')
    target='targets/TTpost.png'
    try:
        location=au.locateCenterOnScreen(target,confidence=0.8)
        # au.moveTo(location)
        au.click(location)
    except Exception as e:
        print(e)
    print("S-a postat pe tiktok")
    time.sleep(5)


class VideoUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Uploader de videoclipuri")

        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack()
        self.submited=False
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
        if self.submited:
            uploadTT()
            uploadInsta()
            uploadYT()
    def submit(self):
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        hashtags = self.hashtags_text.get("1.0", tk.END).strip()
        ok=False
        cuvinte=hashtags.split()
        hashtaguri=""
        for cuvant in cuvinte:
            hashtaguri += f"#{cuvant} "
        verificare=f'{title} {hashtaguri}'
        if len(verificare)>100:
            ok=True

        if not title or not description or not hashtags or not self.video_path or ok:
            if ok:
                messagebox.showerror("Eroare", f"Titlul si hashtagurile au in total mai mult de 100 de caractere\nAu chiar {len(verificare)} caractere")
            else:
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
        self.submited = True
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoUploaderApp(root)
    root.mainloop()

    app.close_app_and_continue()
