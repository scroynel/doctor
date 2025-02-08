from django.core.cache import cache

def get_data(received_data):
    data = cache.get('my_data')
    print('data1 cache', data)
    if data is None:
        # Retrieve data from the database or another source
        data = received_data
        print('data2 not cache', data)
        cache.set('my_data', data, timeout=60)  # Cache for 1 minute
    return data