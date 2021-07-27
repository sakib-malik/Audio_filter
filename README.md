# Audio_filter (course project EE301A)

## Real time audio filtering with custom filters

1. Provide numerator and denominator coefficients for the transfer funtion of the filter H(z).
2. You can hear the filtered output simultaneously with the recording (at real time) or later on using the saved .wav file.
3. You can choose the amount of time for record and playback.
4. Make sure to place speaker away from mic to avoid reverbing of the voice or use earphones.
5. Can use Low pass , high pass, bandpass, bandstop filters according to the appropriate transfer function provided by the user.
6. Use play.py (to play a .wav file using it's filename)
7. Use record.py (to record voice into 'filename.wav' with a fixed amount of time)

## Information about different files:

### Play.py

This file just consists of a function “play_audio(filename)” which takes in some filename for ex: “input.wav” and plays the audio to the user.

### Record.py

This file just consists of a function “record_audio(time, filename)” which takes in some filename for ex: “output.wav” and time which is the recording time, and then it saves the recorded audio to the filename.

### util.py

This file contains two functions :
(a) dft_of_hz(zeros, poles, samples)
This function returns the value of DFT (discrete Fourier transform) from the provided “poles” and “zeros”, it first computes the DTFT and then takes it “samples” to compute the required DFT.
(b) apply_filter(b, a, x)
This function takes in the numerator coefficients “b”, denominator coefficients, “a” of the transfer function and also the input signal “x[n]”. It then computes
the Poles and zeros of this transfer function and then it computes the DFT of H(z)  dft_of_hz() and then it computes the DFT “x” and then computes the product of DFT{X} * DFT{H} and then takes the IDFT of this to compute Y[n]. And then it scales the output and returns it. This file also contains some example workings of this filter using coefficients from some lowpass, highpass filters, and their plots.

### Filter.py

This is the main workhorse algorithm, it takes in the coefficients of H(z) from the user, 
then whether to play the filtered audio along with input or just save it. And also the 
The time or recording. It then computes the filtered output using apply_filter() function
from util. It creates two streams, first stream is responsible to save the input voice to
“Input.wav” the second stream is responsible to save the filtered output 
To “output.wav” and also for playing it at real-time.

