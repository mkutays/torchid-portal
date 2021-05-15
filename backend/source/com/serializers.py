from rest_framework import serializers
from .listener import COMPort


class ComSetSerializer(serializers.Serializer):
    port = serializers.CharField(max_length=20)

    def validate_port(self, value):
        av_port_list = [coms["name"].lower() for coms in COMPort.list_all()]
        if value.lower() not in av_port_list:
            raise serializers.ValidationError(
                f"Selected port [{value}] is not an available option!")
        return value
