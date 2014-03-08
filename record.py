"""
    Simplifies recording of word .wav files
"""

import sys
import pyaudio
import wave
import audioop

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
THRESHOLD_MULTIPLIER = 6
THRESHOLD_TIME = 3

audio = pyaudio.PyAudio()

def getScore(data):
    rms = audioop.rms(data, 2)
    score = rms / 3
    return score

def activeRecord(output_filename):
    """
        Starts recording at loud sound and stops recording when loud sound ends
    """

    # prepare recording stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    # stores the audio data
    frames = []

    # stores the lastN score values
    lastN = [i for i in range(30)]

    # calculate the long run average, and thereby the proper threshold
    for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

        data = stream.read(CHUNK)
        frames.append(data)

        # save this data point as a score
        lastN.pop(0)
        lastN.append(getScore(data))
        average = sum(lastN) / len(lastN)

    # this will be the benchmark to cause a disturbance over!
    THRESHOLD = average * THRESHOLD_MULTIPLIER

    # save some memory for sound data
    frames = []

    # flag raised when sound disturbance detected
    didDetect = False

    # start passively listening for disturbance above threshold
    score = 0
    print "READY TO RECORD %s" % output_filename
    while score < THRESHOLD:

        data = stream.read(CHUNK)
        frames.append(data)
        score = getScore(data)

    loud_start = len(frames)
    
    # continue recording until drop in sound level
    lastN = [THRESHOLD * THRESHOLD_MULTIPLIER for i in range(30)]
    average = sum(lastN) / float(len(lastN))

    while average > THRESHOLD*0.7:

        data = stream.read(CHUNK)
        frames.append(data)
        score = getScore(data)

        lastN.pop(0)
        lastN.append(score)

        average = sum(lastN) / float(len(lastN))

    print "DONE"

    # save the audio data
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames[loud_start-2:-35]))
    wf.close()

if __name__ == "__main__":

    sentence = sys.argv[1]
    
    for word in sentence.split(" "):
        activeRecord("%s.wav" % word)
    