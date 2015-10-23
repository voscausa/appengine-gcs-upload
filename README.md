# appengine-gcs-upload
Direct upload (form POST) to GCS using a signed url and a policy document.
Docs: [https://cloud.google.com/storage/docs/xml-api/post-object]

App Engine is used to create a form with a signed url and process the GCS callback when the file upload was successful.

Appengine `app_identity.sign_blob()` makes is very easy to create a signed url. 

![example](/static/direct-gcs-upload.png)
