#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from webapp2_extras import jinja2

# building URIs in jinja : https://webapp-improved.appspot.com/guide/routing.html?highlight=uri_for#building-uris
config = {'webapp2_extras.jinja2': {'globals': {'uri_for': webapp2.uri_for}}}


class BaseHandler(webapp2.RequestHandler):
    """ webapp2 base handler
        https://webapp-improved.appspot.com/api/webapp2_extras/jinja2.html
    """

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template, **template_args):
        # Renders a template and writes the result to the response.
        self.response.write(self.jinja2.render_template(template, **template_args))


app = webapp2.WSGIApplication([
    webapp2.Route('/gcs_upload', handler='gcs_upload.GcsUpload', name='gcs_upload'),
    webapp2.Route('/gcs_upload_ok', handler='gcs_upload.GcsUpload:ok', name='gcs_upload_ok'),
], config=config, debug=True)