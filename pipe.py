#!/usr/bin/python3

import argparse
import errno
import io
import os
import sys
import zipfile

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

PAT_ENVIRON_VARNAME = 'AZURE_DEVOPS_PERSONAL_ACCESS_TOKEN'
DEFAULT_ORGANIZATION_URL = 'https://msazure.visualstudio.com'
DEFAULT_PROJECT = 'AzureRedHatOpenShift'
DEFAULT_PIPELINE = 'PROD - Deploy all RPs'

def safe_mkdir(path, mode=0o777):
    try:
        os.makedirs(path, mode)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def main(args):
    # Create a connection to the org
    credentials = BasicAuthentication('', args.personal_access_token)
    connection = Connection(base_url=args.organization_url, creds=credentials)

    # Get needed clients
    client_factory = connection.clients_v6_0
    pipelines_client = client_factory.get_pipelines_client()
    build_client = client_factory.get_build_client()

    # Get pipelines
    pipelines_by_name = {}
    pipelines = pipelines_client.list_pipelines(args.project)
    if pipelines:
        pipelines_by_name = {p.name: p for p in pipelines}
    try:
        pipeline = pipelines_by_name[args.pipeline_name]
    except KeyError as ex:
        print('Invalid pipeline name "{}"'.format(ex.args[0]), file=sys.stderr)
        print('Valid pipeline names:', file=sys.stderr)
        for name in sorted(pipelines_by_name):
            print('  ' + name, file=sys.stderr)
        sys.exit(2)

    # Get the corresponding build definition
    build_definition = build_client.get_definitions(
        args.project,
        name=pipeline.name,
        path=pipeline.folder).pop()

    # Get runs for pipeline
    runs_by_name = {}
    runs = pipelines_client.list_runs(args.project, pipeline.id)
    if runs:
        runs_by_name = {r.name: r for r in runs}
    if args.run_name:
        try:
            runs_by_name = {args.run_name: runs_by_name[args.run_name]}
        except KeyError as ex:
            print('Invalid run name "{}"'.format(ex.args[0]), file=sys.stderr)
            print('Valid run names:', file=sys.stderr)
            for name in sorted(runs_by_name):
                print('  ' + name, file=sys.stderr)
            sys.exit(2)

    # Get the corresponding build for each run
    for run_name in runs_by_name:
        build = build_client.get_builds(
            args.project,
            definitions=(build_definition.id,),
            build_number=run_name).pop()

        # Download and save logs from the build
        run_logs_dir = os.path.join(os.getcwd(), pipeline.name, run_name)
        safe_mkdir(run_logs_dir)
        byte_stream = io.BytesIO()
        for data in build_client.get_build_logs_zip(args.project, build.id):
            byte_stream.write(data)
        with zipfile.ZipFile(byte_stream) as zipped_logs:
            zipped_logs.extractall(run_logs_dir)


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
    parser.add_argument(
        '--pipeline', metavar='NAME', dest='pipeline_name',
        default=DEFAULT_PIPELINE,
        help='pipeline name (default={})'.format(DEFAULT_PIPELINE))
    parser.add_argument(
        '--run', metavar='NAME', dest='run_name',
        help='run name for pipeline')
    args = parser.parse_args()
    main(args)
