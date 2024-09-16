output "api_gateway_endpoint" {
  description = "The endpoint URL of the API Gateway"
  value       = aws_api_gateway_deployment.main.invoke_url
}

output "api_gateway_stage" {
  description = "The stage name of the API Gateway deployment"
  value       = aws_api_gateway_stage.main.stage_name
}

output "database_connection_string" {
  description = "The connection string for the main database"
  value       = "postgresql://${aws_db_instance.main.username}:${aws_db_instance.main.password}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.name}"
  sensitive   = true
}

output "read_replica_connection_string" {
  description = "The connection string for the read replica database"
  value       = "postgresql://${aws_db_instance.read_replica.username}:${aws_db_instance.read_replica.password}@${aws_db_instance.read_replica.endpoint}/${aws_db_instance.read_replica.name}"
  sensitive   = true
}

output "main_storage_bucket_name" {
  description = "The name of the main storage bucket"
  value       = aws_s3_bucket.main.id
}

output "backup_storage_bucket_name" {
  description = "The name of the backup storage bucket"
  value       = aws_s3_bucket.backup.id
}

output "compute_instance_public_ip" {
  description = "The public IP address of the main compute instance"
  value       = aws_instance.main.public_ip
}

output "compute_instance_private_ip" {
  description = "The private IP address of the main compute instance"
  value       = aws_instance.main.private_ip
}

output "compute_instance_id" {
  description = "The ID of the main compute instance"
  value       = aws_instance.main.id
}

# HUMAN ASSISTANCE NEEDED
# The following outputs may need to be adjusted based on the specific resources created in the Terraform configuration.
# Please review and modify as necessary to match the actual resources defined in your infrastructure.

output "lambda_function_name" {
  description = "The name of the main Lambda function"
  value       = aws_lambda_function.main.function_name
}

output "cloudfront_distribution_domain" {
  description = "The domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.main.domain_name
}

output "vpc_id" {
  description = "The ID of the main VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = aws_subnet.private[*].id
}