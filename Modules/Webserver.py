from bottle import Bottle, ServerAdapter, template
import sys
import random


class Webserver:
    def __init__(self, server):
        self.name = str(random.randint(0, 1000))
        self._server = server
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/test/<var>', callback=self._test)

    def start(self):
        self._app.run(server=self._server)

    def _index(self):
        return 'Hello fellas'

    def _test(self, var="var"):
        return template('Output:  {{var}}', var=var)


# https://stackoverflow.com/a/16056443
# maybe replace with tornada.wsgi like this instead https://github.com/bottlepy/bottle/issues/636#issuecomment-47940562
# to fix error below? Or just use another wsgi altogether
class MyWSGIRefServer(ServerAdapter):
    server = None
    quiet = True

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(
            self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # It prints an error that the socket can't be closed
        # but I'm to stupid to find out why.
        # As far as I see it only happens when you close the server before ever went to it via the browser
        print("Webserver is closing")
        # TODO: This below could be the solution, but I need to get the self.server casted from '_MyWSGIRefServer_' to '_BaseServer_'
        # self.server.__shutdown_request = True
        self.server.server_close()
        self.server.socket.close()
