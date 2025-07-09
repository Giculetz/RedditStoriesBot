import glob
import re

import ffmpeg
import os

def bg_adder_clip(input_video_path, output_video_path, start_ms, end_ms, new_audio_path):
    # Creează directoarele pentru output dacă nu există
    output_dir = os.path.dirname(output_video_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_s = start_ms / 1000
    duration_s = (end_ms - start_ms) / 1000

    # Obține info video
    probe = ffmpeg.probe(input_video_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])

    # Raportul 9:16
    target_ratio = 9 / 16

    # Calculează crop centrat cu ratio 9:16
    if (width / height) > target_ratio:
        # Video mai lat decât 9:16, cropează lățimea
        crop_height = height
        crop_width = int(height * target_ratio)
    else:
        # Video mai înalt sau egal, cropează înălțimea
        crop_width = width
        crop_height = int(width / target_ratio)

    x = int((width - crop_width) / 2)
    y = int((height - crop_height) / 2)

    # 1. Taie + crop + scale la 1080x1920, salvează temporar
    ffmpeg.input(input_video_path, ss=start_s, t=duration_s) \
        .crop(x, y, crop_width, crop_height) \
        .filter('scale', 1080, 1920) \
        .output('temp_video.mp4', vcodec='libx264', acodec='aac', strict='experimental') \
        .run(overwrite_output=True)

    # 2. Taie audio nou la durata clipului
    ffmpeg.input(new_audio_path, ss=0, t=duration_s) \
        .output('temp_audio.aac', acodec='aac', strict='experimental') \
        .run(overwrite_output=True)

    # 3. Combină video și audio, păstrând codec copy pentru video, audio nou
    video_input = ffmpeg.input('temp_video.mp4')
    audio_input = ffmpeg.input('temp_audio.aac')
    ffmpeg.output(video_input,audio_input,output_video_path, vcodec='copy', acodec='aac', strict='experimental', shortest=None) \
        .run(overwrite_output=True)

    # Șterge fișiere temporare dacă vrei
    os.remove('temp_video.mp4')
    os.remove('temp_audio.aac')


def bg_adder():
    os.makedirs('../VideoWithSound', exist_ok=True)
    video_path= '../BgVideo/clip.mp4'
    folder_path = '../StoryParts'
    start=1000
    dur=60*1000

    def extract_story_number(path):
        match = re.search(r'Story(\d+)', path)
        return int(match.group(1)) if match else float('inf')

    directories = sorted(
        [d for d in glob.glob(os.path.join(folder_path, "*/")) if os.path.isdir(d)],
        key=extract_story_number
    )
    for index,dir in enumerate(directories,start=1):
        os.makedirs(f'VideoWithSound/Story{index}',exist_ok=True)
        files = glob.glob(os.path.join(dir, "*.mp3"))
        for i,file in enumerate(files,start=1):
            bg_adder_clip(
                video_path,
                f'VideoWithSound/Story{index}/part_{i}.mp4',
                start,
                start+dur,
                file
            )
            start = start + dur
    # bg_adder_clip(video_path,'VideoWithSound/clip.mp4',1000,60*1000,'StoryParts/Story1/part_1.mp3')
