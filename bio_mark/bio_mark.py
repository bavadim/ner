#!/usr/bin/env python3

import sys
import csv
import random
import functools

import signal
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from gi.repository import Notify

APPID = "GTK Test"
CURRDIR = os.path.dirname(os.path.abspath(__file__))
# could be PNG or SVG as well
ICON = os.path.join(CURRDIR, 'icon.svg')

class Handler:

    def __init__(self):
        self.window_is_hidden = False

    def onShowButtonClicked(self, button):
        msg = "Clicked: " + entry.get_text()
        dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, msg)
        dialog.run()
        dialog.destroy()

    def onNotify(self, *args):
        Notify.Notification.new("Notification", "Hello!", ICON).show()

    def onShowOrHide(self, *args):
        if self.window_is_hidden:
            window.show()
        else:
            window.hide()

        self.window_is_hidden = not self.window_is_hidden

    def onQuit(self, *args):
        Notify.uninit()
        Gtk.main_quit()

# Handle pressing Ctr+C properly, ignored by default
signal.signal(signal.SIGINT, signal.SIG_DFL)

builder = Gtk.Builder()
builder.add_from_file('gui.glade')
builder.connect_signals(Handler())

text = builder.get_object('text')
text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

textbuffer = text.get_buffer()

colors = [
        'INDIANRED', 
        'PINK', 
        'LIGHTSALMON', 
        'GOLD', 
        'LAVENDER', 
        'GREENYELLOW', 
        'AQUA', 
        'CORNSILK', 
        'MISTYROSE', 
        'GAINSBORO', 
        'GOLDENROD', 
        'ORANGE'
        ]
text = ''
tags = []
for row in csv.reader(iter(sys.stdin.readline, ''), delimiter=' '):
    if len(row) !=2:
        print('bad input: ' + str(row), file=sys.stderr)
        continue

    word = row[0]
    tp = row[1]

    if tp == 'O':
        text = text + ' ' + word
        continue

    start = len(text)
    text = text + ' ' + word
    end = len(text)

    tags.append((start, end, tp))

def combine(acc, rt):
    start, end, type = rt
    if len(acc) > 0 and acc[-1][2].replace('I-', '').replace('B-', '') == type.replace('I-', '').replace('B-', '') :
        return acc[:-1] + [(acc[-1][0], end, acc[-1][2])]
    else:
        return acc + [(start, end, type.replace('I-', '').replace('B-', ''))]

for i in functools.reduce(combine, tags, []):
    tag = textbuffer.create_tag(row[1], background=random.choice(colors))
    textbuffer.apply_tag(tag, textbuffer.get_iter_at_offset(start), textbuffer.get_iter_at_offset(end))


textbuffer.set_text(text)

window = builder.get_object('main_window')
window.set_icon_from_file(ICON)
window.show_all()
Notify.init(APPID)
Gtk.main()
