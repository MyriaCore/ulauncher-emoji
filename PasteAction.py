import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Xlib import X, display
from Xlib.ext import xtest
from ulauncher.api.shared.action.BaseAction import BaseAction

xdisplay = display.Display()

class PasteAction(BaseAction):
    """
    Simulate paste key press
    """

    def keep_app_open(self):
        return False
    
    def perform_key_event(self, accelerator, press, delay=X.CurrentTime):
        key, modifiers = Gtk.accelerator_parse(accelerator)
        keycode = xdisplay.keysym_to_keycode(key)
        event_type = X.KeyPress if press else X.KeyRelease

        if keycode != 0:
            if modifiers & Gdk.ModifierType.CONTROL_MASK:
                modcode = xdisplay.keysym_to_keycode(Gdk.KEY_Control_L)
                xtest.fake_input(xdisplay, event_type, modcode, delay)

            if modifiers & Gdk.ModifierType.SHIFT_MASK:
                modcode = xdisplay.keysym_to_keycode(Gdk.KEY_Shift_L)
                xtest.fake_input(xdisplay, event_type, modcode, delay)

            xtest.fake_input(xdisplay, event_type, keycode, delay)
            xdisplay.sync()

    def run(self):
        self.perform_key_event("<Control>v", True, 100)
        self.perform_key_event("<Control>v", False, 0)
