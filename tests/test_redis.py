import redis
r = redis.Redis(host='localhost2', port=6379, db=0)
r.set('foo', 'bar')
# print(str(r.get('foo')))
# print(r.get('bar'))
