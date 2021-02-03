import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import webscrapy


class Window(Gtk.Window):    
    def __init__(self):
        Gtk.Window.__init__(self, title='MultiLanguage Dictionay')
        self.set_border_width(10)
        self.set_size_request(800, 600)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'MultiLanguage Dictionay'
        self.set_titlebar(hb)
        
        self.language = webscrapy.English()

        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        self.add(vbox)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.entry = Gtk.Entry()
        self.entry.set_size_request(400, 5)
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, 'system-search-symbolic')
        self.entry.connect("activate", self.on_button_search_clicked)
        hbox.pack_start(self.entry, True, True, 0)

        button_search = Gtk.Button(label='Search')
        button_search.connect('clicked', self.on_button_search_clicked)
        hbox.add(button_search)

        self.combo = Gtk.ComboBoxText()
        self.combo.insert(0, '0', 'English')
        self.combo.insert(1, '1', 'Portuguese')
        self.combo.insert(2, '2', 'Spanish')
        self.combo.set_active(0)
        self.combo.connect('changed', self.on_comboboxtext_changed)
        hbox.add(self.combo)
        vbox.add(hbox)
        
        self.label = Gtk.Label(label='')
        self.label.set_line_wrap(True)
        
        answerbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        answerbox.set_border_width(6)
        # answerbox.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(32000, 32000, 32000))
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_border_width(10)
        scroll.set_size_request(600, 350)
        scroll.add(self.label)

        answerbox.pack_start(scroll, True, True, 0)
        vbox.pack_start(answerbox, True, True, 0)
        
        
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

win = Window()
win.connect('destroy', Gtk.main_quit)
win.show_all()
if __name__ == '__main__':
    Gtk.main()