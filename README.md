This is the code from the talk _Unmasking Data Leaks: A Guide to Finding, Fixing, and Preventing_ presented at BSides SATX 2019.

# Usage

After cloning the repository, you need to install the requirements:

```
pip install -r requirements.txt
```

## Online Usage

To gather live data, you'll need to uncomment `scanner.py` to import the proper libraries:

```python
# For a real use-case you would use:
#
from censys.ipv4 import CensysIPv4
from elasticsearch import Elasticsearch
#
# from offline.censys.ipv4 import CensysIPv4
# from offline.elasticsearch import OfflineElasticsearch
```

## Offline Usage

The script was developed to support a conference environment, where network access wasn't guaranteed. To that end, we've created the ability to cache data offline, and load that data from the filesystem.

The first step in this process is to gather the data. To do this, we have a script called `bootstrap.py`. Here's the usage:

```
python bootstrap.py -h
usage: bootstrap.py [-h] --api-id API_ID --api-secret API_SECRET

Gathers open Elasticsearch instances from Censys, storing the data offline

optional arguments:
  -h, --help            show this help message and exit
  --api-id API_ID       The Censys API ID (required)
  --api-secret API_SECRET
                        The Censys API secret (required)
```

This will gather data in the `offline/data/` folder.

## Scanner Usage

To scan Censys for open Elasticsearch instances, you can use `scanner.py`. Here's the usage:

```
python scanner.py -h
usage: scanner.py [-h] --api-id API_ID --api-secret API_SECRET

Gathers open Elasticsearch instances from Censys, storing the results in a CSV
file

optional arguments:
  -h, --help            show this help message and exit
  --api-id API_ID       The Censys API ID (required)
  --api-secret API_SECRET
                        The Censys API secret (required)
```

This will create a file called `elasticsearch_instances.csv` containing the CSV results for each discovered Elasticsearch instance.

# Notes

While open Elasticsearch instances are inherently public, this code only gathers index names, field names, and record counts in order to avoid gathering the records themselves.

As data leaks are discovered, it's recommended to contact the owner for remediation.
