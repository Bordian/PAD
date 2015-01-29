#!/usr/bin/python

import json
from werkzeug.wrappers import Response, Request
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.wsgi import SharedDataMiddleware


class FoodServer(object):

    def __init__(self, config=None):

        self.urlMap = Map([
            Rule('/', endpoint='root'),
            Rule('/menu', endpoint='menu'),
            Rule('/orders', endpoint='orders'),
            Rule('/orders/<order_id>', endpoint='orderID'),
            Rule('/postdata', endpoint='postdata'),
        ])

        self.menu = ['Palermo', 'Fagotta', '4 Cheeses', 'Mario',
                     'Mexican Soup', 'Cream Soup', 'Chicken Soup',
                      'Caesar', 'Poiana', 'Tuna', 'Province',
                      'Burger', 'Cheese Sticks', 'Nachos', 'Chicken Wings', 'Potato Mix',
                      'Pasta Carbonara', 'Pasta Salmon', 'Pasta Bechamel', 'Makarona po Flotski',
                      'Chicken Lasagna', 'Beef Lasagna']

        self.orders = []
                    


    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        adapter = self.urlMap.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e

    def on_root(self, request):
        if request.method == 'GET':
            return Response('Welcome to our restaurant', mimetype='text/html')
        else:
            return MethodNotAllowed()

    def on_menu(self, request):
        if request.method == 'GET':
            return Response(json.dumps(self.menu), mimetype='application/json')

    def on_orders(self, request):
        print self.orders
        if request.method == 'GET':
        
            return Response(json.dumps(self.orders), mimetype='application/json')

    def on_postdata(self, request):
        if request.method == 'POST':
            data = request.get_data()
            print json.loads(data)
            self.orders.append(json.loads(data))

            print data
        return Response('Hello there')



def create_app():
    app = FoodServer()
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    port = 54543
    interface = '0.0.0.0'
    app = create_app()
    run_simple(interface, port, app, use_debugger=True, use_reloader=True, threaded=True)
