variable "aws_region" {
  type        = string
  description = "AWS region for provisioning cloud resources."
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the custom VPC."
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for the public web subnet."
  default     = "10.20.1.0/24"
}

variable "instance_type" {
  type        = string
  description = "EC2 compute instance type."
  default     = "t3.micro"
}

variable "bucket_name" {
  type        = string
  description = "Name for the demo S3 bucket."
  default     = "yatri-aadish-cloud-demo"
}

variable "environment" {
  type        = string
  description = "Environment identifier tag."
  default     = "dev"
}
