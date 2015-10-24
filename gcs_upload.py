#!/usr/bin/python
# -*- coding:

from main import BaseHandler
from webapp2_extras.appengine.users import login_required
from google.appengine.api import users
from google.appengine.api import app_identity
from datetime import datetime, timedelta
import webapp2
import base64
import logging

logging.getLogger().setLevel(logging.DEBUG)
# appengine default bucket has free quota
default_bucket = app_identity.get_default_gcs_bucket_name()
# these folders can be used in the upload
bucket_folders = ['test', 'uploads']


def gcs_upload(acl='bucket-owner-read'):
    """ return GCS upload form context
        more info : https://cloud.google.com/storage/docs/xml-api/post-object
    """

    user_id = users.get_current_user().email().lower()
    google_access_id = app_identity.get_service_account_name()
    success_redirect = webapp2.uri_for('gcs_upload_ok', _full=True)
    # GCS signed upload url expires
    expiration_dt = datetime.now() + timedelta(seconds=60)

    # The security json policy document that describes what can and cannot be uploaded in the form
    policy_string = """
    {"expiration": "%s",
              "conditions": [
                  ["starts-with", "$key", ""],
                  {"acl": "%s"},
                  {"success_action_redirect": "%s"},
                  {"success_action_status": "201"},
                  {"x-goog-meta-user-id": "%s"},
              ]}""" % (expiration_dt.replace(microsecond=0).isoformat() + 'Z', acl, success_redirect, user_id)

    # sign the policy document
    policy = base64.b64encode(policy_string)
    _, signature_bytes = app_identity.sign_blob(policy)
    signature = base64.b64encode(signature_bytes)

    logging.debug('GCS upload policy : ' + policy_string)
    return dict(form_bucket=default_bucket, form_access_id=google_access_id, form_policy=policy, form_signature=signature,
                form_succes_redirect=success_redirect, form_user_id=user_id, form_folders=bucket_folders)


class GcsUpload(BaseHandler):

    @login_required
    def get(self):

        self.render_template('gcs_upload.html', title='Gcs Upload', **gcs_upload())

    @login_required
    def ok(self):
        """ GCS upload success callback """

        logging.debug('GCS upload result : %s' % self.request.query_string)
        bucket = self.request.get('bucket', default_value='')
        key = self.request.get('key', default_value='')
        key_parts = key.rsplit('/', 1)
        folder = key_parts[0] if len(key_parts) > 1 else None

        # show modal box with result
        self.render_template('gcs_upload.html', title='Gcs Upload', modal_box="show",
                             bucket=bucket, key=key, form_folder=folder, **gcs_upload())