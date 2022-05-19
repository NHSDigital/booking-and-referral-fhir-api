-include .env

tf_opt=
tf_state=-backend-config="key=infra"
tf_vars=

tf_cmd = AWS_PROFILE=$(aws_profile) terraform $(tf_opt)

init:
	$(tf_cmd) init $(tf_state) $(tf_vars)

plan:
	$(tf_cmd) plan

apply:
	 $(tf_cmd) apply -auto-approve

destroy:
	$(tf_cmd) destroy
