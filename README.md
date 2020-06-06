# Maevis

## REQUIREMENTS:
* Vertica DB - This is the querying/target Database. (Postgres in Progress).
* DynamoDB - This is the where cached-results are stored.There is a setting to run the cache in memory, but features will be more limited (ie, clearing specific cached queries when a table is updated).


## UTILIZATION:

#### Settings
* Paramaters are read from ./constants.py. This is where configurations for target host:port, local port, & AWS Credentails are read from. Edit these as needed.

#### Running
* Run ./service.py
* Connect your client to the host ./service.py is running from on the LOCAL_PORT from ./constants.py.

#### Clearing Full Cache
* Cache is cleared whenever the ./service.py restarts.

#### Clearing individual items
When a query is written to the cache, tables/views from the Query are written to a seperate table (`from constants import CACHE_TABLE_NAME`). This table stores each table used in the query along with the cache_key (FK to the query_cache table `from constants import QUERY_CACHE_NAME` )

To remove an item from the cache (ie, at the end of an ETL job) read the cache_keys from the `cache_table` table (scanning based on the table that is refreshed) and delete those keys from the `query_cache` table. 



