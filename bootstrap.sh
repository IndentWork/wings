az ad sp create-for-rbac \
  --name wings-github-actions-sp \
  --role Contributor \
  --scopes /subscriptions/"$SUBSCRIPTION_ID"
