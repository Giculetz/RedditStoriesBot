from pydub import AudioSegment
from pydub.effects import speedup
import os
import glob

def speedify():
    os.makedirs('../StoryVocalRapid', exist_ok=True)


    fisiere=glob.glob('StoryVocal/*.mp3')
    for index, file in enumerate(fisiere, start=1):
        print(file)
        audio = AudioSegment.from_file(f"{file}", format="mp3")

        # Mărește viteza de redare (ex: 1.5x mai rapid)
        audio_fast = speedup(audio, playback_speed=1.2)

        # # Salvează rezultatul
        audio_fast.export(f"StoryVocalRapid/story{index}.mp3", format="mp3")
