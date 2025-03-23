# This method reads out everything line by line

# 1st method which reads out everything line by line word by word that are not fast

import os
import time
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer

# Load the API key from the environment
client = Neuphonic(api_key='fe4408d269a6f1de662dde8c0967183c112f426e6a1e01b6502e65a194ba392e.2dbc8286-798a-4e7b-bd0f-11f8933dd5b5')

sse = client.tts.SSEClient()

# TTSConfig is a pydantic model so check out the source code for all valid options
tts_config = TTSConfig(
    speed=1,
    lang_code='en', # replace the lang_code with the desired language code.
    voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'  # use client.voices.list() to view all available voices
)

def speak_line_by_line():
    print("Type your rap lines. Press enter when you are done.\n")
    lines = []
    while len(lines) < 4:
        line = input(">")
        # If line is empty case
        if line.strip() == "":
            break
        # If not then add to the lines list
        lines.append(line)
        print(len(lines))

    # Create an audio player with `pyaudio`
    with AudioPlayer() as player:
        for i in range(len(lines)):
            current_line = lines[i]
            print(f"Line {i + 1}: {current_line}")
            response = sse.send(current_line, tts_config=tts_config)
            player.play(response)
            time.sleep(0.01) # to make a pause between lines
        player.save_audio('output.wav')  # save the audio to a .wav file
    
def main():
    speak_line_by_line()

if __name__ == '__main__':
    main()


# 1st method which reads out everything line by line word by word that are not fast

##import os
##import time
##from pyneuphonic import Neuphonic, TTSConfig
##from pyneuphonic.player import AudioPlayer
##
### Load the API key from the environment
##client = Neuphonic(api_key='fe4408d269a6f1de662dde8c0967183c112f426e6a1e01b6502e65a194ba392e.2dbc8286-798a-4e7b-bd0f-11f8933dd5b5')
##
##sse = client.tts.SSEClient()
##
### TTSConfig is a pydantic model so check out the source code for all valid options
##tts_config = TTSConfig(
##    speed=1,
##    lang_code='en', # replace the lang_code with the desired language code.
##    voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'  # use client.voices.list() to view all available voices
##)
##
##def speak_line_by_line_word_by_word():
##    print("Type your rap lines. Press enter when you are done.\n")
##    lines = []
##    while len(lines) < 4:
##        line = input(">")
##        # If line is empty case
##        if line.strip() == "":
##            break
##        # If not then add to the lines list
##        lines.append(line)
##        print(len(lines))
##
##    # Create an audio player with `pyaudio`
##    with AudioPlayer() as player:
##        for i in range(len(lines)):
##            current_line = lines[i]
##            print(f"Line {i + 1}: {current_line}")
##
##            words = current_line.strip().split()
##            for word in words:
##                print(f" Speaking word: {word}")
##                response = sse.send(word, tts_config=tts_config)
##                player.play(response)
##            #time.sleep(1.0) # to make a pause between lines
##        player.save_audio('output.wav')  # save the audio to a .wav file
##    
##def main():
##    speak_line_by_line_word_by_word()
##
##if __name__ == '__main__':
##    main()

# 2nd method which reads out everything line by line word by word but in 2 other ways that are not fast as well

##import os
##import time
##import io
##from concurrent.futures import ThreadPoolExecutor
##from pyneuphonic import Neuphonic, TTSConfig
##from pyneuphonic.player import AudioPlayer
##from pydub import AudioSegment
##from pydub.playback import play  # for playing concatenated audio
##
### Load API key from environment (or directly set it)
##client = Neuphonic(api_key='fe4408d269a6f1de662dde8c0967183c112f426e6a1e01b6502e65a194ba392e.2dbc8286-798a-4e7b-bd0f-11f8933dd5b5')
##sse = client.tts.SSEClient()
##
### Define TTS configuration (adjust voice_id, speed, etc., as desired)
##tts_config = TTSConfig(
##    speed=1.0,
##    lang_code='en',
##    voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'
##)
##
### -----------------------------
### Method 1: Pre-fetch Audio Concurrently
### -----------------------------
##def fetch_word_audio(word):
##    """Fetch TTS audio for a single word."""
##    return sse.send(word, tts_config=tts_config)
##
##def speak_words_concurrently(text):
##    """Speak each word with minimal pause by pre-fetching all TTS audio concurrently."""
##    words = text.strip().split()
##    responses = []
##
##    # Use ThreadPoolExecutor to fetch audio concurrently
##    with ThreadPoolExecutor() as executor:
##        futures = [executor.submit(fetch_word_audio, word) for word in words]
##        # Retrieve responses in the same order as words
##        for future in futures:
##            responses.append(future.result())
##
##    with AudioPlayer() as player:
##        for word, response in zip(words, responses):
##            print(f"Speaking: {word}")
##            player.play(response)
##            # Optionally, use a very short sleep if needed:
##            time.sleep(0.1)  # Adjust this if necessary
##
### -----------------------------
### Method 2: Concatenating Audio Segments
### -----------------------------
##def speak_words_concatenated(text):
##    """Concatenate the TTS audio for each word and play as a single stream."""
##    words = text.strip().split()
##    segments = []
##
##    for word in words:
##        print(f"Fetching audio for: {word}")
##        response = sse.send(word, tts_config=tts_config)
##        # Assuming response is a WAV file in bytes; load it with pydub
##        segment = AudioSegment.from_file(io.BytesIO(response), format="wav")
##        segments.append(segment)
##    
##    # Concatenate all audio segments
##    if segments:
##        combined = segments[0]
##        for segment in segments[1:]:
##            combined += segment
##        print("Playing concatenated audio...")
##        play(combined)  # This will play the whole combined audio stream
##        # Optionally, save to a file
##        combined.export("combined_output.wav", format="wav")
##    else:
##        print("No words to play.")
##
### -----------------------------
### Main function to choose a method
### -----------------------------
##def main():
##    text = input("Enter a phrase for TTS: ")
##    print("\nChoose playback method:")
##    print("1. Pre-fetch words concurrently (play each word individually)")
##    print("2. Concatenate audio (smooth, continuous playback)")
##    choice = input("Enter 1 or 2: ").strip()
##
##    if choice == "1":
##        speak_words_concurrently(text)
##    elif choice == "2":
##        speak_words_concatenated(text)
##    else:
##        print("Invalid choice.")
##
##if __name__ == "__main__":
##    main()
