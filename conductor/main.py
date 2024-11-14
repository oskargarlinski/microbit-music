import microbit
import music
import radio
import utime

# Creating the music data variable that hold the transcribed music data.
music_data = {
    1: {1: ['D4:6', 'D4:3', 'D4:6', 'D4:3']},
    2: {1: ['D4:6', 'D4:3', 'D4:3', 'D4:3', 'D4:3']},
    3: {1: ['D4:6', 'D4:3', 'D4:6', 'D4:3']},
    4: {1: ['D4:6', 'D4:3', 'D4:3', 'D4:3', 'D4:3']},
    5: {
        1: ['D4:6', 'D4:3', 'D4:6', 'D4:3'],
        2: ['D0:18'],
        3: ['D-1:18']
    },
    6: {
        1: ['D4:6', 'D4:3', 'D4:3', 'A3:3', 'C4:3'],
        2: ['D0:9', 'D0:9'],
        3: ['D0:9', 'D-1:9']
    }
}

# Setting music tempo (69 bpm at dotted half notes, would roughly equate to 207bpm with this config based on 6/8 time sig)
ticks = 6
bpm = 207
music.set_tempo(ticks=ticks, bpm=bpm)

# Turn radio on
radio.on()

# Set radio message limit to have a length limit of 200 bytes instead of standard 32 bytes
radio.config(length=200)

synced_microbits = set()
total_slaves = 2  # Total number of slave microbits expected
start_time_sent = False


# Start sending tempo timing to the receivers, ensure that there's enough time for them to process it.
def setup_receiver_tempo():
    # Send tempo timing, wait between each transmission to make sure that there is enough time for the receivers to process this data.
    radio.send("TICKS:{}".format(ticks))
    microbit.sleep(400)
    radio.send("BPM:{}".format(bpm))
    microbit.sleep(400)
    microbit.display.show(microbit.Image.YES)
    microbit.sleep(1000)
    microbit.display.show(microbit.Image.ALL_CLOCKS, loop=True, delay=100, wait=False)


# Start sending music data to the receivers, ensure that there's enough time for them to process it.
def setup_receiver_notes():
    # Iterate over each bar in a sorted order to ensure messages are sent in order
    for bar_number in sorted(music_data.keys()):
        microbit_data = music_data[bar_number]
        for microbit_id, notes in microbit_data.items():
            # Convert the list of notes to a string format
            notes_str = ','.join(notes)
            # Format the message to include the bar number, microbit ID, and notes
            message = "NOTES:{}:{}:{}".format(bar_number, microbit_id, notes_str)
            # Send the message with a delay for processing time
            radio.send(message)
            microbit.sleep(100)

    microbit.display.show(microbit.Image.HEART)
    microbit.sleep(1000)
    microbit.display.show(microbit.Image.ALL_CLOCKS, loop=True, delay=100, wait=False)


def send_play_signal():
    radio.send("PLAY")
    microbit.display.show(microbit.Image.ARROW_E)
    microbit.sleep(2000)
    microbit.display.show(microbit.Image.ALL_CLOCKS, loop=True, delay=100, wait=False)


def respond_to_time_requests():
    global start_time_sent
    received_message = radio.receive()

    if received_message:
        if received_message.startswith("TIME_REQUEST:"):
            # Send acknowledgment back to the slave (optional for debugging)
            print("Received a time request")
            _, microbit_id = received_message.split(":")
            synced_microbits.add(int(microbit_id))  # Log that the slave is ready

    # Once all slaves have requested time sync, send the start time
    if len(synced_microbits) >= total_slaves and not start_time_sent:
        start_time = utime.ticks_add(utime.ticks_ms(), 5000)  # Set start time 5 seconds from now
        radio.send("START_TIME:{}".format(start_time))
        print("Broadcasting start time:", start_time)
        start_time_sent = True  # Prevent repeated broadcasts of start time


microbit.display.show(microbit.Image.ALL_CLOCKS, loop=True, delay=100, wait=False)

while True:
    respond_to_time_requests()
    if microbit.button_a.was_pressed():
        setup_receiver_notes()
    elif microbit.button_b.was_pressed():
        setup_receiver_tempo()
    elif microbit.accelerometer.was_gesture("shake"):
        send_play_signal()
