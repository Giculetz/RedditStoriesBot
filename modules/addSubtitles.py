import glob
import os
from moviepy import VideoFileClip, ImageClip, TextClip, ColorClip, CompositeVideoClip
from moviepy.video.VideoClip import VideoClip
import re
import numpy as np

def parse_srt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = re.findall(
        r'\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)',
        content, re.DOTALL)

    def time_to_sec(t):
        h, m, s = t.replace(',', '.').split(':')
        return float(h)*3600 + float(m)*60 + float(s)

    return [{
        'text': text.strip(),
        'start': time_to_sec(start),
        'end': time_to_sec(end)
    } for start, end, text in entries]

def overlay_subs_on_video(video_path, sub_path, output_path,
                          intro_image_path="reddit_post_screenshot.png",
                          intro_duration=3.0):

    # Parsează subtitrările
    data = parse_srt(sub_path)
    font_path = "C:\\Users\\savas\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Forque.ttf"
    font_size = 80

    video = VideoFileClip(video_path)
    W, H = video.size
    # Imaginea de început (fără efecte)
    intro = ImageClip(intro_image_path, transparent=True) \
        .with_duration(intro_duration) \
        .with_position("center")\
        .with_start(0)

    # Subtitrări direct în video
    subtitle_clips = []
    for entry in data:
        start = entry['start']  # decalare după intro
        duration = entry['end'] - entry['start']
        text = entry['text']

        txt_clip = TextClip(
            text=text,
            font=font_path,
            font_size=font_size,
            color='yellow',
            stroke_color='black',
            stroke_width=3,
            method='caption',
            size=(W, H)
        ).with_start(start).with_duration(duration).with_position('center')

        subtitle_clips.append(txt_clip)

    # Decalăm și video-ul principal să înceapă după intro

    # Combină totul
    final = CompositeVideoClip([ video] + subtitle_clips + [intro], size=video.size)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video.fps, preset='ultrafast')


# Rulează
def add_subtitles():
    from pushbullet import Pushbullet

    # pb = Pushbullet("o.mnLi8hGUluVC1yxkEWX6iP3Wi8QcP9f0")
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.dirname(cur_folder)
    folder_path = os.path.join(root_folder, 'temps', 'VideoWithSound')

    def extract_story_number(path):
        match = re.search(r'Story(\d+)', path)
        return int(match.group(1)) if match else float('inf')

    directories = sorted(
        [d for d in glob.glob(os.path.join(folder_path, "*/")) if os.path.isdir(d)],
        key=extract_story_number
    )
    cur_folder=os.path.dirname(os.path.abspath(__file__))
    parent_folder=os.path.dirname(cur_folder)
    file_path=os.path.join(parent_folder, 'output_folder.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        output_folder_path=f.read()

    def get_max_story_number(path):
        max_number = 0
        for name in os.listdir(path):
            match = re.match(r"Story(\d+)?(-postat)", name)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number
        return max_number

    start_index=get_max_story_number(output_folder_path)+1
    for index,dirg in enumerate(directories,start=1):
        os.makedirs(f'{output_folder_path}/Story{start_index}', exist_ok=True)
        cur_folder = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(cur_folder)
        folder_path = os.path.join(parent_folder, 'temps', 'VideoWithSound')
        files = glob.glob(f'{folder_path}\\Story{index}\\*.mp4')

        for i,file in enumerate(files,start=1):
            # print(f"Story {index} part {i} file {file} in dir {dirg}\n")
            sub_path=os.path.join(parent_folder, 'temps','Subtitles',f'Story{index}')
            sub_path=f'{sub_path}\\part_{i}.srt'
            image_path=os.path.join(parent_folder, 'temps','RedditImages',f'Story{index}.png')
            overlay_subs_on_video(
                file,
                sub_path,
                f'{output_folder_path}\\Story{start_index}\\part_{i}.mp4',
                image_path,
            )
            # pb.push_note("Fabrica de clipuri",f"Story {index} Part {i} is ready")
        start_index=start_index+1

