import re
import json


class OfflineStore():
    """An offline datastore, saving results to the local filesystem.
    """

    def __init__(self, service, api_key, directory='offline/data/'):
        self.service = service
        self.id = api_key
        self.directory = directory

    def _query_to_filename(self, endpoint, query, page=1):
        """Generates a filename slug from a query.

        Arguments:
            endpoint {str} -- The endpoint being hit (e.g. "query")
            query {str} -- The query to execute
        """
        slug = '{}-{}-{}-{}'.format(self.service, self.id, endpoint,
                                    query).lower()
        slug = re.sub('[^a-zA-Z0-9\-_\.]', '-', slug)
        slug = re.sub('[^a-zA-Z0-9]+$', '', slug)
        slug = slug + '.json'
        return slug

    def load_results(self, endpoint, query, page=1, default=[]):
        """Loads the JSON results from a local file.

        Arguments:
            endpoint {str} -- The endpoint of the service we're requesting
            query {str} -- The query sent to the endpoint
            page {int} -- The page we're requesting
            default {object} -- The default datatype to return in the case of
                missing results

        Returns:
            dict -- The parsed results
        """
        filename = self._query_to_filename(endpoint, query, page=page)
        with open(self.directory + filename, 'r') as results_file:
            results = results_file.read()
            if not results:
                return default
            return json.loads(results)