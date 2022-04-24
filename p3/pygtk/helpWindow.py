import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DialogExample(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label='Wciśnij na komórkę aby zmienić jej stan.\nWciśnij przycisk "Start", aby rozpocząć automatyczną symulację, której prędkość można zmienić suwakiem.\nWciśnij przycisk "Następna", aby wyświetlić kolejną epokę.\nWciśnij przycisk "Reset", aby zresetować stan tablicy')

        box = self.get_content_area()
        box.add(label)
        self.show_all()