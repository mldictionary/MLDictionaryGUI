import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import webscrapy

builder = Gtk.Builder()
builder.add_from_file('./glade/interface.glade')

class Handler:
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        
        self.language = webscrapy.English()
        self.entry = builder.get_object('entry')
        self.button_search = builder.get_object('search')
        self.combo = builder.get_object('combo')
        self.label = builder.get_object('label')
    
    def onDestroy(self, *args):
        Gtk.main_quit()
        
        
    def on_button_search_clicked(self, widget):
        word = self.entry.get_text().lower().strip()
        if len(word)==0:
            ...
        else:
            result = self.language.returnMeaning(word)
            if result[0]:
                self.label.set_yalign(0)
                self.label.set_xalign(0)
                self.label.set_justify(Gtk.Justification.LEFT)
                self.label.set_selectable(True)
                self.label.set_text(result[1])
            else:
                self.label.set_yalign(0.5)
                self.label.set_xalign(0.5)
                self.label.set_justify(Gtk.Justification.CENTER)
                self.label.set_selectable(False)
                self.label.set_text(f'The word "{word}" was not found' + '\nPlease, check the word\'s spelling and/or your connection')
 
 
    def on_comboboxtext_changed(self, widget):
        if self.combo.get_active() == 0:
            self.language = webscrapy.English()
        elif self.combo.get_active() == 1:
            self.language = webscrapy.Portuguese()
        elif self.combo.get_active() == 2:
            self.language = webscrapy.Spanish()
            
            
builder.connect_signals(Handler())
window = builder.get_object('main_window')
window.show_all()

if __name__ == '__main__':
    Gtk.main()