#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache


class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write('summer storage!')


class SetHandler(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    value = self.request.get('value')
    ret = 'true' if memcache.set(key, value) else 'false'
    callback = self.request.get('callback')
    if callback:
      ret = callback+'('+ret+')'
    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(ret)


class GetHandler(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    ret = memcache.get(key)
    ret = '"'+ret+'"' if ret else 'null'

    callback = self.request.get('callback')
    if callback:
      ret = callback+'('+ret+')'
    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(ret)


class DeleteHandler(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    ret = 'true' if (memcache.delete(key) == 2) else 'false'
    callback = self.request.get('callback')
    if callback:
      ret = callback+'('+ret+')'
    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(ret)


def main():
  application = webapp.WSGIApplication(
    [
      ('/', MainHandler),
      ('/set', SetHandler),
      ('/get', GetHandler),
      ('/delete', DeleteHandler)],
    debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
