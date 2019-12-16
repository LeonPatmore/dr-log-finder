
# Push to ECR
1) `docker build -t nexmo-chatapp-log-finder .`


2）`docker tag nexmo-chatapp-log-finder:latest 564623767830.dkr.ecr.eu-west-1.amazonaws.com/nexmo-chatapp-log-finder:latest`


3) `docker push 564623767830.dkr.ecr.eu-west-1.amazonaws.com/nexmo-chatapp-log-finder:latest`

4) if login expired, try `aws configure` and/or `aws ecr get-login --no-include-email` to get new token