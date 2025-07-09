import os
from google.cloud import speech
import io
import modules.mp3ToWav as mp
import modules.keyFinder as keyFinder
import glob


def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def merge_words(words_with_times, min_duration=0.3):
    merged = []
    buffer = []

    for word, start, end in words_with_times:
        duration = end - start
        if duration < min_duration:
            buffer.append((word, start, end))
        else:
            if buffer:
                merged_word = " ".join([w for w, _, _ in buffer])
                merged_start = buffer[0][1]
                merged_end = buffer[-1][2]
                merged.append((merged_word, merged_start, merged_end))
                buffer = []
            merged.append((word, start, end))

    if buffer:
        merged_word = " ".join([w for w, _, _ in buffer])
        merged_start = buffer[0][1]
        merged_end = buffer[-1][2]
        merged.append((merged_word, merged_start, merged_end))

    return merged

def generate_srt_from_words(words_with_times, srt_path):
    # Apelăm direct unificarea
    merged_words = merge_words(words_with_times, min_duration=0.3)
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (word, start, end) in enumerate(merged_words, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(start)} --> {format_srt_time(end)}\n")
            f.write(f"{word}\n\n")

def transcribe_with_word_time_offsets(speech_file_mp3):
    path = keyFinder.cauta_cel_mai_recent_fisier("F:\\CloudKey\\", "zinc-", "json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
    client = speech.SpeechClient()
    mp.mp3_to_wav(speech_file_mp3, 'temp.wav')
    speech_file = 'temp.wav'
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            results.append((word, start_time, end_time))

    os.remove('temp.wav')

    return results

def get_subtitles():
    os.makedirs('../Subtitles', exist_ok=True)
    folder_path = '../StoryParts'
    directories = [d for d in glob.glob(os.path.join(folder_path, "*/")) if os.path.isdir(d)]
    for i, dir in enumerate(directories, start=1):
        os.makedirs(f'Subtitles/Story{i}', exist_ok=True)
        files = glob.glob(os.path.join(dir, "*.mp3"))
        for file_index, file in enumerate(files, start=1):
            words_with_times = transcribe_with_word_time_offsets(file)
            generate_srt_from_words(words_with_times, f'Subtitles/Story{i}/part_{file_index}.srt')
