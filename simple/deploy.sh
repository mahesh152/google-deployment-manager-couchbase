#!/bin/sh

PARAMETERS_FILE=$1
DEPLOYMENT_NAME=$2
nodeCount=$3
serverVersion=$4
serverUrl=$5
serverUser=$6
serverPassword=$7

sed -i 's@valServerUrl@'"${serverUrl}"'@g' parameters.${PARAMETERS_FILE}.yaml
sed -i 's@valServerUser@'"${serverUser}"'@g' parameters.${PARAMETERS_FILE}.yaml
sed -i 's@valServerPassword@'"${serverPassword}"'@g' parameters.${PARAMETERS_FILE}.yaml
sed -i 's@valServerVersion@'"${serverVersion}"'@g' parameters.${PARAMETERS_FILE}.yaml
sed -i 's@valNodeCount@'"${nodeCount}"'@g' parameters.${PARAMETERS_FILE}.yaml

gcloud deployment-manager deployments create ${DEPLOYMENT_NAME} --config parameters.${PARAMETERS_FILE}.yaml
