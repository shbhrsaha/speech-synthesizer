speech-synthesizer
==================

A naive speech synthesis engine for text-to-speech

Workflow
--------
PortAudio and PyAudio are required.

Build a vocabulary by recording words with record.py:

    python record.py "this is the sentence I would like to record"

The script will iterate over the words in the sentence and ask you to speak the word into your microphone. The recording for each word will be saved in the same directory.

Play back a sentence with play.py:

    python play.py "I would like this sentence"

Words included in the sentence argument should have been recorded already in the previous step.