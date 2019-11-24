import argparse

class IOTArgParse:

  def parse_args(self):
    AllowedActions = ['both', 'publish', 'subscribe']

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store", dest="host", help="Your AWS IoT custom endpoint")
    parser.add_argument("-r", "--rootCA", action="store", dest="rootCAPath", default="/home/pi/AWS_IOT_CREDS/root-CA.crt", help="Root CA file path")
    parser.add_argument("-c", "--cert", action="store", dest="certificatePath", default="/home/pi/AWS_IOT_CREDS/senseHAT.cert.pem", help="Certificate file path")
    parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", default="/home/pi/AWS_IOT_CREDS/senseHAT.private.key", help="Private key file path")
    parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
    parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                        help="Use MQTT over WebSocket")
    parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="piweather",
                        help="Targeted client id")
    parser.add_argument("-t", "--topic", action="store", dest="topic", default="senseHAT", help="Targeted topic")
    parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                        help="Operation modes: %s"%str(AllowedActions))
    
    args = parser.parse_args()

    self.host = args.host
    self.rootCAPath = args.rootCAPath
    self.certificatePath = args.certificatePath
    self.privateKeyPath = args.privateKeyPath
    self.useWebsocket = args.useWebsocket
    self.clientId = args.clientId
    self.topic = args.topic
    self.mode = args.mode

    if args.mode not in AllowedActions:
      parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
      exit(2)

    if args.useWebsocket and args.certificatePath and args.privateKeyPath:
      parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
      exit(2)

    if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
      parser.error("Missing credentials for authentication.")
      exit(2)

    # Port defaults
    if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
      self.port = 443
    if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
      self.port = 8883

