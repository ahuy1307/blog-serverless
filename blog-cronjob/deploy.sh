#!/bin/bash

RULE_NAMES=("job_expiration_rule" "job_views_rule")
REGION="ap-southeast-1"

# Prompt the user for confirmation
read -p "Delete existed rules? (y/n): " DELETERULES
if [[ $DELETERULES == "y" || $DELETERULES == "Y" ]]; then
    for RULE_NAME in "${RULE_NAMES[@]}"; do
        # List targets
        TARGET_IDS=$(aws events list-targets-by-rule --rule $RULE_NAME --region $REGION --query 'Targets[*].Id' --output text)

        # Remove targets
        if [ -n "$TARGET_IDS" ]; then
        aws events remove-targets --rule $RULE_NAME --ids $TARGET_IDS --region $REGION
        fi

        # Delete the rule
        aws events delete-rule --name $RULE_NAME --region $REGION
        echo "Deleted rule $RULE_NAME."
    done
fi
# Deploy the Serverless stack
npm run dev