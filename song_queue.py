class Queue:
    def __init__(self):
        self.songs = []
        self.pt = 0

    def add(self, element: list):
        self.songs.append(element)

    def remove(self):
        if not self.is_empty():
            song = self.songs[self.pt]
            self.pt += 1
            if self.pt > len(self.songs) / 2:
                self.songs = self.songs[self.pt :]
                self.pt = 0
            return song
        else:
            return -1

    def remove_by_index(self, index):
        return self.songs.pop(self.pt + index)

    def get_songs(self):
        return self.songs[self.pt :]

    def is_empty(self):
        return not self.songs

    def __str__(self):
        return str(self.songs[self.pt :])

    def __getitem__(self, item):
        return self.songs[item]

    def __len__(self):
        return len(self.songs)
