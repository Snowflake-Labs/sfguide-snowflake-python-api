import functools, time, re

from flask import jsonify, make_response


def params_valid(start_range, end_range):
    if re.search("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", start_range) and re.search("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", end_range):
        return True
    return False


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)

    
app.json_encoder = JsonEncoder


def api_response(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time        
        response = dict(result=result, time_ms=int(run_time*1000))
        value = make_response(jsonify(response))
        value.headers['Access-Control-Allow-Origin'] = '*'
        return value
    return f
