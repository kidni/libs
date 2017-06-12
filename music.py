import re

SCALES = {
    'Major':            ['M2', 'M3', 'P4', 'P5', 'M6', 'M7', 'P8'],
    'Harmonic Minor':   ['M2', 'm3', 'P4', 'P5', 'm6', 'M7', 'P8'],
    'Melodic Minor':    ['M2', 'm3', 'P4', 'P5', 'M6', 'M7', 'P8'],
    'Dorian':           ['M2', 'm3', 'P4', 'P5', 'M6', 'm7', 'P8'],
    'Phrygian':         ['m2', 'm3', 'P4', 'P5', 'm6', 'm7', 'P8'],
    'Lydian':           ['M2', 'M3', 'A4', 'P5', 'M6', 'M7', 'P8'],
    'Mixolydian':       ['M2', 'M3', 'P4', 'P5', 'M6', 'm7', 'P8'],
    'Aeolian':          ['M2', 'm3', 'P4', 'P5', 'm6', 'm7', 'P8'],
    'Locrian':          ['m2', 'm3', 'P4', 'd5', 'm6', 'm7', 'P8'],
    'Major Pentatonic': ['M2', 'M3', 'P5', 'M6', 'P8'],
    'Minor Pentatonic': ['m3', 'P4', 'P5', 'm7', 'P8'],
}


class Note():
    tones = {0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 11: 'B'}
    note_ids = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    def __init__(self, note):
        note_pattern = re.compile(r'^[A-G]([b#])?$')

        if note_pattern.search(note) is None:
            raise Exception(note + ' is not a valid note')

        self.tone = note[0]
        self.accidental = re.findall('[b#]', note)
        self.note_id = self.note_ids[self.tone]

        for change in self.accidental:
            if change == '#':
                self.note_id += 1
            elif change == 'b':
                self.note_id -= 1
        self.note_id %= 12

        if self.accidental == []:
            self.accidental = ''
        else:
            self.accidental = self.accidental[0]

    def get_closest_tone(self, note_id, direction='asc'):
        """
        Takes the ID of a note and a direction then returns a Note.
        If direction is 'asc' a sharp is returned if needed
        If direction is 'desc' a flat is returned if needed
        """
        if note_id in self.tones:
            return Note(self.tones[note_id])
        if direction == 'asc':
            return Note(self.tones[note_id-1]+'#')
        else:
            return Note(self.tones[note_id+1]+'b')

    def __add__(self, interval):
        if not isinstance(interval, Interval):
            raise Exception(type(interval) + ' is not a valid Interval')
        _new_note_id = (self.note_id + interval.semitones) % 12
        return self.get_closest_tone(_new_note_id)

    def __sub__(self, interval):
        if not isinstance(interval, Interval):
            raise Exception(type(interval) + ' is not a valid Interval')
        _new_note_id = (self.note_id - interval.semitones) % 12
        return self.get_closest_tone(_new_note_id, 'desc')

    def __str__(self):
        return self.tone + self.accidental


class Interval():
    def __init__(self, interval):
        try:
            self.semitones = {
                'P1': 0,
                'm2': 1,
                'M2': 2,
                'm3': 3, 'A2': 3, 'd3': 3,
                'M3': 4, 'd4': 4,
                'P4': 5, 'A3': 5,
                'A4': 6, 'd5': 6,
                'P5': 7, 'd6': 7,
                'm6': 8, 'A5': 8,
                'M6': 9, 'd7': 9,
                'm7': 10, 'A6': 10,
                'M7': 11, 'd8': 11,
                'P8': 12, 'A7': 12,
            }[interval]
        except:
            raise Exception('Could not parse the interval.')
        self.name = interval[0]
        self.number = int(interval[1])


if __name__ == '__main__':
    add = Note('D#') - Interval('M3')
    print add
