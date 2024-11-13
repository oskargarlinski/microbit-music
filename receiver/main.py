import microbit
import music
import radio

radio.on()
radio.config(length=200)

my_microbit_id = 1
microbit.display.show(my_microbit_id, wait=False)

my_notes_data = {}

while True:
    received_message = radio.receive()

    if microbit.button_a.was_pressed():
        if my_microbit_id - 1 == 0:
            microbit.display.show(microbit.Image.NO)
            microbit.sleep(1000)
            microbit.display.show(my_microbit_id, wait=False)
        else:
            my_microbit_id -= 1
            microbit.display.show(my_microbit_id, wait=False)

    if microbit.button_b.was_pressed():
        my_microbit_id += 1
        microbit.display.show(my_microbit_id, wait=False)

    if received_message:
        # Check if the message starts with notes, if it does, then you know it's music data.
        if received_message.startswith("NOTES"):
            # Split the received message into relevant parts - keyword (_), bar_number (bar_number), microbit_id (microbit_id) and notes data (notes_data)
            _, bar_number, microbit_id, notes_data = received_message.split(":", 3)
            # Cast the received data into proper data types
            bar_number = int(bar_number)
            microbit_id = int(microbit_id)

            # Check if the microbit id matches
            if microbit_id == my_microbit_id:
                # Convert notes data back into a list
                notes_list = notes_data.split(',')

                # Store the notes list in the notes_data dictionary with the key of the bar number
                my_notes_data[bar_number] = notes_list
                print("Stored notes for bar", bar_number, ":", notes_list)


        # Check if the message starts with ticks, if it does, then you know it's tempo data.
        if received_message.startswith("TICKS"):
            _, value = received_message.split(':')
            ticks = int(value)
            music.set_tempo(ticks = ticks)
            print("Music Ticks set to", ticks)

        # Check if the message starts with bpm, if it does, then you know it's tempo data.
        if received_message.startswith("BPM") :
            _, value = received_message.split(':')
            bpm = int(value)
            music.set_tempo(bpm = bpm)
            print("Music BPM set to", bpm)


