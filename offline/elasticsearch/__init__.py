from offline.store import OfflineStore


class OfflineIndexClient():
    def __init__(self, store):
        self.store = store

    def get(self, pattern):
        """Return the indices created in an Elasticsearch instance.

        Arguments:
            pattern {str} -- The pattern to match against (recommend "*")
        """
        return self.store.load_results('indices', 'get', default={})


class OfflineElasticsearch():
    def __init__(self, hosts):
        """Creates a new instance of the offline Elasticsearch datastore.

        Arguments:
            hosts {list} -- A list of IP addresses mapping to ES hosts.
        """
        self.store = OfflineStore('elasticsearch', hosts[0])
        self.hosts = hosts
        self.indices = OfflineIndexClient(self.store)

    def count(self, requested_indices):
        """Return the number of documents in a given index.

        Note: While this function normally expects a list of indices, in this
        case only the first will be processed.

        Arguments:
            requested_index {list} -- A list of indices to get the count for.
        """
        indexes = self.indices.get("*")
        return indexes[requested_indices[0]]['_count']
