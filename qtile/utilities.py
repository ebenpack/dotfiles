# symlinked at ~/.config/qtile/utilities.py

from libqtile.config import Screen
from libqtile import bar, widget

import subprocess, re

class Xrandr(object):
    """
    Object representing connected screens, as reported by xrandr.
    This is very simple at the moment, and does not, in its current state, really deserve
    its own module, but the intention is to expand the functionality to provide more
    complicated interaction with connected screens.
    """
    def __init__(self):
        xrandr_process = subprocess.Popen("xrandr", stdout=subprocess.PIPE)
        out, err = xrandr_process.communicate()
        self.xrandr_output = out.decode(encoding='UTF-8')

    @property
    def screens(self):
        screens = []
        lines = self.xrandr_output.split('\n')[1:]

        temp = []
        for line in lines:
            if not line.startswith("   "):
                screens.append(temp)
                temp = []
            temp.append(line)
        screens.append(temp)
        return screens

    @property
    def connected_screens(self):
        return re.findall("(.*)\sconnected", self.xrandr_output)


def initialize_screens():
    X = Xrandr()
    S1 = "LVDS1"
    S2 = "VGA1"

    primary_screen = Screen(
                top = bar.Bar(
                    [
                        widget.GroupBox(
                            urgent_alert_method='text',
                            fontsize=14,
                            borderwidth=1),
                        widget.CurrentLayout(),
                        widget.WindowName(foreground = "a0a0a0"),
                        widget.Prompt(foreground = "CF0C0C"),
                        widget.Notify(),
                        widget.Systray(),
                        widget.Wlan(interface="wlp4s0b1"),
                        widget.Battery(
                            energy_now_file='energy_now',
                            energy_full_file='energy_full',
                            power_now_file='energy_now',
                            update_delay = 5,
                            foreground = "7070ff"), 
                        widget.Volume(foreground = "70ff70"),
                        widget.Clock(foreground = "a0a0a0",
                            fmt = '%Y-%m-%d %a %I:%M %p'),
                    ], 22,
                ),
            )
    secondary_screen = Screen(
                top = bar.Bar(
                    [
                        widget.GroupBox(
                            urgent_alert_method='text',
                            fontsize=14,
                            borderwidth=1),
                        widget.CurrentLayout(),
                        widget.WindowName(foreground = "a0a0a0"),
                        widget.Prompt(),
                        widget.Clock(foreground = "a0a0a0",
                            fmt = '%Y-%m-%d %a %I:%M %p'),
                    ], 22,
                ),
            )
    
    one_screen = [primary_screen]
    two_screens = [primary_screen, secondary_screen]

    if len(X.connected_screens) == 2:
        subprocess.call(["xrandr", "--output", S1, "--auto", "--output", 
            S2, "--auto", "--left-of", S1])
        screens = two_screens
    else:
        subprocess.call(["xrandr", "--output", S1, "--auto", "--output", 
            S2, "--off"])
        screens = one_screen
    return screens