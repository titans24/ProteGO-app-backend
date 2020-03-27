resource "google_storage_bucket" "files-source" {
  name          = "files-source"
  location      = "europe-west3"
}
resource "google_storage_bucket" "files-success" {
  name          = "files-success"
  location      = "europe-west3"
}
resource "google_storage_bucket" "files-errors" {
  name          = "files-errors"
  location      = "europe-west3"
}
resource "google_storage_bucket" "internal-data" {
  name          = "internal-data"
  location      = "europe-west3"
}
resource "google_storage_bucket" "danger-zones" {
  name          = "danger-zones"
  location      = "europe-west3"
}
