# For a real use-case you would use:
#
# from censys.ipv4 import CensysIPv4
# from elasticsearch import Elasticsearch
#
from offline.censys.ipv4 import CensysIPv4
from offline.elasticsearch import OfflineElasticsearch

import argparse
import csv


def get_results(api_id, api_secret):
    """Searches Censys for open Elasticsearch instances, returning each record
    in a generator.
    """
    query = 'protocols:"9200/elasticsearch"'
    api = CensysIPv4(api_id=api_id, api_secret=api_secret)
    for result in api.search(query):
        yield result


def process_result(ip_address):
    """Gathers the indices, mappings, and properties for an Elasticsearch
    instance.

    Arguments:
        ip_address {str} -- The IP address of the Elasticsearch instance
    """
    print('Processing instance at {}'.format(ip_address))
    client = OfflineElasticsearch([ip_address])
    indices = client.indices.get("*")
    # Each "record" is a dictionary for a given index on the Elasticsearch
    # instance.
    records = []
    for name, index in indices.items():
        try:
            num_records = client.count([name])
            mappings = index.get('mappings', {})
            for mapping_name, mapping in mappings.items():
                properties = mapping.get('properties', {}).keys()
                records.append({
                    'ip_address': ip_address,
                    'index': name,
                    'mapping': mapping_name,
                    'fields': str(list(properties)),
                    'num_records': num_records
                })
        except Exception as e:
            continue
    return records


def main():
    """Gather the Elasticsearch instances, saving the results to a CSV file.
    """
    parser = argparse.ArgumentParser(description='Gathers open Elasticsearch instances from Censys, storing the results in a CSV file')
    parser.add_argument('--api-id', required=True,
                        help='The Censys API ID (required)')
    parser.add_argument('--api-secret', required=True,
                        help='The Censys API secret (required)')
    args = parser.parse_args()

    results = get_results(args.api_id, args.api_secret)

    with open('elasticsearch_instances.csv', 'w') as instances:
        writer = csv.DictWriter(instances,
                                fieldnames=[
                                    'ip_address', 'index', 'mapping', 'fields',
                                    'num_records'
                                ])
        writer.writeheader()
        for result in results:
            records = process_result(result['ip'])
            writer.writerows(records)


if __name__ == '__main__':
    main()
