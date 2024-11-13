# Conductor Microbit (Master)

- Define a dictionary to hold music data:
    - Structure: `{ bar_number: { microbit_id: [list_of_notes] } }`
- Define tempo and time signature for interval calculation
- Initialize radio communication

1. **Setup Phase**:
    - For each bar in the dictionary:
        - For each microbit ID in the bar:
            - Send the list of notes and wait for acknowledgment from each microbit

2. **Send Start Signal**:
    - Calculate the start time for the piece based on current time and tempo
    - Broadcast "start signal" with the start time and tempo information
    - Each microbit will calculate intervals internally based on the tempo and time signature
    - Monitor for acknowledgments that the start time was received

3. **Performance Monitoring**:
    - Conductor can monitor progress or re-sync if necessary but avoids sending continuous timing signals

4. **End Performance**:
    - Broadcast a "stop signal" to end playback

# Receiver Microbit (Player)

- Initialize and listen for radio signals
- On receiving note data for each bar:
    - Store notes locally and acknowledge receipt to conductor

- On receiving "start signal" with start time and tempo:
    - Calculate the interval for each bar based on tempo and time signature
    - Acknowledge the start time and tempo received
    - Set a local timer to begin playback at the calculated start time
    - Use the bar interval to autonomously progress through bars

- During Playback:
    - Retrieve notes for the current bar based on the bar interval
    - Play assigned notes at each interval until reaching the final bar

- On receiving "stop signal":
    - Stop playing and reset

# General Flow

1. **Initialization**:
    - Preload music data with acknowledgments for each bar
2. **Start Timing**:
    - Use a single start signal to communicate start time and calculate intervals
3. **Autonomous Playback**:
    - Microbits use internal timers to stay in sync with each other based on start time
4. **End of Performance**:
    - Stop signal concludes playback
