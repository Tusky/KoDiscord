import pypresence


class DiscordPresence:
    _client = None
    _client_id = None
    _pipe = None
    _connected = False

    def __init__(self, client_id: int, pipe: int = 0):
        self._client_id = client_id
        self._pipe = pipe
        self.connect()

    def disconnect(self):
        """
        Disconnects from the Discord Rich Presence session.
        """
        if self._connected:
            self._connected = False
            self._client.close()

    def connect(self):
        """
        Connects to a Discord Rich Presence session.
        """
        if not self._connected:
            self._client = pypresence.Presence(
                self._client_id,
                pipe=self._pipe
            )
            self._connected = True
            self._client.connect()

    def update_status(self, state: str, details: str):
        """
        Updates the status of the Discord Rich Presence.
        """
        if self._connected:
            self._client.update(state=state, details=details)
