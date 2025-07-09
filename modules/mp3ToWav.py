from pydub import AudioSegment

def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    print(f"Converted {mp3_path} to {wav_path}")
