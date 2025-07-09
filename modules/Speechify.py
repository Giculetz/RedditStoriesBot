import json
from google.cloud import texttospeech
import os
import modules.keyFinder as keyFinder

def speechify():
    path= keyFinder.cauta_cel_mai_recent_fisier("F:\\CloudKey\\", "zinc-", "json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
    client = texttospeech.TextToSpeechClient()

    os.makedirs("temps/StoryVocal", exist_ok=True)
    os.makedirs("temps/Subtitles", exist_ok=True)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-B',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.5
    )

    with open('stories.json', 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    for index, text in enumerate(data, start=1):
        print(f'Processing {index} of {len(data)}')
        text_input = texttospeech.SynthesisInput(text=text['title'] + " " + text['content'])

        response = client.synthesize_speech(
            input=text_input,
            voice=voice,
            audio_config=audio_config
        )

        with open(f'temps/StoryVocal/story{index}.mp3', 'wb') as outfile:
            outfile.write(response.audio_content)

        print('Done')

