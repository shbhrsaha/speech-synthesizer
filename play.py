"""
    Speaks a sentence based on the words recorded in wav files
"""

import pyaudio
import wave
import sys

CHUNK = 1024
p = pyaudio.PyAudio()

def say(sentence):
    total_data = ''

    for word in sentence.split(" "):
        wf = wave.open("%s.wav" % word, 'rb')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
        data = wf.readframes(CHUNK)
        
        while data != '':
            total_data += data
            data = wf.readframes(CHUNK)

    stream.write(total_data)
    stream.stop_stream()
    stream.close()


if __name__ == "__main__":
    say(sys.argv[1])