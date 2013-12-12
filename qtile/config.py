# symlinked at ~/.config/qtile/config.py

from libqtile.config import Key, Group, Click, Drag
from libqtile.command import lazy
from libqtile import layout, hook

import utilities

import subprocess, re

mod = "mod4"

widget_defaults = dict(
    font = 'Source Code Pro',
    border_focus="#de4377",
    border_normal="#ad8e99"
)

keys = [
    # Log out
    Key([mod, "shift"], "q",
        lazy.shutdown()),
    Key([mod, "shift"], "r",
        lazy.restart()),
    Key([mod, "shift"], "c",
        lazy.window.kill()),

    # Switch between windows in current stack pane
    Key([mod], "l",
        lazy.layout.down()),
    Key([mod], "h",
        lazy.layout.up()),


    # Move windows up or down in current stack
    Key([mod], "k",
        lazy.layout.next()),
    Key([mod], "j",
        lazy.layout.previous()),

    # Resize windows in current stack pane
    Key([mod, "shift"], "h", 
        lazy.layout.decrease_ratio()),
    Key([mod, "shift"], "l", 
        lazy.layout.increase_ratio()),

    # MonadTall resize
    ####
    # It would be nice if these key bindings could be same as the two above. Is this possible?
    ####
    Key([mod, "shift"], "j", 
        lazy.layout.grow()),
    Key([mod, "shift"], "k", 
    lazy.layout.shrink()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k",
        lazy.layout.shuffle_down()),
    Key([mod, "control"], "j",
        lazy.layout.shuffle_up()),

    Key([mod, "control"], "h",
        lazy.layout.section_down()),
    Key([mod, "control"], "l",
        lazy.layout.section_up()),


    # Switch window focus to other pane(s) of stack
    Key([mod, "shift"], "space",
        lazy.layout.next()),

    # Swap panes of split stack
    Key([mod], "s",
        lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split()),
    # Key([mod], "h",
    #     lazy.to_screen(1)),
    # Key([mod], "l",
    #     lazy.to_screen(0)),
    
    # Launch specific applications
    Key([mod], "Return", 
        lazy.spawn("terminator")),
    Key([mod], "w",
        lazy.spawn("firefox")),
    Key([mod], "r",
        lazy.spawncmd()),

    # Toggle between different layouts as defined below
    Key([mod], "space",
        lazy.nextlayout()),
    Key([mod], "f",
        lazy.window.toggle_fullscreen()),
    Key([mod, "control"], "space",
        lazy.window.toggle_floating()),
    Key([mod], "m",
        lazy.window.toggle_maximize()),
    Key([mod], "n",
        lazy.window.toggle_minimize()),
    
    # Move between groups
    
    Key([mod], "Right",
        lazy.screen.nextgroup()),
    Key([mod], "Left",
        lazy.screen.prevgroup()),
]

mouse = [
   Drag([mod], "Button1", lazy.window.set_position_floating(),
       start=lazy.window.get_position()),
   Drag([mod], "Button3", lazy.window.set_size_floating(),
       start=lazy.window.get_size()),
   Click([mod], "Button2", lazy.window.bring_to_front())
]

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
]
for i in groups:
    # mod4 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen()))

    # mod4 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)))

dbgroups_key_binder = None
dbgroups_app_rules = []

layouts = [
    layout.Tile(**widget_defaults),
    layout.RatioTile(**widget_defaults),
    layout.MonadTall(**widget_defaults),
    layout.Max(),
    layout.TreeTab(),
    layout.Zoomy(),
    layout.Stack(),
]

screens = utilities.initialize_screens()

def is_running(process):
    s = subprocess.Popen(["ps", "axuw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False

def execute_once(process, options=""):
    if not is_running(process):
        process = process.split()
        if options:
            process.extend(options.split())
        return subprocess.Popen(process)

main = None
follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()

@hook.subscribe.startup
def startup():
    execute_once("conky")
    execute_once("dropboxd")
    execute_once("redshift", "-l 44.6:-68.37 -t 5700:3600 -g 0.8 -m randr")
