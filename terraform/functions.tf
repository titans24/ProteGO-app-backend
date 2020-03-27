resource "google_storage_bucket" "functions" {
  name = "functions-source"
}

resource "google_storage_bucket_object" "archive-register" {
  name   = "index.zip"
  bucket = google_storage_bucket.functions.name
  source = "./path_to_code"
}

resource "google_cloudfunctions_function" "register" {
  name        = "register"
  runtime     = "nodejs10"

  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.archive-register.name
  entry_point           = "main"
}

resource "google_cloudfunctions_function_iam_member" "invoker-register" {
  project        = google_cloudfunctions_function.register.project
  region         = google_cloudfunctions_function.register.region
  cloud_function = google_cloudfunctions_function.register.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

# -----------------------------------------------------

resource "google_storage_bucket_object" "archive-process" {
  name   = "index2.zip"
  bucket = google_storage_bucket.functions.name
  source = "./path_to_code"
}

resource "google_cloudfunctions_function" "process" {
  name        = "process"
  runtime     = "nodejs10"

  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.archive-process.name
  entry_point           = "main"    
}

resource "google_cloudfunctions_function_iam_member" "invoker-process" {
  project        = google_cloudfunctions_function.process.project
  region         = google_cloudfunctions_function.process.region
  cloud_function = google_cloudfunctions_function.process.name
  
  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
