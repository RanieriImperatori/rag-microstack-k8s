variable "argocd_name" {
  type    = string
  default = "argocd"
}

variable "argocd_repository" {
  type        = string
  default     = "https://argoproj.github.io/argo-helm"
  description = "The URL of the Helm chart repository."
}

variable "argocd_chart" {
  type        = string
  default     = "argo-cd"
  description = "The name of the Helm chart to install."
}

variable "argocd_namespace" {
  type        = string
  default     = "gitops"
  description = "The namespace in which to install the Helm chart."
}

variable "argocd_create_namespace" {
  type        = bool
  default     = true
  description = "Whether to create the namespace if it does not exist."
}

variable "argocd_version" {
  type        = string
  default     = "7.8.14"
  description = "The version of the Helm chart to install."
}

variable "argocd_verify" {
  type        = bool
  default     = false
  description = "Whether to verify the chart before installation."
}