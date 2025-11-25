import os
import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy import VideoFileClip
from PIL import Image, ImageTk
from pushbullet import Pushbullet

from modules.GetSubtitles import get_subtitles
from modules.storyGetter import story_getter
from modules.Speechify import speechify
from modules.Speechify2 import speechify2
from modules.Partify import partify
from modules.BgAdder import bg_adder
from modules.Speedify import speedify
from modules.ssGetter import ss_getter
from modules.addSubtitles import add_subtitles
import modules.deleter as deleter

OUTPUT_PATH_FILE = "F:\\RedditStoriesBot\\output_folder.txt"
BG_FOLDER_PATH="F:\\RedditStoriesBot\\BgVideo"
bg_path="F:\\RedditStoriesBot\\BgVideo\\clip.mp4"
def get_thumbnail(video_path, time=18):
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(time)  # frame la secunda 1
        image = Image.fromarray(frame)
        image.thumbnail((160, 90))  # resize pt afișare
        return image
    except Exception as e:
        print(f"Eroare la {video_path}: {e}")
        return None

def select_video(clip_path):
    global bg_path
    bg_path=clip_path
    path.set(os.path.basename(bg_path))



def check_output_folder():
    if not os.path.exists(OUTPUT_PATH_FILE) or os.path.getsize(OUTPUT_PATH_FILE) == 0:
        folder = filedialog.askdirectory(title="Selectează folderul de output")
        if folder:
            with open(OUTPUT_PATH_FILE, "w", encoding="utf-8") as f:
                f.write(folder)
        else:
            messagebox.showerror("Eroare", "Trebuie să selectezi un folder!")
            return False
    return True

def text_saver(nr_povesti):
    def get_max_story_number(path):
        max_number = 0
        for name in os.listdir(path):
            match = re.match(r"Story(\d+)", name)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number
        return max_number

    with open('stories.json', 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    for index, story in enumerate(data, start=get_max_story_number(get_output_folder())-nr_povesti+1):
        output_path = get_output_folder()
        os.makedirs(f'{output_path}/Story{index}', exist_ok=True)
        with open(f'{output_path}/Story{index}/story{index}.txt', 'w', encoding='utf-8') as f:
            f.write("TITLE:"+story['title'] + "\n")
            f.write("CONTENT:\n"+story['content'])

def get_output_folder():
    with open(OUTPUT_PATH_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def run_pipeline(num_clips, subreddit_index,bg_video_path,eleven):
    pb = Pushbullet("o.uhvrEttwLRN1Mzf80nW0l9hc7w0ltiPj")
    progres="inceput"
    try:
        os.makedirs('temps', exist_ok=True)
        pb.push_note("Fabrica de clipuri", "A inceput fabrica de clipuri")
        progres="story getter"
        print(f"Se procura {num_clips} povesti din subreddit {subreddit_index}")
        story_getter(num_clips, subreddit_index)
        print("Hai sa facem si vocile pentru povestile astea")

        if eleven:
            progres = "speechify 2"
            speechify2()
            progres="speedify"
            print("Tre sa le grabim putin")
            speedify()
            print("Si acum sa le impartim")
            progres="partify"
            partify("temps/StoryVocalRapid")
        else:
            progres = "speechify"
            speechify()
            progres = "partify"
            print("Si acum sa le impartim")
            partify("temps/StoryVocal")
        print("Daca tot le am impartit, le facem si subtitrari")
        progres="get subtitles"
        get_subtitles(eleven)
        print("Facem o poza pentru fiecare postare si sanatate")
        progres = "ss getter"
        ss_getter()
        print("Adaugam sunetul pe fundal")
        progres = "bg adder"
        bg_adder(bg_video_path)
        pb.push_note("Fabrica de clipuri", "S-au facut clipurile fara subtitrari")
        print("Acum avem de toate, ai de stat vreo 10 min per clip sa se faca")
        progres = "add subtitles"
        add_subtitles()
        text_saver(nr_povesti=num_clips)
        deleter.delete_temps()
        pb.push_note("Fabrica de clipuri", f"S-au terminat {num_clips} clipuri cu succes!")
        messagebox.showinfo("Succes", f"Au fost generate {num_clips} clipuri!")
    except Exception as e:
        pb.push_note("Eroare", f"Eroare la fabrica: {e}\nS-a ajuns la {progres}")
        deleter.delete_temps()
        messagebox.showerror("Eroare", f"Eroare la procesare: {e}")

def start_factory():
    if not check_output_folder():
        return

    try:
        num_clips = int(entry_num_clips.get())
        subreddit_index = subreddit_combo.current()
        messagebox.showinfo("Fabrica de clipuri",f"Incepe crearea a {num_clips} clipuri cu clip de fundal din {bg_path}")
        global is_eleven
        eleven=is_eleven.get()
        if subreddit_index == -1:
            raise ValueError("Alege un subreddit din listă.")


        run_pipeline(num_clips, subreddit_index,bg_path,eleven)

    except ValueError as ve:
        messagebox.showerror("Eroare", f"Valoare invalidă: {ve}")

# === INTERFATA GRAFICA ===
root = tk.Tk()
root.title("Fabrica de Clipuri")

tk.Label(root, text="Câte clipuri vrei să faci?", font=("Arial", 12)).pack(pady=10)
entry_num_clips = tk.Entry(root, font=("Arial", 12))
entry_num_clips.pack()

tk.Label(root, text="Alege subreddit:", font=("Arial", 12)).pack(pady=10)
subreddit_combo = ttk.Combobox(root, font=("Arial", 12), state="readonly")
subreddit_combo["values"] = ["stories", "Am I the Asshole", "nosleep (horror)", "Today I Fucked Up"]
subreddit_combo.pack()
is_eleven=tk.BooleanVar()
checkbox=tk.Checkbutton(root,text="Folosesti ElevenLabs pentru voce?", variable=is_eleven)
checkbox.pack()

tk.Label(root,text="Alege un clip de background: ", font=("Arial", 12)).pack(pady=10)


path=tk.StringVar()
path.set(os.path.basename(bg_path))
tk.Label(root, text="Clip selectat:", font=("Arial", 12)).pack(pady=5)
tk.Label(root,textvariable=path, font=("Arial", 12)).pack(pady=2)
frame=tk.Frame(root)
frame.pack()
thumbnails=[]
row=0
column = 0
for file in os.listdir(BG_FOLDER_PATH):
    if file.endswith(".mp4"):
        full_path = os.path.join(BG_FOLDER_PATH, file)
        thumb = get_thumbnail(full_path)
        if thumb:
            tk_img = ImageTk.PhotoImage(thumb)
            thumbnails.append(tk_img)  # reținem imaginea

            btn = tk.Button(frame, image=tk_img, command=lambda p=full_path:select_video(p))
            btn.grid(row=row, column=column, padx=5, pady=5)

            column += 1
            if column == 2:  # 4 pe rând
                column = 0
                row += 1

tk.Button(root, text="Pornește fabrica", font=("Arial", 12), command=start_factory).pack(pady=20)

root.update_idletasks()
root.geometry("")

root.mainloop()
