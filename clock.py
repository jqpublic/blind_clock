#!/usr/bin/python

# Copyright 2010 Daniel Buettner
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import Tkinter
import time
import math
import string
import os

ROUND_MINUTES = 25

def time_format(x):
    m = int(math.floor(x / 60))
    s = min(x % 60, 59)

    return "%02d:%02.0f\n" % (m,s)



class Timer(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        now = time.time()

        self.last_tick = now
        self.round_length = ROUND_MINUTES*60.0
        self.remaining = self.round_length

        self.paused = True

        w = self.big_text("current blind")
        w.pack()
        self.lbl_current_blind = self.quadroon_text("?")
        self.lbl_current_blind.pack()

        self.lbl_countdown = self.big_text("")
        self.lbl_countdown.pack()
        
        w = self.small_text("next blind")
        w.pack()
        self.lbl_next_blind = self.small_text("?")
        self.lbl_next_blind.pack()

        b = Tkinter.Button(self.root, text="pause", command=self.pause)
        b.pack()
        b = Tkinter.Button(self.root, text="skip", command=self.skip)
        b.pack()
        self.entry_interval = Tkinter.Entry(self.root, width=5)
        self.entry_interval.pack()
        self.entry_interval.insert(0, int(self.round_length/60))

        f = open("structure")
        self.blinds = f.readlines()
        f.close()
        self.blind_idx = 0

    def update_timer(self):
        now = time.time()

        if not self.paused:
            if self.remaining >= 60.0:
                maybe_warn = True
            else:
                maybe_warn = False

            self.remaining -= (now - self.last_tick)

            if maybe_warn and self.remaining < 60:
                os.system("afplay smb_warning.wav")

            if self.remaining < 0:
                self.update_round_length()
                self.remaining = self.round_length
                self.blind_idx = self.safe_blind_idx(self.blind_idx + 1)
                s = self.blinds[self.blind_idx]
                if s[0] not in string.digits:
                    if s.startswith("buy"):
                        self.paused = True
                        os.system("afplay smb_1-up.wav")
                    else:
                        self.paused = True
                        os.system("afplay smb_pause.wav")
                else:
                    os.system("afplay smb_mariodie.wav")

        self.last_tick = time.time()
        if not self.paused:
            self.lbl_countdown["text"] = time_format(self.remaining)
        else:
            self.lbl_countdown["text"] = "paused: %s" % time_format(self.remaining)
        self.lbl_current_blind["text"] = self.blinds[self.blind_idx]
        self.lbl_next_blind["text"] = self.blinds[self.safe_blind_idx(self.blind_idx+1)].strip()
        self.root.after(100, self.update_timer)


    def safe_blind_idx(self, val):
        return min(val, len(self.blinds)-1)
        

    def big_text(self, s):
            return Tkinter.Label(self.root, text=s, font=("Helvetica", 100))

    def quadroon_text(self, s):
            return Tkinter.Label(self.root, text=s, font=("Helvetica", 100), fg="red")


    def small_text(self, s):
        return Tkinter.Label(self.root, text=s, font=("Helvetica", 60))


    def go(self):
        self.update_timer()
        self.root.mainloop()

    def pause(self):
        self.paused = not self.paused
        os.system("afplay smb_pause.wav")

    def skip(self):
        self.blind_idx = self.safe_blind_idx(self.blind_idx + 1)
        self.update_round_length()
        self.remaining = self.round_length

    def update_round_length(self):
        try:
            foo = float(self.entry_interval.get()) * 60
        except:
            return
            
        self.round_length = foo
        

my_timer = Timer()
my_timer.go()
