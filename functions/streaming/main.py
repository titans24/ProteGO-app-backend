import json
import logging
import os
import traceback

from google.api_core import retry
from google.cloud import bigquery
from google.cloud import pubsub_v1
from google.cloud import storage


PROJECT_ID = os.environ["GCP_PROJECT"]
BQ_DATASET = os.environ["BQ_DATASET"]
BQ_TABLE = BQ_DATASET["BQ_TABLE"]
ERROR_TOPIC = "projects/%s/topics/%s" % (PROJECT_ID, os.environ["ERROR_TOPIC"])
SUCCESS_TOPIC = "projects/%s/topics/%s" % (PROJECT_ID, os.environ["SUCCESS_TOPIC"])

CS = storage.Client()
PS = pubsub_v1.PublisherClient()
BQ = bigquery.Client()


def streaming(data, context):
    """This function is executed whenever a file is added to Cloud Storage"""
    bucket_name = data["bucket"]
    file_name = data["name"]
    try:
        _insert_into_bigquery(bucket_name, file_name)
        _handle_success(file_name)
    except Exception:
        _handle_error(file_name)


def _insert_into_bigquery(bucket_name, file_name):
    table_ref = BQ.dataset(BQ_DATASET).table(BQ_TABLE)
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://%s/%s" % (bucket_name, file_name)
    load_job = BQ.load_table_from_uri(
        uri, table_ref, job_config=job_config, retry=retry.Retry(deadline=60)
    )
    logging.info("Starting job {}".format(load_job.job_id))

    result = load_job.result()  # Waits for table load to complete.
    logging.info("Job finished.")

    logging.info("Loaded {} rows.".format(result.output_rows))
    if result.errors != []:
        raise BigQueryError(result.errors)


def _handle_success(file_name):
    message = "File '%s' streamed into BigQuery" % file_name
    PS.publish(SUCCESS_TOPIC, message.encode("utf-8"), file_name=file_name)
    logging.info(message)


def _handle_error(file_name):
    message = "Error streaming file '%s'. Cause: %s" % (
        file_name,
        traceback.format_exc(),
    )
    PS.publish(ERROR_TOPIC, message.encode("utf-8"), file_name=file_name)
    logging.error(message)


class BigQueryError(Exception):
    """Exception raised whenever a BigQuery error happened"""

    def __init__(self, errors):
        super().__init__(self._format(errors))
        self.errors = errors

    def _format(self, errors):
        err = []
        for error in errors:
            err.extend(error["errors"])
        return json.dumps(err)
