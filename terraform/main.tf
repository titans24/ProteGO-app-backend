provider "google" {
  credentials = file("anna-dev.json")
  project     = "anna-dev-272212"
  region      = "europe-west3"
}
