from twisted.internet import protocol, reactor
from constants import LOCAL_PORT
from vq_protocol import ServerProtocol


if __name__ == '__main__':
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    reactor.listenTCP(LOCAL_PORT, factory)
    reactor.run()
    