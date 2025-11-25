from pydub import AudioSegment
from pydub.effects import speedup
import os
import glob

def speedify():
    os.makedirs('temps/StoryVocalRapid', exist_ok=True)


    fisiere=glob.glob('temps/StoryVocal/*.mp3')
    for index, file in enumerate(fisiere, start=1):
        print(file)
        audio = AudioSegment.from_file(f"{file}", format="mp3")

        # Mărește viteza de redare (ex: 1.5x mai rapid)
        audio_fast = speedup(audio, playback_speed=1.2)

        # # Salvează rezultatul
        audio_fast.export(f"temps/StoryVocalRapid/story{index}.mp3", format="mp3")
