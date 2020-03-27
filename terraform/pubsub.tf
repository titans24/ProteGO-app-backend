resource "google_pubsub_topic" "success" {
  name = "streaming-success"

  message_storage_policy {
    allowed_persistence_regions = [
      "europe-west3",
    ]
  }
}

resource "google_pubsub_topic" "error" {
  name = "streaming-error"

  message_storage_policy {
    allowed_persistence_regions = [
      "europe-west3",
    ]
  }
}
