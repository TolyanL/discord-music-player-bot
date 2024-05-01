class Song:
    def __init__(self, name, duration, song_url, embed_url, thumbnail=None):
        self.name = name
        self.duration = duration
        self.url = song_url
        self.embed_url = embed_url
        self.thumbnail = thumbnail

    def __str__(self):
        return self.name


class Queue:
    def __init__(self):
        self.songs = list()
        self.loop = False
        self.is_plaing = True
        self.pos = 0

    def add(self, song: Song):
        self.songs.append(song)

    def remove(self):
        if not self.is_empty():
            song = self.songs[self.pos]
            self.pos += 1
            if self.pos > len(self.songs) / 2:
                self.songs = self.songs[self.pos :]
                self.pos = 0
            return song
        else:
            return -1

    def clear_queue(self):
        return self.songs.clear()

    def remove_by_index(self, index) -> Song:
        return self.songs.pop(self.pos + index)

    def all_songs(self) -> list[Song]:
        return self.songs[self.pos :]

    def is_empty(self):
        return not self.songs

    def __str__(self):
        return str(self.songs[self.pos :])

    def __getitem__(self, song):
        return self.songs[song]

    def __len__(self):
        return len(self.songs)
