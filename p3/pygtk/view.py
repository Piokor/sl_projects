import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pygtk.htmls import UI_INFO
from pygtk.helpWindow import DialogExample


class GolWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Menu Example")

        self.set_default_size(902, 942)

        action_group = Gtk.ActionGroup(name="my_actions")

        self.add_file_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)

        self.add(box)

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action(name="HelpMenu", label="Pomoc")
        action_group.add_action(action_filemenu)

        action_new = Gtk.Action(
            name="ShowHelpA",
            label="_Pokaż pomoc",
            tooltip="",
            stock_id=Gtk.STOCK_NEW,
        )
        action_new.connect("activate", self.on_menu_file_new_generic)
        action_group.add_action(action_new)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_file_new_generic(self, a):
        dialog = DialogExample(self)
        dialog.run()
        dialog.destroy()