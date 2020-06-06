import re
from constants import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, _CACHE_LOCATION


#QUERY_CACHE_PATTERN
_SOURCE_RE_PATTERN = "\s+(?:FROM|JOIN)\s+(\w+\.\w+)" #pattern to retrieve list of tables in query

class QueryCache:
    
    def __init__(self):
        self.dict_cache = {}          
        self.query_logs = []
        self.source_queries = {}
        self.nosql_cache_keys = []
        if _CACHE_LOCATION == 'NOSQL':
            from dynamodb_request_manager import DydbRequestManager
            self.nosql_client = DydbRequestManager(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION)

    def cache_access(self, key):
        if _CACHE_LOCATION == 'MEMORY':
            return self.dict_cache[key]
        elif _CACHE_LOCATION == 'NOSQL':
            return self.nosql_client.retrieve_from_query_cache(key)
    
    @property
    def cache_keys(self):
        if _CACHE_LOCATION == 'MEMORY':
            return self.dict_cache.keys()
        elif _CACHE_LOCATION == 'NOSQL':
            return self.nosql_cache_keys
        else:
            return ["785dcdffd13c8ff6e539f3ac6d9a50c1"] #test key
            
    def parse_query(self, msg):
        matches = re.findall(_SOURCE_RE_PATTERN, msg.message)
        return matches
                
    def write_to_cache(self, msg, responses):
        self.query_logs.append(msg.message)
        
        if _CACHE_LOCATION == 'MEMORY':
            self.dict_cache[msg.key] = responses
        elif _CACHE_LOCATION == 'NOSQL':
            self.nosql_cache_keys.append(msg.key)
            self.nosql_client.load_query_cache(msg.key, responses)
            data = self.parse_query(msg)
            if data:
                self.nosql_client.load_table_key_mapping(data, msg.key)
    
    
