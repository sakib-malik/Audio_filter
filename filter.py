import pyaudio
import wave
import numpy as np
import util


def get_transfer_function():
    # Ask the user for LCCDE coefficients
    numerator = list(map(float, input("Please Enter Numerator Coefficients for H(z) : \n").split()))
    denominator = list(map(float, input("Please Enter Denominator Coefficients for H(z) : \n").split()))

    num = np.array(numerator).astype(np.float32)
    deno = np.array(denominator).astype(np.float32)
    return num, deno


b, a = get_transfer_function() # LCCDE Coefficients

save = input("Do you wanna just save the audio instead of playing immediately (y/n) ? : ")

time = input("Please provide time for the recording : ")

############### INITIALIZE I/O Streams ######################
#############################################################


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = int(RATE/20)
RECORD_SECONDS = int(time)
WAVE_INPUT_FILENAME = "input.wav"
WAVE_OUTPUT_FILENAME = "output.wav"

p1 = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()

stream1 = p1.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

stream2 = p2.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  output=True)

#############################################################


########################### MAIN LOOP ####################################

print("* Recording started ...\n")

input_frames = []
output_frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):      # For number of chunks

    input_data = stream1.read(CHUNK)    # FROM INPUT STREAM
    X_chunk = np.frombuffer(input_data, np.int16)
    Y_chunk = util.apply_filter(b, a, X_chunk).astype(X_chunk.dtype)
    Y_bytes = bytes(Y_chunk)
    if save == 'n':
        stream2.write(Y_bytes)          # TO OUTPUT STREAM
    input_frames.append(input_data)     # INPUT  FILE
    output_frames.append(Y_bytes)       # OUTPUT FILE

print("* Recording Done...\n")

#########################################################################

# CLOSE I/O  Streams

stream1.stop_stream()
stream1.close()
p1.terminate()
stream2.stop_stream()
stream2.close()
p2.terminate()

# SAVE I/O FILES

# SAVE INPUT FILE TO "input.wav"

wf = wave.open(WAVE_INPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p1.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(input_frames))
wf.close()

# SAVE OUTPUT FILE TO "output.wav"

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p2.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(output_frames))
wf.close()
