#!/usr/bin/python3

import argparse
import os

from datetime import datetime, timedelta

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pytz

PAT_ENVIRON_VARNAME = 'AZURE_DEVOPS_PERSONAL_ACCESS_TOKEN'
DEFAULT_ORGANIZATION_URL = 'https://msazure.visualstudio.com'
DEFAULT_PROJECT = 'AzureRedHatOpenShift'

def main(args):
    # Set historical time frame in days
    days_to_subtract = 1
    d = datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=days_to_subtract)

    # Create a connection to the org
    credentials = BasicAuthentication('', args.personal_access_token)
    connection = Connection(base_url=args.organization_url, creds=credentials)

    # Get a client
    core_client = connection.clients_v6_0.get_build_client()

    # Get builds for pipeline
    get_builds_response = core_client.get_builds(args.project)
    if get_builds_response:
        # Note: Unfinished builds have a finish_time of None
        recent_builds = [b for b in get_builds_response if b.finish_time and d < b.finish_time]
    else:
        recent_builds = []

    for build in recent_builds:
        # Get logs info from build
        get_build_logs_response = core_client.get_build_logs(args.project, build.id)
        if get_build_logs_response:
            for log in get_build_logs_response:
                # Get logs lines from logs from log info
                get_build_log_lines_response = core_client.get_build_log_lines(args.project, build.id, log.id)
                if get_build_log_lines_response:
                    for log_lines in get_build_log_lines_response:
                        # Outputs logs within given historical timeframe for project
                        print(log_lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_personal_access_token = os.getenv(PAT_ENVIRON_VARNAME)
    parser.add_argument(
        '--organization-url', metavar='URL',
        default=DEFAULT_ORGANIZATION_URL,
        help='organization URL (default={})'.format(DEFAULT_ORGANIZATION_URL))
    parser.add_argument(
        '--personal-access-token', metavar='TOKEN',
        default=default_personal_access_token,
        help='personal access token')
    parser.add_argument(
        '--project',
        default=DEFAULT_PROJECT,
        help='project name (default={})'.format(DEFAULT_PROJECT))
    args = parser.parse_args()
    main(args)
