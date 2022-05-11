import functools, time

from flask import jsonify, make_response


def api_response(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time        
        response = dict(result=result, time_ms=int(run_time*1000))
        value = make_response(jsonify(response))
        return value
    return f