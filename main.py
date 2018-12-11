import time
import audioio
import board
import digitalio

SAMPLE_RATE = 22050
BIT_DEPTH = 16
VOICE_COUNT = 10

# list all samples here
samples = [audioio.WaveFile(open("C3.wav", "rb")),
           audioio.WaveFile(open("D3.wav", "rb")),
           audioio.WaveFile(open("E3.wav", "rb")),
           audioio.WaveFile(open("F3.wav", "rb")),
           audioio.WaveFile(open("G3.wav", "rb")),
           audioio.WaveFile(open("A3.wav", "rb")),
           audioio.WaveFile(open("B3.wav", "rb")),
           audioio.WaveFile(open("C4.wav", "rb")),
           audioio.WaveFile(open("D4.wav", "rb")),
           audioio.WaveFile(open("E4.wav", "rb"))]

# list all input buttons here
buttons = [digitalio.DigitalInOut(board.D13),
           digitalio.DigitalInOut(board.D12), 
           digitalio.DigitalInOut(board.D11),
           digitalio.DigitalInOut(board.D10),
           digitalio.DigitalInOut(board.D9),
           digitalio.DigitalInOut(board.D6),
           digitalio.DigitalInOut(board.D5),
           digitalio.DigitalInOut(board.SCL),
           digitalio.DigitalInOut(board.SDA),
           digitalio.DigitalInOut(board.A1)]
           
# initialize speaker output pin
audio_pin = audioio.AudioOut(board.A0)
   
# initialize all buttons in the list   
for i in buttons:
    i.switch_to_input(pull=digitalio.Pull.UP)

# test all buttons
print("Test Buttons")

for index, button in enumerate(buttons):
    print("Push Button " + str(index))
    while button.value:
        pass
    print(str(i))
    print("Button " + str(index) + " works.")
    
print("All buttons work.")

# create mixer object with the number of voices required
mixer = audioio.Mixer(voice_count=VOICE_COUNT,
                      sample_rate=SAMPLE_RATE,
                      channel_count=1,
                      bits_per_sample=BIT_DEPTH,
                      samples_signed=True)

# start outputing the mixer to the DAC
audio_pin.play(mixer)

was_released = []
for i in buttons:
    was_released.append(True)


# main body loop
# check buttons and play sample in mixer
while True:
    for index, button in enumerate(buttons):
        if not button.value and was_released[index]:
            was_released[index] = False
            mixer.play(samples[index], voice=index, loop=True)
            print("Playing sample " + str(index) + ".")
        elif button.value and not was_released[index]:
            was_released[index] = True
            mixer.stop_voice(voice=index)
        
    # debounce delay
    time.sleep(0.01)
    