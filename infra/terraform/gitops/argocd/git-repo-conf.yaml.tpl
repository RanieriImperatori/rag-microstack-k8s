apiVersion: v1
kind: Secret
metadata:
  name: private-repo-ranieri
  namespace: gitops
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  url: https://${GITHUB_USERNAME}@github.com/RanieriImperatori/rag-microstack-k8s.git
  password: ${GITHUB_TOKEN}
  username: ${GITHUB_USERNAME}