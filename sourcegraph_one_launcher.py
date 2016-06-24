import json
import socket
import sys

_SOCKET_FILE = "/tmp/app.sourcegraph"

def send_request_to_socket(url):
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        message = {"type": "sourcegraph-launcher", "data": {"url": url}}
        message_json = json.dumps(message)
	try:
		sock.connect(_SOCKET_FILE)
		sock.send(bytes(message_json))
		sock.send(bytes("\f"))
	except Exception as error:
                sys.stderr.write(str(error))	    
        finally:
		sock.close()


send_request_to_socket(str(sys.argv[1]))
