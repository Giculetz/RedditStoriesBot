import json
from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs

def speechify2():
    load_dotenv()

    client = ElevenLabs(api_key="sk_bfa09d5be1708476259523f9b185913f70622db5af1069c2")

    os.makedirs("temps/StoryVocal", exist_ok=True)

    with open('F:\\RedditStoriesBot\\stories.json', 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    for index, text in enumerate(data, start=1):
        print(f'Processing {index} of {len(data)}')
        audio = client.text_to_speech.convert(
            text=text['title'] + " " + text['content'],
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        with open(f'temps/StoryVocal/story{index}.mp3', 'wb') as outfile:
            for chunk in audio:
                outfile.write(chunk)
        print('Done')

