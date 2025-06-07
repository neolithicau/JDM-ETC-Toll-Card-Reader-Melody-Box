# JDM ETC Toll Card Reader Melody Box  
**Raspberry Pi Pico + DFPlayer Mini project **

This project was created to repurpose a Panasonic ETC Toll Card reader as a JDM melody box. It simulates the audio playback behaviour of a Japanese ETC card reader using audio recorded from an actual reader and plays back train station jingles under 10 seconds using a DF Player audio amplifier. 

In my use case, the project was designed to fit within the shell of a Panasonic CY-ET900 ETC Toll Card reader. It uses the existing ETC speaker plug and speaker (physically cut out of the original unit) and uses one of the two buttons on the top (with a bunch of hotglue). I wanted it to be a drop in replacement for an actual ETC Card Reader that was in a Kei truck - noting USB power is different from the hardwired 12v ETC supply.

---

## Summary

This script allows you to easily build an ETC-style audio device with:

- Simple Pico + DFPlayer hardware  
- Flexible and customisable volume feedback  
- Perfect simulation of real ETC reader tones  
- LED visual feedback for user interaction.

---

## Features:

- Non-repeating shuffled main audio tracks  
- User button to trigger playback or adjust volume (volume level select by holding down button for more than 600ms)
- Status LED with blink patterns for visual feedback on volume levels
- Error tone fallback (playback failed or other errors).

---

## What you need

- Raspberry Pi Pico  
- DFPlayer Mini (clone — tested on a common Amazon model)  
- MicroSD card (FAT32, properly ordered - more on this below)  
- Button: Wired to GP16
- LED: Wired to GP5  
- DFPlayer TX/RX: Wired GP0/GP1 → UART0  
- 5V USB supply (Pico takes USB Micro - DFPlayer powered by the Pico)

---

## Features

### Main content playback

- Plays audio tracks from `0006.mp3` to `0073.mp3` stored in the root directory. For my use case, I sorted and selected Japan train station melodies under 10 seconds for playback. The audio files are included in this release.  
- Tracks play in a non-repeating manner — reshuffled each time the pool is exhausted.

### Volume Control

Four volume levels defined as:

| Volume Level | DFPlayer Value | % of Max Volume | Confirmation Tones - Panasonic ETC lines |
|--------------|----------------|-----------------|-------------------|
| Level 1      | 14             | ~40%            | `0002.mp3` → ("Volume is 1.")       |
| Level 2      | 18             | ~60%            | `0003.mp3` → ("Volume is 2.")       |
| Level 3      | 21             | ~70%            | `0004.mp3` → ("Volume is 3.")       |
| Level 4      | 26             | ~87%            | `0005.mp3` → ("Volume is 4. Voice guidance will be stopped." - 6 secs)

- Volume index is saved to `volume.txt` on the Pico → restored on next boot.

### Error Tone

`0001.mp3` in root = error / fallback tone.

### Button Behaviour

- Short press (<0.6 sec) - Plays next shuffled main track.
- Long press (>=0.6 sec) - Cycles volume level → plays corresponding confirmation tone:
    - For level 4 → `0005.mp3` plays for 6 seconds fully to match original Panasonic ETC message for Level 4 volume (it says "Volume is 4. Voice guidance will be stopped.)

### LED light feedback

- LED on GP5 stays solid ON during normal operation.
- LED blinks:
    - 1 blink → volume level 1  
    - 2 blinks → volume level 2  
    - 3 blinks → volume level 3  
    - 4 blinks → volume level 4  
    - 5 blinks → error tone played

The LED light is optional to the overall functionality.

---

## SD Card Layout information

Format: FAT32 (important!)  
Root directory structure: Files must be copied in order to the root directory of a Fat32 formatted MicroSD card. This is due to how the DFPlayer and clones tend to function. If your copy order is wrong, you will hear the wrong tones played back and truncated when selecting new volume levels.

## Known Limitations

- DFPlayer clones do not support folder commands (`0x0F`) reliably → all tones are played from root using `0x03`.
- SD card must be carefully ordered to ensure `0001–0005.mp3` are first. Use FATSort if needed.

## Note on audio files used on this project

The Panasonic ETC Toll Card reader lines were recorded from a real device by me (under alias MortD) and are available on Internet Archive (https://archive.org/details/panasonic-etc-card-reader-cy-et-909-d-audio-lines-.-7z).

The Japanese train jingles were adapted from a widely available pack shared on Reddit and available on Dropbox (https://www.dropbox.com/s/4vpco5q1k2poqz1/JR%20Train%20Departure%20Melodies%20MP3.zip?dl=0)

---

MIT License

Copyright (c) 2025 Neolithicau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
