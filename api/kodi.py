import requests


class Kodi:
    current_time = [0, 0, 0]
    total_time = [0, 0, 0]
    title = None
    year = None
    playing = False
    failed_connection = False

    def __init__(self, ip: str, port: int = 8080):
        self._ip = ip
        self._port = port

    def set_default(self):
        """
        Sets the default values, in case there is an error.
        """
        self.current_time = [0, 0, 0]
        self.total_time = [0, 0, 0]
        self.title = None
        self.year = None
        self.playing = False

    def update_stream_information(self):
        """
        Connects to Kodi via json-RPC, and gets the currently played media information.
        """
        try:
            r = requests.post('http://{_ip}:{_port}/jsonrpc'.format(**self.__dict__), json=[
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
        except requests.exceptions.ConnectionError:
            self.failed_connection = True
            print('Could not connect to Kodi instance.')
        else:
            self.failed_connection = False
            for j in r.json():
                if j['id'] == 'player':
                    current_time = j['result']['time']
                    total_time = j['result']['totaltime']
                    self.current_time = [current_time['hours'], current_time['minutes'], current_time['seconds']]
                    self.total_time = [total_time['hours'], total_time['minutes'], total_time['seconds']]
                    self.playing = j['result']['speed'] == 1
                elif j['id'] == 'video':
                    item = j['result']['item']
                    if item['type'] == 'movie':
                        self.title = '{title} ({year})'.format(**item)
                        self.year = item['year']
                    elif item['type'] == 'episode':
                        self.title = '{showtitle} {season}x{episode:02d}'.format(**item)
                        self.year = item['year']
                    elif item['type'] == 'unknown':
                        self.set_default()
                    else:
                        print('Unknown type: {type}'.format(type=item['type']))
                        self.set_default()

    def get_currently_playing_item(self):
        """
        Returns media information parsed from Kodi.
        :return: Information (`title`, `current_time`, `total_time`, `playing`, `year`, `failed_connection`)
        :rtype: dict
        """
        self.update_stream_information()
        return self.__dict__
