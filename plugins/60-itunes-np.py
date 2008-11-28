#!/usr/bin/env python

from subprocess import Popen, PIPE
from thread import start_new_thread

from pynicotine.gtkgui.pluginsystem import BasePlugin, returncode

class Plugin(BasePlugin):
    __name__ = "iTunes OSX Now Playing"
    __version__ = "2008-11-28r00"
    osascript = """
tell application "iTunes"
    set myartist to the artist of current track as string
    set mytrack to the name of current track
    set mystate to the player state
    if myartist is not "" then
        set info to (the myartist & the " - " & the mytrack)
    else
        set info to the mytrack
    end if
    set info to (the info & " [" & the mystate & "]")
end tell """

    def PublicCommand(self, command, room, args):
        if command in ('itunes',):
            # We'll fork the osascript since it' slow as hell
            start_new_thread(self.spam, (self.saypublic,room))
            return returncode['zap']
    def PrivateCommand(self, command, user, args):
        if command in ('itunes',):
            # We'll fork the osascript since it' slow as hell
            start_new_thread(self.spam, (self.sayprivate,user))
            return returncode['zap']
    def spam(self, callbackfunc, destination):
        self.log("Probing iTunes...")
        proc = Popen(['osascript','-e',self.osascript], stdout=PIPE)
        (out, err) = proc.communicate()
        out = out.rstrip('\r\n ')
        if not out:
            self.log("The output was empty.")
            return
        out = ' '.join(['iTunes:',out])
        callbackfunc(destination, out)