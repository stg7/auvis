#!/usr/bin/env python
# based on https://github.com/tez3998/loopback-capture-sample
import soundcard as sc
import soundfile as sf
import numpy as np
import curses
from curses import wrapper

def main(stdscr):

    OUTPUT_FILE_NAME = "out.wav"    # file name.
    SAMPLE_RATE = 44000              # [Hz]. sampling rate.
    RECORD_SEC = 0.1                  # [sec]. duration recording audio.
    MAX_WIDTH = curses.COLS - 1
    MAX_HEIGHT = curses.LINES
    #all_data = np.array([])
    try:
        while True:
            stdscr.clear()
            with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                # record audio with loopback from default speaker.
                data = mic.record(numframes=int(SAMPLE_RATE*RECORD_SEC))
                # data = 4400, 2
                #print(help(mic.record))
                #breakpoint()
                #print(data[:,1], data.shape)

                hist, _ = np.histogram(data[:,1], bins=MAX_HEIGHT)
                hist2, _ = np.histogram(data[:,0], bins=MAX_HEIGHT)
                #print(hist)
                for i, v in enumerate(hist):
                    #bar = "▇" * int(MAX_WIDTH * v / (SAMPLE_RATE*RECORD_SEC))
                    bar = "▀" * int(MAX_WIDTH * v / (3   * hist.max()))
                    #print(i, bar)
                    if len(bar) > MAX_WIDTH // 3:
                        pass
                    stdscr.addstr(i, 0, bar)
                for i, v in enumerate(hist2): # ▀ ▇ █
                    bar = "▀" * int(MAX_WIDTH * v / (3   * hist2.max()))
                    #print(i, bar)
                    if len(bar) > MAX_WIDTH // 3:
                        pass
                    stdscr.addstr(i, max(0, MAX_WIDTH - len(bar)), bar)
                #all_data = np.append(all_data, data).reshape((-1,2))
                #print(all_data.shape)
            stdscr.refresh()
            #stdscr.getkey()
    except KeyboardInterrupt:
        #breakpoint()
        # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
        #sf.write(file=OUTPUT_FILE_NAME, data=all_data, samplerate=SAMPLE_RATE)
        return


wrapper(main)
#main("")