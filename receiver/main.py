import microbit
import music
import radio
import utime

radio.on()
radio.config(length=200)

# Initialize global variables
my_microbit_id = 1
my_notes_data = {}
start_time = None  # Placeholder for synchronized start time
is_synchronized = False  # Flag to track synchronization status

# Display the initial microbit ID
microbit.display.show(my_microbit_id, wait=False)


def update_microbit_id():
    global my_microbit_id
    if microbit.button_a.was_pressed():
        if my_microbit_id - 1 == 0:
            microbit.display.show(microbit.Image.NO)
            microbit.sleep(1000)
        else:
            my_microbit_id -= 1
            microbit.display.show(my_microbit_id, wait=False)

    if microbit.button_b.was_pressed():
        my_microbit_id += 1
        microbit.display.show(my_microbit_id, wait=False)


def receive_message():
    global start_time, is_synchronized
    received_message = radio.receive()

    if received_message:
        if received_message.startswith("NOTES"):
            process_notes_message(received_message)
        elif received_message.startswith("TICKS"):
            process_ticks_message(received_message)
        elif received_message.startswith("BPM"):
            process_bpm_message(received_message)
        elif received_message.startswith("START_TIME"):
            # Set the start time based on master's broadcast
            _, start_time_str = received_message.split(":")
            start_time = int(start_time_str)
            is_synchronized = True
            print("Synchronized start time set to:", start_time)
            # Send confirmation to the master
            radio.send("TIME_SYNC_CONFIRMED")


def process_notes_message(message):
    global my_notes_data
    _, bar_number, microbit_id, notes_data = message.split(":", 3)
    bar_number = int(bar_number)
    microbit_id = int(microbit_id)

    if microbit_id == my_microbit_id:
        notes_list = notes_data.split(',')
        my_notes_data[bar_number] = notes_list
        print("Stored notes for bar", bar_number, ":", notes_list)


def process_ticks_message(message):
    _, value = message.split(':')
    ticks = int(value)
    music.set_tempo(ticks=ticks)
    print("Music Ticks set to", ticks)


def process_bpm_message(message):
    _, value = message.split(':')
    bpm = int(value)
    music.set_tempo(bpm=bpm)
    print("Music BPM set to", bpm)


def synchronize_time():
    global is_synchronized
    if is_synchronized:
        return

    print("Sent out a request, waiting for master to broadcast start time.")
    radio.send("TIME_REQUEST:{}".format(my_microbit_id))


# Main loop
while True:
    update_microbit_id()
    receive_message()

    # Trigger time synchronization with a button combination (A + B pressed together)
    if microbit.accelerometer.was_gesture("shake"):
        synchronize_time()
        microbit.display.show(microbit.Image.ALL_CLOCKS, loop=True, delay=100, wait=False)
