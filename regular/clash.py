"""
clash.py
the Clash of Clans module
"""

import requests
import arrow
from regular import creds
from regular.config import TIMEZONE

API_LINK = "https://api.clashofclans.com/v1"
CLAN_CODE = "%232PCQCRQVY"


def _get_time_until(datetime_iso):
    """
    :param datetime_iso: ISO 8601 - formatted datetime from API response
    :return: string denoting the time until this event
    """
    return arrow.get(datetime_iso).to(TIMEZONE).humanize(
        arrow.utcnow().to(TIMEZONE),
        granularity=["hour", "minute"])


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
        """
        :return: String of members or error details
        """
        response = self._make_request(
            API_LINK + "/clans/{}/members".format(CLAN_CODE))
        if response is None:
            # error sending response
            return "Response Error"
        members = response.get("items")
        if response is None:
            return "Response Error"
        if len(members) == 0:
            return "Nobody is in our clan!"
        message = "\n --- Clan members --- \n"
        for memb in members:
            message += "Name: {}, Trophies: {}, Donations: {}\n".format(
                memb["name"],
                memb["trophies"],
                memb["donations"])
        return message

    def get_war_details(self):
        """
        :return: String of current war details or error details
        """
        response = self._make_request(
            API_LINK + "/clans/{}/currentwar".format(CLAN_CODE))
        if response is None:
            return "Response Error"
        if response["state"] == "inWar":
            message = "War is live! {} - {} VS {} - {}\nWar ends {}".format(
                        response["clan"]["name"],
                        response["clan"]["stars"],
                        response["opponent"]["name"],
                        response["opponent"]["stars"],
                        _get_time_until(response["endTime"]))
        elif response["state"] == "preparation":
            message = "Preparation Day ends {}".format(
                _get_time_until(response["startTime"]))
        else:
            message = "Clan not at War"
        return message
