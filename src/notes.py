import glob
import pickle
from music21 import converter, instrument, note, chord

class Notes:
    def __init__(self, path_to_data, path_to_dump):
        self.array = []
        self.path_to_data = path_to_data
        self.path_to_dump = path_to_dump

    def update(self):
        """ Get all the notes and chords from the midi files in the dataset directory """
        for file in glob.glob(self.path_to_data):
            midi = converter.parse(file)

            print("Parsing %s" % file)

            notes_to_parse = None

            try: # file has instrument parts
                s2 = instrument.partitionByInstrument(midi)
                notes_to_parse = s2.parts[0].recurse() 
            except: # file has notes in a flat structure
                notes_to_parse = midi.flat.notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    self.array.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    self.array.append('.'.join(str(n) for n in element.normalOrder))
    
    def save(self):
        with open(self.path_to_dump, 'wb') as filepath:
            pickle.dump(self.array, filepath)
    
    def load(self):
         with open(self.path_to_dump, 'rb') as filepath:
            self.array = pickle.load(filepath)