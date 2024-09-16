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
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
}

# Module imports for specific service configurations

module "word_backend" {
  source = "./modules/word_backend"

  project_id = var.project_id
  region     = var.region
  network_id = google_compute_network.word_network.id
  subnet_id  = google_compute_subnetwork.word_subnet.id
}

module "word_frontend" {
  source = "./modules/word_frontend"

  project_id = var.project_id
  region     = var.region
  network_id = google_compute_network.word_network.id
  subnet_id  = google_compute_subnetwork.word_subnet.id
}

module "word_database" {
  source = "./modules/word_database"

  project_id = var.project_id
  region     = var.region
  network_id = google_compute_network.word_network.id
  subnet_id  = google_compute_subnetwork.word_subnet.id
}

# HUMAN ASSISTANCE NEEDED
# The following block may need adjustments based on specific requirements:
# - Review and adjust the CIDR range for the subnet
# - Confirm if additional firewall rules are needed
# - Verify if the Cloud Storage bucket configuration meets all requirements
# - Ensure that the module imports align with the actual module structures