
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from com.listener import COMPort
from utils.decorators import validate
from .serializers import ComSetSerializer


@api_view(["GET"])
def com_list(request):
    response = COMPort.list_all()
    return Response(response)


@api_view(["POST"])
@validate(ComSetSerializer)
def com_set(request):
    port = request.data["port"]
    if not COMPort().is_alive():
        COMPort().com_port = port
        msgs = [f"COM Port successfully set as [{port}]"]
        status_code = status.HTTP_200_OK
    else:
        msg1 = f"COM Port already listening for [{COMPort().com_port}]"
        msg2 = "Please disconnect before you configure!"
        msgs = [msg1, msg2]
        status_code = status.HTTP_400_BAD_REQUEST
    response = {"messages": msgs}
    return Response(response, status=status_code)


@api_view(["POST"])
def com_disconnect(request):

    if COMPort().is_alive():
        COMPort().stop()
        msgs = [
            "Your request has been recieved. Connection will be shutdown gracefully."]
        status_code = status.HTTP_202_ACCEPTED
    else:
        msgs = ["Connection already has been closed."]
        status_code = status.HTTP_200_OK

    response = {"messages": msgs}
    return Response(response, status=status_code)


@api_view(["GET"])
def com_status(request):
    response = {"status": COMPort().is_alive(), "port": COMPort().com_port}
    return Response(response)
