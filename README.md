# Maevis

## OVERVIEW:
  Maevis is a service that runs as a Proxy between your client and your target Vertica database. When a query is executed against Maevis, Maevis first checks it's query cache to see if the query has been run before. 
  If the query has not been run, it is executed against the target Vertica database--the resultset is sent back to your client and stored in a Cache Database.
  If the query has been run before, Maevis will retrieve the resultset from the Cache Database and send it back to you client.

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
* When a query is written to the cache, tables/views from the Query are written to a seperate table (`from constants import CACHE_TABLE_NAME`). This table stores each table used in the query along with the cache_key (FK to the query_cache table `from constants import QUERY_CACHE_NAME` )

* To remove an item from the cache (ie, at the end of an ETL job) read the cache_keys from the `cache_table` table (scanning based on the table that is refreshed) and delete those keys from the `query_cache` table. 

* TBD: ./py job will be created to clear a table from cache than can be executed at the end of ETL.

#### Notes:
* A query will only read from the Cache Database if the Query is identical to a previously executed query (i.e, changing a table alias on the query will result in re-reading from the target DB rather than the Cache DB).
* Maevis will only cache results that are less < 380KB as this is only intended to store data from expensive aggregated data.
* If the cache server is slower than expectations or unexpectedly fails on large reads or high usage, consider upping the AWS throughput (in ./constants.py).

