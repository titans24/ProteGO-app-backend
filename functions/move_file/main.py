import base64
import os
import logging

from google.cloud import storage


SOURCE_BUCKET = os.environ["SOURCE_BUCKET"]
DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]


def move_file(data, context):
    """This function is executed from a Cloud Pub/Sub"""
    client = storage.Client()
    message = base64.b64decode(data["data"]).decode("utf-8")
    file_name = data["attributes"]["file_name"]

    source_bucket = client.get_bucket(SOURCE_BUCKET)
    source_blob = source_bucket.blob(file_name)

    destination_bucket = client.get_bucket(DESTINATION_BUCKET)

    source_bucket.copy_blob(source_blob, destination_bucket, file_name)
    source_blob.delete()

    logging.info(
        "File '%s' moved from '%s' to '%s': '%s'",
        file_name,
        SOURCE_BUCKET,
        DESTINATION_BUCKET,
        message,
    )
