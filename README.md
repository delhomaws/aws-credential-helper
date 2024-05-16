# Access dev organization environments by jump roles

## Prerequisites

Before using this script, make sure you have the following prerequisites:

1. Boto3: Install the Boto3 library using pip:

```bash
pip install boto3 requests urllib3 subprocess32 pyperclip argparse
```

1. The .aws/config file should have:

* the **jump_profile** should be the account that is allowed to assume the target role
* Feel free to change the profile name

```ini
[profile jump-account]
output = json
region = eu-central-1
role_arn = arn:aws:iam::************:role/aws-consultant
source_profile = jump_profile
```

## Usage

To use the AWS Role Jump Script, follow the steps below:

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script with the desired options and arguments using the following command structure:

```bash
python aws-login.py --profile <AWS_PROFILE> --target <AWS_ACCOUNT_ID> --role <ROLE_NAME> [--firefox] [--chrome] [--clipboard]
```

Where:
   * `--profile <AWS_PROFILE>` (Required): Specify the AWS profile name to use for authentication. This is the profile in your AWS configuration (`~/.aws/config`) that contains the necessary credentials for assuming roles.
   * `--target <AWS_ACCOUNT_ID>` (Required): Specify the AWS account ID of the target account to assume the role in.
   * `--role <ROLE_NAME>` (Required): Specify the role you have to assume into the target account
   * `--firefox` (Optional): Include this flag to open the AWS Management Console sign-in URL in a new Firefox window.
   * `--chrome` (Optional): Include this flag to open the AWS Management Console sign-in URL in a new Chrome instance.
   * `--clipboard` (Optional): Include this flag to copy the AWS Management Console sign-in URL to the clipboard.
   * `--cli` (Optional): Include this flag to open a bash terminal session to the target account

1. The script will perform the following actions based on the provided options:

    * Assume the specified IAM role using the provided profile and target account.
    * Generate a sign-in token for the assumed role's credentials.
    * Create the AWS Management Console sign-in URL.
    * Perform the selected actions: opening in Firefox or copying to the clipboard.

## Examples

## Here are some example commands to run the script

* To assume the role and open the sign-in URL in Firefox:

```bash
python aws-login.py --profile my-aws-profile --target ************ --role admin --firefox
```

* To assume the role and open the sign-in URL in Chrome:

```bash
python aws-login.py --profile my-aws-profile --target ************ --role admin --chrome
```

* To assume the role and copy the sign-in URL to the clipboard:

```bash
python aws-login.py --profile my-aws-profile --target ************ --role admin --clipboard
```

* To assume the role, open the sign-in URL in Firefox, and copy it to the clipboard:

```bash
python aws-login.py --profile my-aws-profile --target ************ --role admin --firefox --clipboard
```

* To assume the role, open the sign-in URL in Firefox, in a container:

```bash
python aws-login.py --profile my-aws-profile --target ************ --firefox --container MyCOntainer
```

* zsk alias samples:
  
```bash
alias console='python ~/.../aws-login.py --profile auth-profile --role admin'
alias console-mngt='console --target ***********'
alias console-other-account='console --target *********** --firefox --container MyContainer'

```

## Important Notes

* Depending on your system and Firefox installation location, you may need to update the `firefox_path` variable in the script to point to the correct Firefox executable
