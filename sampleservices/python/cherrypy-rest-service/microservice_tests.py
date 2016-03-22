# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.test import helper

from microservice import Service

class ServiceTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(Service())
        
    def test_retrieve_resource(self):
        self.getPage('/')
        self.assertBody('Hello!')
