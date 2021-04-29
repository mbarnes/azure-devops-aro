from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from datetime import datetime, timedelta
import pytz
    
# Fill in with your personal access token, org URL, and project
personal_access_token = ''
organization_url = ''
project = ''

# Set historical time frame in days
days_to_subtract = 1
d = datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=days_to_subtract)

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client
core_client = connection.clients_v6_0.get_build_client()

# Get builds for pipeline
get_build_response = core_client.get_builds(project)

while get_build_response is not None:
    for build in get_build_response:
        # Omit current running builds with no finish time yet
        if build.finish_time is not None:
            if d < build.finish_time:
                # Get logs info from build
                get_build_log_response = core_client.get_build_logs(project, build.id)
                while get_build_log_response is not None:
                    for log in get_build_log_response:
                        # Get logs lines from logs from log info
                        get_build_log_lines_response = core_client.get_build_log_lines(project, build.id, log.id)
                        while get_build_log_lines_response is not None:
                            for log_lines in get_build_log_lines_response:
                                # Outputs logs within given historical timeframe for project
                                print(log_lines)
                            else:
                                # All logs lines for logs have been retrieved
                                get_build_log_lines_response = None
                    else:
                        # All logs for build have been retrieved
                        get_build_log_response = None
    else:
        # All builds have been retrieved
        get_build_response = None
