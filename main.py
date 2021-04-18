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
        self.pronounce = webscrapy.Pronunciation()
        
        self.entry = builder.get_object('entry')
        self.button_search = builder.get_object('search')
        self.combo = builder.get_object('combo')
        self.label = builder.get_object('label')
        
        self.current_language = builder.get_object('current_language')
        self.current_word = builder.get_object('current_word')
        
        self.current_source = builder.get_object('current_source')
        self.language_source = 'https://dictionary.cambridge.org/us/'
        
        self.play_sound = builder.get_object('play_sound')
        self.pronounce_spell = builder.get_object('pronounce_spell')
        self.is_to_play = False

    def onDestroy(self, *args):
        Gtk.main_quit()


    def on_button_search_clicked(self, widget):
        import re
        word = self.entry.get_text().lower().strip()
        word = re.sub('[^\w ]+', '', word)
        if len(word)==0:
            ...
        else:
            self.current_word.set_text(word.upper())
            if self.language.__repr__() == 'English':
                self.current_source.set_markup(f'<a href="{self.language_source + f"dictionary/english/" + word}"> {self.language_source + f"dictionary/english/" + word}</a>')
            else:
                self.current_source.set_markup(f'<a href="{self.language_source + word}">{self.language_source + word}</a>')
            result = self.language.returnMeaning(word)
            if result[0]:
                self.label.set_yalign(0)
                self.label.set_xalign(0)
                self.label.set_justify(Gtk.Justification.LEFT)
                self.label.set_selectable(True)
                self.label.set_text(result[1])
                
                spell = self.pronounce.return_pronounce_spell(word, self.current_language.get_text())
                self.pronounce_spell.set_text(spell)
            else:
                self.label.set_yalign(0.5)
                self.label.set_xalign(0.5)
                self.label.set_justify(Gtk.Justification.CENTER)
                self.label.set_selectable(False)
                self.label.set_text(f'The word "{word}" was not found' + '\nPlease, check the word\'s spelling and/or your connection')
                self.pronounce_spell.set_text('')
            self.is_to_play = result[0]

    def on_button_play_sound_clicked(self, widget):
        word = self.current_word.get_text().lower()
        if len(word.strip()) > 0 and self.is_to_play:
            self.pronounce.play_audio(word, self.language.__repr__())
        

   
    def on_comboboxtext_changed(self, widget):
        if self.combo.get_active() == 0:
            self.language = webscrapy.English()
            self.language_source = 'https://dictionary.cambridge.org/us/'
        elif self.combo.get_active() == 1:
            self.language = webscrapy.Portuguese()
            self.language_source = 'https://www.dicio.com.br/'
        elif self.combo.get_active() == 2:
            self.language = webscrapy.Spanish()
            self.language_source = 'https://www.wordreference.com/definicion/'

        
        self.current_language.set_text(self.language.__repr__() + ':')
        self.current_word.set_text('')
        self.current_source.set_text(self.language_source)
        self.label.set_text('')
        self.pronounce_spell.set_text('')


builder.connect_signals(Handler())
window = builder.get_object('main_window')
window.show_all()

if __name__ == '__main__':
    Gtk.main()
