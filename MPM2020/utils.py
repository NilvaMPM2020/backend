import redis


def get_error_obj(err):
    return {'error': err}


def init_redis(host, port):
    return redis.Redis(host=host, port=port)
