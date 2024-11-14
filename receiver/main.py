import microbit
import music
import radio

radio.on()
radio.config(length=200)

# Initialize global variables
my_microbit_id = 1
my_notes_data = {}

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
    received_message = radio.receive()
    if received_message:
        if received_message.startswith("NOTES"):
            process_notes_message(received_message)
        elif received_message.startswith("TICKS"):
            process_ticks_message(received_message)
        elif received_message.startswith("BPM"):
            process_bpm_message(received_message)


def process_notes_message(message):
    global my_notes_data
    # Split the message into keyword (_), bar_number, microbit_id, and notes_data
    _, bar_number, microbit_id, notes_data = message.split(":", 3)
    bar_number = int(bar_number)
    microbit_id = int(microbit_id)

    # Check if the microbit ID matches
    if microbit_id == my_microbit_id:
        # Convert notes data back into a list and store in my_notes_data
        notes_list = notes_data.split(',')
        my_notes_data[bar_number] = notes_list
        print("Stored notes for bar", bar_number, ":", notes_list)


def process_ticks_message(message):
    # Process and set the ticks for tempo
    _, value = message.split(':')
    ticks = int(value)
    music.set_tempo(ticks=ticks)
    print("Music Ticks set to", ticks)


def process_bpm_message(message):
    # Process and set the BPM for tempo
    _, value = message.split(':')
    bpm = int(value)
    music.set_tempo(bpm=bpm)
    print("Music BPM set to", bpm)


# Main loop
while True:
    update_microbit_id()
    receive_message()
