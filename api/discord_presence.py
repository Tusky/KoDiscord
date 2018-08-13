import pypresence

from util.error_handling import ErrorHandler


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
            try:
                self._client.connect()
            except pypresence.exceptions.InvalidPipe as e:
                ErrorHandler(e.args[0])
            else:
                self._connected = True

    def update_status(self, state: str, details: str, large_image: str, end: int = None):
        """
        Updates the status of the Discord Rich Presence.
        """
        if self._connected:
            try:
                self._client.update(state=state, details=details, large_image=large_image, end=end)
            except pypresence.exceptions.InvalidID as e:
                self._connected = False
                ErrorHandler(e.args[0])
