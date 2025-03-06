"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-19810.c283.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19810,
    decode_responses=True,
    username="default",
    password="IoLEiix55UFPROIFu9u2PQpe9L1R53Yl",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

print(r.ping())
print(r.set('my_name','LY'))
print(r.get('my_name'))
print(r.exists('my_name'))
print(r.exists('random123'))
print(r.delete('my_name'))
print(r.exists('my_name'))