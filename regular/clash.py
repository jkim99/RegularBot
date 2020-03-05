"""
clash.py
the Clash of Clans module
"""

import requests
from regular import creds

API_LINK = "https://api.clashofclans.com/v1"
CLAN_CODE = "%232PCQCRQVY"


class CLASHOFCLANS:
    def __init__(self):
        self.request_headers = {
            "Accept": "application/json",
            "authorization": "Bearer {}".format(creds.CLASH_API_KEY)}
        self.clan_code = CLAN_CODE

    def _make_request(self, url):
        response = requests.get(url, headers=self.request_headers)
        if 200 <= response.status_code <= 299:
            return response.json()
        return None

    def get_clan_members(self):
        response = self._make_request(
            API_LINK + "/clans/{}/members".format(CLAN_CODE))
        if response is None:
            # error sending response
            return None
        return response["items"]
