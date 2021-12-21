#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:

    imgcpd2e.py [options]

Description:

Options

Examples

Author:

    bsg <sg.byeon1@gmail.com>
"""

import os
import boto3
import base64

#IMAGE_TAGS = []

def get_ecr_repo(ecr_client, account_id):
    paginator = ecr_client.get_paginator("describe_repositories")
    for page in paginator.paginate(registryId=account_id):
        for repo in page["repositories"]:
            print(repo['repositoryName'])

def docker_login_to_ecr(ecr_client, account_id):
    token = ecr_client.get_authorization_token(registryIds=[account_id])

    try:
        auth = token["authorizationData"][0]
    except (IndexErr, KeyError):
        raise RuntimeError("Unable to get authorization token from ECR")

    auth_token = base64.b64decode(auth["authorizationToken"]).decode()
    username, password = auth_token.split(":")

    print(username, password)
    #print(auth)
    print(auth["proxyEndpoint"])


def main():
    account_id = '628842917615'
    ecr_client = boto3.client('ecr')
    get_ecr_repo(ecr_client, account_id)
    docker_login_to_ecr(ecr_client, account_id)

if __name__ == '__main__':
    os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-2'
    os.environ['AWS_PROFILE'] = 'Profile1'
    main()
