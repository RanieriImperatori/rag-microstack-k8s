
output "cluster_name" {
  description = "Displays the name of the cluster tha was created"
  value = minikube_cluster.cluster_k8s.cluster_name
}