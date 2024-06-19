#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    if url is None or len(url.strip()) == 0:
        return ''
    redis_store = redis.Redis()
    response_key = 'result:{}'.format(url)
    request_key = 'count:{}'.format(url)
    result = redis_store.get(response_key)
    if result is not None:
        redis_store.incr(request_key)
        return result
    result = requests.get(url).content.decode('utf-8')
    redis_store.setex(response_key, timedelta(seconds=10), result)
    return result
