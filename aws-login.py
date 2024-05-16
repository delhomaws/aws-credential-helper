# # Open `https://mozilla.org` in a container named `MyContainer`.
# # $ firefox 'ext+container:name=MyContainer&url=https://mozilla.org'
# # Open `https://mozilla.org` in a container named `MyContainer`. If the container doesn't exist, create it using an `orange` colored `fruit` icon. Also, pin the tab.
# # $ firefox 'ext+container:name=MyContainer&color=orange&icon=fruit&url=https://mozilla.org&pinned=true'

# # Where optional OPTIONS may include any combination of:
# # 	--COLOR		color for the container (if does not exist)
# # 	--ICON		icon for the container (if does not exist)
# #   -n,	--name=NAME	container name (default: domain part of the URL)
# #   -p,	--pin		pin tab
# #   -r,	--reader	open tab in the reader mode

# # Where COLOR is one of:
# # 	--blue
# # 	--turquoise
# # 	--green
# # 	--yellow
# # 	--orange
# # 	--red
# # 	--pink
# # 	--purple

# # Where ICON is one of:
# # 	--fingerprint
# # 	--briefcase
# # 	--dollar
# # 	--cart
# # 	--circle
# # 	--gift
# # 	--vacation
# # 	--food
# # 	--fruit
# # 	--pet
# # 	--tree
# # 	--chill


import boto3
import requests
import json
import urllib.parse
import subprocess # nosec B404 - used for the purpose of the tool.
import pyperclip
import argparse
import os

def assume_role(profile_name, role_arn, session_name):
    session = boto3.Session(profile_name=profile_name)
    sts_client = session.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    return assumed_role['Credentials']

def get_signin_token(credentials):
    params = {
        'Action': 'getSigninToken',
        'Session': json.dumps({
            'sessionId': credentials['AccessKeyId'],
            'sessionKey': credentials['SecretAccessKey'],
            'sessionToken': credentials['SessionToken']
        })
    }
    request_url = 'https://signin.aws.amazon.com/federation?' + urllib.parse.urlencode(params)
    response = requests.get(request_url, timeout=10,)
    response.raise_for_status()
    return (response.json())['SigninToken']

def get_console_login_url(signin_token):
    params = {
        'Action': 'login',
        'Issuer': '',
        'Destination': 'https://console.aws.amazon.com/',
        'SigninToken': signin_token
    }
    return 'https://signin.aws.amazon.com/federation?' + urllib.parse.urlencode(params)

def open_in_firefox(url, container):
    try:
        # Path to Firefox - Update this to the path where Firefox is installed on your system
        firefox_path = '/Applications/Firefox.app/Contents/MacOS/firefox'  # For macOS
        if container == "":
            url = url
            # command = "open -a Firefox --url '{}'".format(url)
        else:
            # container = urllib.parse.quote(container)
            url = urllib.parse.quote(url)
            url = "ext+container:name={}&url={}".format(container, url)
            # command = "firefox --url 'ext+container:name={}&url={}'".format(container, url)
        
        
        # print(f'Url is: {url}')
        # print(f'Comand is: {command}')
        # Open URL in a new Firefox window
        subprocess.Popen([firefox_path, '-new-tab', url]) # nosec B603 - used for the purpose of the tool.
        # subprocess.run(command)
        
    except Exception as e:
        print(f"Error opening Firefox: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Script to assume an AWS role and perform actions like opening the AWS console in Firefox or copying the sign-in URL to the clipboard."
    )
    parser.add_argument(
        "--profile", 
        required=True, 
        help="AWS profile name to use for authentication"
    )
    parser.add_argument(
        "--target", 
        required=True, 
        help="AWS account ID of the target account to assume the role in"
    )
    
    parser.add_argument(
        "--role", 
        required=True, 
        help="IAM AWS Role to assume into the target account"
    )
    parser.add_argument(
        "--firefox", 
        help="Open the AWS Management Console sign-in URL in a new Firefox window", 
        action="store_true"
    )
    parser.add_argument(
        "--container",
         help="Open the AWS Management Console sign-in URL in a new Firefox window in the specifyed container", 
    )
    parser.add_argument(
        "--clipboard", 
        help="Copy the AWS Management Console sign-in URL to the clipboard", 
        action="store_true"
    )
    parser.add_argument(
         "--cli", 
        help="Starts a new subprocess with the creds.",
        action="store_true"
    )
    parser.add_argument(
         "--chrome", 
        help="Open the AWS Management Console sign-in URL in a new Chrome instance",
        action="store_true"
    )    
    
    args = parser.parse_args()
    profile_name = args.profile
    target_account = args.target
    target_role = args.role
    
    if args.container is None:
        container = ""
    else:
        container = args.container
        
    # Use specified credentials to assume 'Org_provisioning' role
    assumed_credentials = assume_role(
        profile_name=profile_name,
        role_arn=f'arn:aws:iam::{target_account}:role/{target_role}',
        session_name=f'{target_role}Session'
    )

    # Get the sign-in token using 'Org_provisioning' credentials
    signin_token = get_signin_token(assumed_credentials)

    # Generate the AWS Management Console sign-in URL
    console_login_url = get_console_login_url(signin_token)
    new_env = {
        "AWS_ACCESS_KEY_ID"    : assumed_credentials['AccessKeyId'],
        "AWS_SECRET_ACCESS_KEY": assumed_credentials['SecretAccessKey'],
        "AWS_SESSION_TOKEN"    : assumed_credentials['SessionToken']
    }
    
    if args.firefox:
        open_in_firefox(console_login_url, container)
        print("New tab in Firefox opened")
    if args.clipboard:
        pyperclip.copy(console_login_url)
        print("The sign-in URL has been copied to the clipboard.")
    if args.cli:
        print("Creadentials set to the current bash session")
        subprocess.Popen("bash", shell=True, env=new_env).wait() # nosemgrep: insecure-subprocess-use # nosec B605 B602 B607 - used for the purpose of the tool.
    if args.chrome:
        print("New Chrome instance opened")
        os.popen(f'mkdir -p /Users/$(whoami)/chrome-profiles/{profile_name} && 'f'open -n -a /Applications/Google\ Chrome.app "{console_login_url}" --args --user-data-dir=/Users/$(whoami)/chrome-profiles/{profile_name}') # nosemgrep: insecure-os-exec-use dangerous-system-call-tainted-env-args dangerous-system-call-audit # nosec B605 - used for the purpose of the tool.

if __name__ == "__main__":
    main()
