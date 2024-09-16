# Main Terraform configuration file for Microsoft Word infrastructure

# Provider configuration for Google Cloud Platform
provider "google" {
  project = var.project_id
  region  = var.region
}

# Resource definitions for core infrastructure components

# VPC network
resource "google_compute_network" "word_network" {
  name                    = "word-network"
  auto_create_subnetworks = false
}

# Subnet for Word services
resource "google_compute_subnetwork" "word_subnet" {
  name          = "word-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.word_network.id
}

# Firewall rule to allow internal communication
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal"
  network = google_compute_network.word_network.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  source_ranges = ["10.0.0.0/24"]
}

# Cloud Storage bucket for document storage
resource "google_storage_bucket" "word_documents" {
  name     = "word-documents-${var.project_id}"
  location = var.region
}

# Cloud SQL instance for metadata storage
resource "google_sql_database_instance" "word_metadata" {
  name             = "word-metadata-instance"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

# Module imports for specific service configurations
module "word_editor_service" {
  source = "./modules/word_editor"
  # Add necessary variables
}

module "word_collaboration_service" {
  source = "./modules/word_collaboration"
  # Add necessary variables
}

module "word_auth_service" {
  source = "./modules/word_auth"
  # Add necessary variables
}

# HUMAN ASSISTANCE NEEDED
# The following block requires review and potential customization:
# - Verify if additional core infrastructure components are needed
# - Ensure that the module imports align with the actual module structure
# - Review and adjust resource configurations based on specific requirements