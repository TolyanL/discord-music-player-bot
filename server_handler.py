from song_queue import Queue


class ServerList:
    def __init__(self):
        self.guilds = dict()

    def get_guild(self, guild_id: int) -> Queue:
        guild = self.guilds.get(guild_id)
        if not guild:
            self.add_guild(guild_id)
            return self.guilds.get(guild_id)
        return guild

    def add_guild(self, guild_id: int):
        return self.guilds.update({guild_id: Queue()})

    def __len__(self):
        return len(self.guilds)
