variable "minikube_driver" {
  type        = string
  description = "Driver used to run Minikube"
}

variable "minikube_cluster_name" {
  type        = string
  description = "Name of the cluster to be used"
}

variable "minikube_addons" {
  type        = list(string)
  description = "Cluster configuration addons"
}

variable "minikube_cpus" {
  type        = number
  description = "Number of CPUs to use"
}

variable "minikube_memory" {
  type        = string
  description = "Amount of memory to allocate"
}