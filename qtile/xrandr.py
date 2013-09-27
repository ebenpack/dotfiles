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
