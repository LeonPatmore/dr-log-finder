from configuration.configuration import Configuration
from dr_handler.dr_handler import DRHandler
from server.server import Server


def start():
    configuration = Configuration("application.yaml")
    server = Server(configuration, DRHandler)
    server.start()


if __name__ == "__main__":
    start()
