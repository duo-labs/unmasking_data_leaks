from censys.ipv4 import CensysIPv4
from elasticsearch import Elasticsearch
from offline.store import OfflineStore

import argparse
import json
"""bootstrap.py

This file was used to preload the data from Censys into offline/data, to avoid
relying on the conference network. If you want to use this for your own
applications, you can add your api_id and api_secret.
"""


def gather_instances(api_id, api_secret):
    api = CensysIPv4(api_id=api_id, api_secret=api_secret)
    query = 'protocols:"9200/elasticsearch"'
    store = OfflineStore('censys', 'offline')
    filename = store._query_to_filename('search', query)
    print('Storing results in {}'.format(filename))
    with open('offline/data/{}'.format(filename), 'w') as output_file:
        results = api.search(query, max_records=1000)
        output_file.write(json.dumps(list(results), indent=4))
        return results


def gather_metadata(ip_address):
    client = Elasticsearch([ip_address])
    store = OfflineStore('elasticsearch', ip_address)
    filename = store._query_to_filename('indices', 'get')
    print('Gathering Elasticsearch data for {} and storing in {}'.format(
        ip_address, filename))
    indices = client.indices.get('*')
    for name, index in indices.items():
        try:
            index['_count'] = client.count(index=name)['count']
        except Exception as e:
            print(e)
    with open('offline/data/{}'.format(filename), 'w') as output_file:
        output_file.write(json.dumps(indices, indent=4))


def main():
    parser = argparse.ArgumentParser(
        description=
        'Gathers open Elasticsearch instances from Censys, storing the data offline'
    )
    parser.add_argument('--api-id',
                        required=True,
                        help='The Censys API ID (required)')
    parser.add_argument('--api-secret',
                        required=True,
                        help='The Censys API secret (required)')
    args = parser.parse_args()

    instances = gather_instances(args.api_id, args.api_secret)
    for instance in instances:
        gather_metadata(instance['ip'])


if __name__ == '__main__':
    main()
