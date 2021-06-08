#! /bin/sh

CONFIG_DOMAINS_CSV_CLUSTER_TST(){
    cat tests/.domains.csv > data/domains.csv
    echo --------------------------
    cat data/domains.csv
}

SET_VARS(){
    if [ "$DEPLOYMENT" = "test" ]; then
        echo $DEPLOYMENT
        export GCLOUD_CLUSTER=$GCLOUD_CLUSTER_TEST
        export GCLOUD_ZONE=$GCLOUD_ZONE_TEST
        CONFIG_DOMAINS_CSV_CLUSTER_TST
    elif [ "$DEPLOYMENT" = "production" ]; then
        echo $DEPLOYMENT
        export GCLOUD_CLUSTER=$GCLOUD_CLUSTER_PROD
        export GCLOUD_ZONE=$GCLOUD_ZONE_PROD
    fi
}

SETUP_GCP(){
    gcloud components install kubectl --quiet
    export IMAGE_NAME=us.gcr.io/$GCLOUD_PROJECT/$BITBUCKET_REPO_SLUG:$BITBUCKET_COMMIT
    echo $GCLOUD_API_KEYFILE | base64 -d > ~/.gcloud-api-key.json
    gcloud auth activate-service-account --key-file ~/.gcloud-api-key.json
    gcloud config set project $GCLOUD_PROJECT
    gcloud auth configure-docker --quiet
    gcloud container clusters get-credentials $GCLOUD_CLUSTER \
        --zone=$GCLOUD_ZONE \
        --project $GCLOUD_PROJECT
}

CONFIG_CLOUDFLARE_AUTH_FILE(){
    echo dns_cloudflare_api_token = $CLOUDFLARE_TOKEN > letsencrypt/cloudflare.ini
    chmod 600 letsencrypt/cloudflare.ini
}

CONFIG_AWS_AUTH_FILE(){
    export AWS_CONFIG_FILE=letsencrypt/aws-config
    echo '[default]' > $AWS_CONFIG_FILE
    echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> $AWS_CONFIG_FILE
    echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> $AWS_CONFIG_FILE
    cat $AWS_CONFIG_FILE
}

CONFIG_GCP_SERVICE_ACCOUNT_FILE(){
    export GCP_SERVICE_ACCOUNT_JSON="letsencrypt/$BITBUCKET_REPO_SLUG-gcp-service-account.json"
    echo --------------------------------------------------
    echo $GCP_SERVICE_ACCOUNT_JSON
    echo "$SERVICE_ACCOUNT" > $GCP_SERVICE_ACCOUNT_JSON
    echo --------------------------------------------------
    cat $GCP_SERVICE_ACCOUNT_JSON
}

PUBLISH_IMAGE(){
    docker build . -t $IMAGE_NAME
    docker push $IMAGE_NAME
}

CREATE_CONFIGMAP(){
    export CONFIGMAP_NAME=$BITBUCKET_REPO_SLUG-configmap
    kubectl get configmap | grep "$CONFIGMAP_NAME" && kubectl delete configmap $CONFIGMAP_NAME
    kubectl create configmap $CONFIGMAP_NAME \
        --from-literal=SERVER=$SERVER \
        --from-literal=AWS_CONFIG_FILE=$AWS_CONFIG_FILE
}

CREATE_SECRET(){
    export SECRET_NAME=$BITBUCKET_REPO_SLUG-secret
    kubectl get secret | grep "$SECRET_NAME" && kubectl delete secret $SECRET_NAME
    kubectl create secret generic $SECRET_NAME \
        --from-literal=BITBUCKET_USER=$BITBUCKET_USER \
        --from-literal=BITBUCKET_PASSWORD=$BITBUCKET_PASSWORD
}

SETUP_CRONJOB(){
    export CRONJOB_YML=$(dirname $0)/ssl-certificates-cronjob.yml
    sed -i 's/REPO_NAME_TO_BE_REPLACED/'$BITBUCKET_REPO_SLUG'/g' $CRONJOB_YML
    sed -i 's/CLUSTER/'$GCLOUD_CLUSTER'/g' $CRONJOB_YML
    sed -i 's/ZONE/'$GCLOUD_ZONE'/g' $CRONJOB_YML
    sed -i 's/PROJECT_ID/'$GCLOUD_PROJECT'/g' $CRONJOB_YML
    sed -i 's/CONFIGMAP_TO_BE_REPLACED/'$CONFIGMAP_NAME'/g' $CRONJOB_YML
    sed -i 's/SECRET_TO_BE_REPLACED/'$SECRET_NAME'/g' $CRONJOB_YML
    sed -i 's/BITBUCKET_COMMIT/'$BITBUCKET_COMMIT'/g' $CRONJOB_YML
    cat $CRONJOB_YML
}


# Main code
export DEPLOYMENT=$1
SET_VARS
SETUP_GCP
CONFIG_CLOUDFLARE_AUTH_FILE
CONFIG_AWS_AUTH_FILE
CONFIG_GCP_SERVICE_ACCOUNT_FILE
PUBLISH_IMAGE
CREATE_CONFIGMAP
CREATE_SECRET
SETUP_CRONJOB
kubectl apply -f $CRONJOB_YML
