import re

from pydub import AudioSegment
import os
import glob

def partify(input_folder):
    os.makedirs('../StoryParts', exist_ok=True)

    def extract_number(filename):
        match = re.search(r'(\d+)', os.path.basename(filename))
        return int(match.group(1)) if match else 0

    fisiere = sorted(glob.glob(f'{input_folder}/*.mp3'), key=extract_number)
    durata_parte=50*1000 #ms

    for index,file in enumerate(fisiere,start=1):
        print(file)
        audio = AudioSegment.from_mp3(f"{file}")
        os.makedirs(f'StoryParts/Story{index}',exist_ok=True)
        total_length=len(audio)
        nr_parti=(total_length+durata_parte-1)//durata_parte
        for i in range (nr_parti):
            # print(f' Story {index} part {i} din fisieru {file}')
            start=i*durata_parte
            end = min(start+durata_parte, total_length)
            if i>0:
                start-=10*1000 #ms
                if i<nr_parti-1:
                    end-=10*1000

            parte = audio[start:end]
            parte.export(f"StoryParts/Story{index}/part_{i+1}.mp3", format="mp3")
            print(f"S-a creat partea {i+1} din story ul {index}")

