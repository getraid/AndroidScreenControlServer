from bottle import Bottle, template
import atexit
import sys


class Webserver:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

        atexit.register(self.OnExit)

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/test/<var>', callback=self._test)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    def _index(self):
        return 'Hello fellas'

    def _test(self, var="var"):
        return template('Output:  {{var}}', var=var)

    def OnExit(self):
        print("Webserver is closing...")
        self._app.close()
