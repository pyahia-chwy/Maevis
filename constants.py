

#CUSTOMIZABLE
HOST = '' #Vertica DB Server
TARGET_PORT = 5433 #Database Port
LOCAL_PORT = 7432 #Proxy; Port ODBC/JDBC would connect to
_CACHE_LOCATION = 'NOSQL' #|'MEMORY'

AWS_ACCESS_KEY = None
AWS_SECRET_KEY = None
AWS_REGION = None

CACHE_TABLE_NAME = "cache_table_log"
QUERY_CACHE_NAME = "query_cache"

MAX_RESULT_SIZE = 380000

#THIS AFFECTS AWS BILLING. Play with these Wisely. Note this will impact your capacity.
QUERY_CACHE_NAME_WRITE_THROUGHPUT  = 15
QUERY_CACHE_NAME_READ_THROUGHPUT = 15
CACHE_TABLE_NAME_WRITE_THROUGHPUT = 15
CACHE_TABLE_NAME_READ_THROUGHPUT = 15

#NON-CUSTOMIZABLE
_END_PATTERN = b"\x05T" 
_END_JDBC_PATTERN = b"\x05I"
_RESPONSE_ORD = 84 
_REQUEST_ORD = 81 

if _CACHE_LOCATION == "NOSQL":
    import keyring
    if not AWS_ACCESS_KEY:
        AWS_ACCESS_KEY = keyring.get_password("AWS_ACCESS_KEY", "VQC")
    if not AWS_SECRET_KEY:
        AWS_SECRET_KEY = keyring.get_password("AWS_SECRET_KEY", "VQC")
    if not AWS_REGION:
        AWS_REGION = keyring.get_password("AWS_REGION", "VQC")
    

