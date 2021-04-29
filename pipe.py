#!/usr/bin/python3

from datetime import datetime, timedelta
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pytz

# Fill in with your personal access token, org URL, and project
PERSONAL_ACCESS_TOKEN = ''
ORGANIZATION_URL = ''
PROJECT = ''

def main():
    # Set historical time frame in days
    days_to_subtract = 1
    d = datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=days_to_subtract)

    # Create a connection to the org
    credentials = BasicAuthentication('', PERSONAL_ACCESS_TOKEN)
    connection = Connection(base_url=ORGANIZATION_URL, creds=credentials)

    # Get a client
    core_client = connection.clients_v6_0.get_build_client()

    # Get builds for pipeline
    get_build_response = core_client.get_builds(PROJECT)

    while get_build_response is not None:
        for build in get_build_response:
            # Omit current running builds with no finish time yet
            if build.finish_time is not None:
                if d < build.finish_time:
                    # Get logs info from build
                    get_build_log_response = core_client.get_build_logs(PROJECT, build.id)
                    while get_build_log_response is not None:
                        for log in get_build_log_response:
                            # Get logs lines from logs from log info
                            get_build_log_lines_response = core_client.get_build_log_lines(PROJECT, build.id, log.id)
                            while get_build_log_lines_response is not None:
                                for log_lines in get_build_log_lines_response:
                                    # Outputs logs within given historical timeframe for project
                                    print(log_lines)


if __name__ == '__main__':
    main()
