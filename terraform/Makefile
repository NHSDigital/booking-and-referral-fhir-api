-include .env

interactionId=$(environment)

aws_profile = apim-dev
tf_cmd = AWS_PROFILE=$(aws_profile) terraform

project_name = bars
project_short_name = bars
state_bucket = $(project_name)-terraform-state
tf_state= -backend-config="bucket=$(state_bucket)"

tf_vars= -var="project_name=$(project_name)" -var="project_short_name=$(project_short_name)"

.PHONY : lock-provider workspace init plan apply clean destroy output state-list lambda-zip catch-all-zip

lock-provider:
	# Run this only when you install a new terraform provider. This will generate sha code in lock file for all platform
	echo "This may take a while. Be patient!"
	$(tf_cmd) providers lock -platform=darwin_arm64 -platform=darwin_amd64 -platform=linux_amd64 -platform=windows_amd64

workspace:
	$(tf_cmd) workspace new $(environment) || $(tf_cmd) workspace select $(environment) && echo "Switched to workspace/environment: $(environment)"

init:
	$(tf_cmd) init $(tf_state) -upgrade  $(tf_vars)

plan: workspace
	 $(tf_cmd) plan $(tf_vars)

plan-changes: workspace
	 $(tf_cmd) plan $(tf_vars) -out=plan && $(tf_cmd) show -no-color -json plan | jq -r '.resource_changes[] | select(.change.actions[0]=="update" or .change.actions[0]=="create" or .change.actions[0]=="add") | .address'

apply: workspace
	$(tf_cmd) apply $(tf_vars) -auto-approve

clean:
	rm -rf build .terraform upload-key

destroy: workspace
	$(tf_cmd) destroy $(tf_vars) -auto-approve
	$(tf_cmd) workspace select default
	$(tf_cmd) workspace delete $(environment)

output:
	$(tf_cmd) output -raw $(name)

#Make lambda zip file in /terraform/zips directory. Whenever code gets changed in lamdba_typescript directory , new zip file gets uploaded to s3. For local,you can you this make target
lambda-zip:
	cd ../lambda_typescript && \
	chmod +x ./deploy.sh && \
	./deploy.sh

#Make catch-all-lambda zip file in /terraform/zips directory. Whenever code gets changed in lamdba_typescript directory , new zip file gets uploaded to s3. For local,you can you this make target
catch-all-zip:
	cd ../catch_all_lambda && \
	chmod +x ./deploy.sh && \
	./deploy.sh

tf-%:
	$(tf_cmd) $*