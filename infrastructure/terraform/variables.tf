# Project-wide variables
variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The default region for resources in the project"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The default zone for resources in the project"
  type        = string
  default     = "us-central1-a"
}

# Service-specific variables
variable "compute_instance_type" {
  description = "The machine type for compute instances"
  type        = string
  default     = "n1-standard-1"
}

variable "storage_class" {
  description = "The storage class for GCS buckets"
  type        = string
  default     = "STANDARD"
}

variable "database_tier" {
  description = "The tier for Cloud SQL instances"
  type        = string
  default     = "db-f1-micro"
}

# Environment-specific variables
variable "environment" {
  description = "The deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

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