output "vpc_id" {
  description = "The ID of the custom VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_id" {
  description = "The ID of the public subnet"
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "The ID of the web security group"
  value       = aws_security_group.web.id
}

output "ec2_instance_id" {
  description = "The ID of the provisioned EC2 instance"
  value       = aws_instance.web_server.id
}

output "ec2_public_ip" {
  description = "Public IPv4 address of the EC2 web server"
  value       = aws_instance.web_server.public_ip
}

output "s3_bucket_name" {
  description = "The name of the provisioned S3 bucket"
  value       = aws_s3_bucket.demo_storage.bucket
}

output "s3_bucket_arn" {
  description = "The ARN of the provisioned S3 bucket"
  value       = aws_s3_bucket.demo_storage.arn
}
