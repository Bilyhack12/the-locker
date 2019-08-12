from pynput.keyboard import Listener, KeyCode, Key
from ctypes import *
from time import sleep


class UserInputDisabler(object):
    def __init__(self):
        self.running = True
        self.blocking = False
    def start(self):
        print("start")
        ok = windll.user32.BlockInput(True)
        if ok:
            self.blocking = True
    def stop(self):
        print("stop")
        ok = windll.user32.BlockInput(False)
        if ok:
            self.blocking = False
    def end(self):
        self.blocking = False
        self.running = False

combination = [
        {Key.ctrl_l,Key.alt_l,Key.enter},
        {Key.ctrl_l,Key.alt_l,Key.ctrl_r,Key.alt_r}
    ]
combination_name = {
        "start_stop":{Key.ctrl_l,Key.alt_l,Key.enter},
        "end":{Key.ctrl_l,Key.alt_l,Key.ctrl_r,Key.alt_r}
    }
disabler = UserInputDisabler()
current = set()

def on_press(key):
    if disabler.running:
        if any([key in combo for combo in combination]):
            current.add(key)
            if any(all(k in current for k in combo) for combo in combination):
                if current == set(combination_name["start_stop"]):
                    if disabler.blocking:
                        disabler.stop()
                    else:
                        disabler.start()
                elif current == set(combination_name["end"]):
                    disabler.end()
                    listener.stop()
def on_release(key):
    if any([key in combo for combo in combination]):
        current.remove(key)

with Listener(on_press = on_press,on_release=on_release) as listener:
    listener.join()
