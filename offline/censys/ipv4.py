from offline.store import OfflineStore


class OfflineIPv4():
    def __init__(self, api_id="", api_secret=""):
        self.api_id = api_id
        self.api_secret = api_secret
        self.provider = 'censys'
        self.store = OfflineStore(self.provider, self.api_id)

    def search(self, query, page=1):
        """Returns cached search query results.

        Arguments:
            query {str} -- The query to execute
        """
        return self.store.load_results('search', query, page=page)


def CensysIPv4(api_id="", api_secret=""):
    """A simple wrapper that returns either offline Censys data, or a real
    Censys client.

    To use offline data, set the api_id to "offline".

    Arguments:
        api_id {str} -- The API ID
        api_secret {str} -- The API secret
    """
    if api_id == 'offline':
        return OfflineIPv4(api_id=api_id, api_secret=api_secret)

    from censys.ipv4 import CensysIPv4
    return CensysIPv4(api_id=api_id, api_secret=api_secret)