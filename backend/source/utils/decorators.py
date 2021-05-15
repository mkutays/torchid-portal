import json
from functools import wraps

from rest_framework import serializers


def validate(serializer: serializers.Serializer):
    def deco_validate(func):
        @wraps(func)
        def func_validate(*args, **kwargs):
            def error_messages(error_dict):
                err_list = [
                    f"{err_key}: {msg}" for err_key in error_dict for msg in error_dict[err_key]]
                return {"messages": err_list}
            request = args[0]
            data = request.GET if request.GET else json.loads(request.body)
            srz = serializer(data=data)
            valid = srz.is_valid()
            if not valid:
                message = error_messages(srz.errors)
                raise serializers.ValidationError(message)
            return func(*args, **kwargs)
        return func_validate
    return deco_validate
