variable "minikube_driver" {
  type        = string
  description = "Driver used to run Minikube"
  default     = "docker"
}

variable "minikube_cluster_name" {
  type        = string
  description = "Name of the cluster to be used"
  default     = "rag-microstack-k8s"
}

variable "minikube_addons" {
  type        = list(string)
  description = "Additional cluster configuration addons"
  default     = [
    "default-storageclass",
    "storage-provisioner",
    "ingress",
    "metrics-server"
  ]
}

variable "minikube_cpus" {
  type        = number
  description = "Number of CPUs to use"
  default     = 6
}

variable "minikube_memory" {
  type        = string
  description = "Amount of memory to allocate"
  default     = "6g"
}


# variable "aws_cluster_name" {
#   type        = string
#   description = "Name of the cluster to be used"
#   default     = "k8s-aws"
# }

# variable "aws_cidr_block" {
#   type        = string
#   description = "CIDR block value for the VPC - 10.0.0.0/16"
#   default     = "10.0.0.0/16"
# }

# variable "aws_access_key" {
#   type        = string
#   description = "Access key value used"
#   sensitive   = true
#   default     = ""
# }

# variable "aws_secret_key" {
#   type        = string
#   description = "Secret key value used for access"
#   sensitive   = true
#   default     = ""
# }

# variable "aws_cluster_version" {
#   type        = string
#   description = "Version of the Kubernetes cluster"
#   default     = "1.30"
# }

# variable "aws_private_subnets" {
#   type        = list(string)
#   description = "List of private subnets"
#   default     = ["10.0.1.0/24", "10.0.2.0/24"]
# }

# variable "aws_public_subnets" {
#   type        = list(string)
#   description = "List of public subnets"
#   default     = ["10.0.4.0/24", "10.0.5.0/24"]
# }

# variable "aws_lista_az" {
#   type        = list(string)
#   description = "List of availability zones to use"
#   default     = ["us-east-1a", "us-east-1b"]
# }