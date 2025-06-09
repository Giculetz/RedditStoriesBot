import json
from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\proiecte\\key google cloud\\zinc-fusion-462016-k0-99a7b6673590.json"
client = texttospeech.TextToSpeechClient()
os.makedirs("StoryVocal", exist_ok=True)
voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Wavenet-D',
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.3
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

    with open(f'StoryVocal/story{index}.mp3', 'wb') as outfile:
        outfile.write(response.audio_content)

    print('Done')
