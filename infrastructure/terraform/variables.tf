# This file declares 13 variables. Only project_id and region are referenced
# anywhere in this configuration; the other 11 have no consumer. No variable
# declares a validation block, so Terraform checks nothing beyond the type.
# Project-wide variables
# No default, and no tfvars file is committed, so a value must be passed in.
# Five reference sites in main.tf: provider, bucket name, three module calls.
variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

# Six reference sites in main.tf: provider, subnetwork, bucket location,
# three module calls.
variable "region" {
  description = "The default region for resources in the project"
  type        = string
  default     = "us-central1"
}

# Unreferenced. This configuration declares no zonal resource.
variable "zone" {
  description = "The default zone for resources in the project"
  type        = string
  default     = "us-central1-a"
}

# Service-specific variables
# Unreferenced. This configuration declares no compute instance resource.
variable "compute_instance_type" {
  description = "The machine type for compute instances"
  type        = string
  default     = "n1-standard-1"
}

# Unreferenced. The google_storage_bucket resource in main.tf sets no
# storage_class argument, so this value never reaches the bucket.
variable "storage_class" {
  description = "The storage class for GCS buckets"
  type        = string
  default     = "STANDARD"
}

# Unreferenced. This configuration declares no Cloud SQL instance.
variable "database_tier" {
  description = "The tier for Cloud SQL instances"
  type        = string
  default     = "db-f1-micro"
}

# Environment-specific variables
# Unreferenced, and with no validation block this variable accepts any string,
# not only the dev, staging, and prod values its description names.
variable "environment" {
  description = "The deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# The three instance counts and three storage sizes below are all unreferenced.
# No resource in this configuration reads a count or a disk size.
variable "dev_instance_count" {
  description = "Number of instances to deploy in dev environment"
  type        = number
  default     = 1
}

variable "staging_instance_count" {
  description = "Number of instances to deploy in staging environment"
  type        = number
  default     = 2
}

variable "prod_instance_count" {
  description = "Number of instances to deploy in production environment"
  type        = number
  default     = 3
}

variable "dev_storage_size" {
  description = "Storage size for dev environment (in GB)"
  type        = number
  default     = 10
}

variable "staging_storage_size" {
  description = "Storage size for staging environment (in GB)"
  type        = number
  default     = 50
}

variable "prod_storage_size" {
  description = "Storage size for production environment (in GB)"
  type        = number
  default     = 100
}