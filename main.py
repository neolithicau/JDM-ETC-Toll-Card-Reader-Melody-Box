import machine
import utime
import urandom
import os

# JDM ETC Toll Card Reader Melody Box - Created by Neolithicau
# Offered for free use and modification under the MIT license

# UART setup
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
print("UART initialized on GP0 (TX) and GP1 (RX)")

# Button input on GP16
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

# LED output on GP5 (pin 7 on Pico)
led = machine.Pin(5, machine.Pin.OUT)
led.value(1)  # Keep LED on at all times

def blink_led(times=1, delay=200):
    for _ in range(times):
        led.value(0)
        utime.sleep_ms(delay)
        led.value(1)
        utime.sleep_ms(delay)

# Volume step values
VOLUME_LEVELS = [14, 18, 21, 26]  # 50%, 60%, 70%, ~87% of max volume
VOLUME_FILE = "volume.txt"

# Track range (root folder): 0006–0073 (0001 error tone, 0002–0005 reserved for volume levels)
TRACK_MIN = 6
TRACK_MAX = 73
track_pool = []

def shuffle_track_pool():
    global track_pool
    track_pool = list(range(TRACK_MIN, TRACK_MAX + 1))
    for i in range(len(track_pool) - 1, 0, -1):
        j = urandom.randint(0, i)
        track_pool[i], track_pool[j] = track_pool[j], track_pool[i]
    print("Track pool shuffled.")

def get_next_track():
    global track_pool
    if not track_pool:
        shuffle_track_pool()
    return track_pool.pop()

def load_volume_index():
    try:
        with open(VOLUME_FILE, "r") as f:
            idx = int(f.read().strip())
            if 0 <= idx < len(VOLUME_LEVELS):
                print(f"Loaded saved volume index: {idx}")
                return idx
    except:
        print("No saved volume found. Using default.")
    return VOLUME_LEVELS.index(25)  # Default to 90%

def save_volume_index(index):
    try:
        with open(VOLUME_FILE, "w") as f:
            f.write(str(index))
        print(f"Saved volume index: {index}")
    except Exception as e:
        print(f"Error saving volume index: {e}")

def send_command(cmd, param1=0, param2=0):
    packet = bytearray([0x7E, 0xFF, 0x06, cmd, 0x00, param1, param2, 0xEF])
    uart.write(packet)
    print(f"Sent command: 0x{cmd:02X} Params: {param1}, {param2}")
    utime.sleep_ms(200)

def set_volume(vol):
    send_command(0x06, 0x00, vol)
    print(f"Volume set to {vol} ({int((vol/30)*100)}%)")

def play_track(track_num):
    high_byte = (track_num >> 8) & 0xFF
    low_byte = track_num & 0xFF
    send_command(0x03, high_byte, low_byte)
    print(f"Playing track from root: {track_num:04}")

def play_volume_tone(index):
    # index is 0..3 → play 0002.mp3 to 0005.mp3 in root
    tone_track = index + 2  # 0002.mp3 to 0005.mp3
    print(f"Playing volume tone: {tone_track:04}.mp3 (root)")
    play_track(tone_track)
    blink_led(tone_track - 1)  # Blink 1..4 times corresponding to volume level
    
    # Custom wait: 6 sec for 0005.mp3, else 2 sec
    if tone_track == 5:
        utime.sleep(6.0)
    else:
        utime.sleep(2.0)
    
    stop_playback()
    print("Volume tone finished and stopped.")

def play_error_tone():
    print("Playing ERROR tone: 0001.mp3 (root)")
    play_track(1)
    blink_led(5)
    utime.sleep(2.0)
    stop_playback()
    print("Error tone finished.")

def stop_playback():
    send_command(0x16)
    print("Playback stopped")

def play_next_main_track():
    next_track = get_next_track()
    play_track(next_track)

# === Startup ===
print("Waiting for DFPlayer to boot...")
utime.sleep(1)

volume_index = load_volume_index()
volume = VOLUME_LEVELS[volume_index]
set_volume(volume)

shuffle_track_pool()
play_next_main_track()
print("Waiting for button press on GP16...")

# === Main Loop ===
while True:
    if button.value() == 0:
        press_time = utime.ticks_ms()
        print("Button down")

        while button.value() == 0:
            utime.sleep_ms(10)

        release_time = utime.ticks_ms()
        duration = utime.ticks_diff(release_time, press_time) / 600
        print(f"Button held for {duration:.2f} seconds")

        if duration < 0.6:
            play_next_main_track()
        else:
            print("Long press: changing volume")
            stop_playback()
            utime.sleep(0.3)

            volume_index = (volume_index + 1) % len(VOLUME_LEVELS)
            volume = VOLUME_LEVELS[volume_index]
            set_volume(volume)
            save_volume_index(volume_index)

            utime.sleep(0.5)
            play_volume_tone(volume_index)

            continue

        utime.sleep(0.2)
