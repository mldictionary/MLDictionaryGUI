#!/bin/python3


from sys import path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import webscrapy

builder = Gtk.Builder()
builder.add_from_file(f'{path[0]}/glade/interface.glade')


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
        self.is_to_play = False
        self.pronounce_spell = builder.get_object('pronounce_spell')
        self.is_to_search_pronounce_spell = False
        
        
    def onDestroy(self, *args):
        Gtk.main_quit()


    def on_button_search_clicked(self, widget):
        import re
        if len(word := re.sub('[^\w ]+', '', self.entry.get_text().lower().strip()))>0:
            self.current_word.set_text(word.upper())
            source = f'<a href="{self.language.URL.format(word)}">' + self.language.URL.format(word) + '</a>'
            self.current_source.set_markup(source)
            if result := self.language.get_meanings(word):
                if str(self.language)=='Spanish':
                    meanings = '\n\n'.join([f'{pos+1}º: {mean[5:]}' for pos, mean in enumerate(result)])
                else:
                    meanings = '\n\n'.join([f'{pos+1}º: {mean}' for pos, mean in enumerate(result)])
                self.label.set_yalign(0)
                self.label.set_xalign(0)
                self.label.set_justify(Gtk.Justification.LEFT)
                self.label.set_selectable(True)
                self.label.set_text(meanings)
                self.pronounce_spell.set_text('Click on sound to see the word\'s pronounce spell')            
            else:
                self.label.set_yalign(0.5)
                self.label.set_xalign(0.5)
                self.label.set_justify(Gtk.Justification.CENTER)
                self.label.set_selectable(False)
                self.label.set_text(f'The word "{word}" was not found' + '\nPlease, check the word\'s spelling and/or your connection')
                self.pronounce_spell.set_text('')
            self.is_to_play = result
            self.is_to_search_pronounce_spell = result


    def show_up_pronounce_spell(self, word, language):
        if self.is_to_search_pronounce_spell:
            self.pronounce_spell.set_text(self.pronounce.return_pronounce_spell(word, language))
            self.is_to_search_pronounce_spell = False

 
    def on_button_play_sound_clicked(self, widget):
        if len(word := self.current_word.get_text().lower().strip()) > 0 and self.is_to_play:
            self.pronounce.play_audio(word, str(self.language))
        self.show_up_pronounce_spell(word, self.current_language.get_text())
                
    
    def on_comboboxtext_changed(self, widget):
        if self.combo.get_active() == 0:
            self.language = webscrapy.English()
            self.language_source = 'https://dictionary.cambridge.org/us/'
        elif self.combo.get_active() == 1:
            self.language = webscrapy.Portuguese()
            self.language_source = 'https://www.dicio.com.br/'
        elif self.combo.get_active() == 2:
            self.language = webscrapy.Spanish()
            self.language_source = 'https://dle.rae.es//'
            
        self.current_language.set_text(str(self.language) + ':')
        self.current_word.set_text('')
        self.current_source.set_text(self.language_source)
        self.label.set_text('')
        self.pronounce_spell.set_text('')


builder.connect_signals(Handler())
window = builder.get_object('main_window')
window.show_all()

if __name__ == '__main__':
    Gtk.main()
