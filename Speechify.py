import json
from google.cloud import texttospeech

import os

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\savas\\OneDrive\\Documents\\proiecte\\Reddit Stories\\zinc-fusion-462016-k0-2e5c8e74f15d.json"

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Wavenet-A',
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.3
)
with open('stories.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

for index,text in enumerate(data,start=1):
    print(f'Processing {index} of {len(data)}')
    text_input = texttospeech.SynthesisInput(text=text['title']+text['content'])
    response = client.synthesize_speech(input=text_input, voice=voice,audio_config= audio_config)
    with open(f'StoryVocal/story{index}.mp3', 'wb') as outfile:
        outfile.write(response.audio_content)
    print('Done')

