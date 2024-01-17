#!/bin/bash

template_file="credentials_template.json"
output_file="credentials.json"

# Function to prompt for input
prompt_for_input() {
    read -p "Enter a value for $1: " value
    echo "$value"
}

# Read the template file
template=$(<"$template_file")

# Iterate through the keys in the template
while IFS= read -r key; do
    # Get the value for the key from the template
    value=$(jq -r ".$key" "$template_file")
    # # Get the value for the key from the template - without jq
    # value=$(grep -oP "\"$key\": \"\K[^\"]+" "$template_file")

    # If the value is empty, prompt the user for input
    if [ -z "$value" ]; then
        new_value=$(prompt_for_input "$key")

        # Update the template with the new value
        template=$(echo "$template" | jq ".$key |= \"$new_value\"")
        # # Update the template with the new value - without jq
        # template=$(echo "$template" | sed "s/\"$key\": \".*\"/\"$key\": \"$new_value\"/")
    fi
done <<< "$(jq -r 'keys[]' "$template_file")"
# done <<< "$(grep -oP '\"[^\"]+\"' "$template_file" | tr -d '\"')" # - without jq

# Save the filled values to the output file
echo "$template" > "$output_file"

# Inform the user
echo "Credentials filled and saved to $output_file"

createdb makers-bnb
createdb makers-bnb-test
pipenv install
# pipenv install flask
# pipenv install psycopg2-binary
# pipenv install peewee
# pipenv install twilio

pipenv shell
python seed_db.py
python app.py