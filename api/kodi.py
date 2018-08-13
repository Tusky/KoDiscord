import datetime
from json import JSONDecodeError

import requests

from util.error_handling import ErrorHandler


class Kodi:
    remaining_time = None
    end_time = None
    title = None
    year = None
    playing = False
    failed_connection = False
    type = None

    def __init__(self, ip: str, port: int = 8080, username: str = None, password: str = None):
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password

    def set_default(self):
        """
        Sets the default values, in case there is an error.
        """
        self.remaining_time = None
        self.end_time = None
        self.title = None
        self.year = None
        self.playing = False
        self.type = None

    @property
    def kodi_url(self):
        """
        Returns the Kodi url to be used for the connection. Adds in authentication if applicable.

        :return: URL for the connection.
        :rtype: str
        """
        auth = ""
        if self._username and self._password:
            auth = '{_username}:{_password}@'.format(**self.__dict__)
        return 'http://{auth}{_ip}:{_port}/jsonrpc'.format(auth=auth, **self.__dict__)

    def update_stream_information(self):
        """
        Connects to Kodi via json-RPC, and gets the currently played media information.
        """
        try:
            r = requests.post(self.kodi_url, json=[
                {
                    "jsonrpc": "2.0",
                    "method": "Player.GetProperties",
                    "params": {
                        "playerid": 1,
                        "properties": [
                            "playlistid",
                            "speed",
                            "position",
                            "totaltime",
                            "time",
                            "percentage",
                            "shuffled",
                            "repeat",
                            "canrepeat",
                            "canshuffle",
                            "canseek",
                            "partymode"
                        ]
                    },
                    "id": "player"
                },
                {
                    "jsonrpc": "2.0",
                    "method": "Player.GetItem",
                    "params": {
                        "playerid": 1,
                        "properties": [
                            "title",
                            "thumbnail",
                            "file",
                            "artist",
                            "genre",
                            "year",
                            "rating",
                            "album",
                            "track",
                            "duration",
                            "playcount",
                            "dateadded",
                            "season",
                            "episode",
                            "artistid",
                            "albumid",
                            'showtitle',
                            "tvshowid",
                            "fanart"
                        ]
                    },
                    "id": "video"
                }
            ])
            for response in r.json():
                if 'error' in response:
                    ErrorHandler(response['error'].get('message', 'No message'))
                    raise requests.exceptions.ConnectionError
            if r.status_code == 401:
                ErrorHandler("Authorization has failed for user {username}. "
                             "Invalid password?".format(username=self._username))
                raise requests.exceptions.ConnectionError
        except requests.exceptions.ConnectionError:
            self.failed_connection = True
            ErrorHandler('Could not connect to Kodi instance.')
        else:
            self.failed_connection = False
            try:
                json_content = r.json()
            except JSONDecodeError:
                ErrorHandler('Faulty response ({status}): {response}'.format(status=r.status_code, response=r.text))
                json_content = []
            for j in json_content:
                if j['id'] == 'player':
                    current_time = j['result']['time']
                    total_time = j['result']['totaltime']
                    now = datetime.datetime.now()
                    self.end_time = int((now + datetime.timedelta(
                        hours=total_time['hours'] - current_time['hours'],
                        minutes=total_time['minutes'] - current_time['minutes'],
                        seconds=total_time['seconds'] - current_time['seconds']
                    )).timestamp())
                    self.remaining_time = datetime.timedelta(seconds=self.end_time - int(now.timestamp()))
                    self.playing = j['result']['speed'] == 1
                elif j['id'] == 'video':
                    item = j['result']['item']
                    self.type = item['type']
                    self.year = item.get('year', None)
                    if item['type'] == 'movie':
                        self.title = '{title} ({year})'.format(**item)
                    elif item['type'] == 'episode':
                        self.title = '{showtitle} {season}x{episode:02d}'.format(**item)
                    elif item['type'] == 'unknown':
                        self.set_default()
                    else:
                        ErrorHandler('Unknown type: {type}'.format(type=item['type']))
                        self.set_default()

    def get_currently_playing_item(self):
        """
        Returns media information parsed from Kodi.
        :return: Information (`title`, `current_time`, `total_time`, `playing`, `year`, `failed_connection`)
        :rtype: dict
        """
        self.update_stream_information()
        return self.__dict__
