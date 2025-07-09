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
    os.makedirs('../VideoFinal', exist_ok=True)
    folder_path = '../VideoWithSound'

    def extract_story_number(path):
        match = re.search(r'Story(\d+)', path)
        return int(match.group(1)) if match else float('inf')

    directories = sorted(
        [d for d in glob.glob(os.path.join(folder_path, "*/")) if os.path.isdir(d)],
        key=extract_story_number
    )
    for index,dirg in enumerate(directories,start=1):
        os.makedirs(f'VideoFinal/Story{index}', exist_ok=True)
        files = glob.glob(f'VideoWithSound/Story{index}/*.mp4')

        for i,file in enumerate(files,start=1):
            # print(f"Story {index} part {i} file {file} in dir {dirg}\n")

            overlay_subs_on_video(
                f'VideoWithSound/Story{index}/part_{i}.mp4',
                f'Subtitles/Story{index}/part_{i}.srt',
                f'VideoFinal/Story{index}/part_{i}.mp4',
                f'RedditPostImage/Images/Story{index}.png'
            )
            # pb.push_note("Fabrica de clipuri",f"Story {index} Part {i} is ready")
