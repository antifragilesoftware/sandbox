# -*- coding: utf-8 -*-
import cherrypy

class Service(object):
    @cherrypy.expose
    def index(self):
        return "Hello!"

if __name__ == "__main__":
    cherrypy.quickstart(Service())

