# first import the modules
import boto3
import botocore
import click


#noun (i.e. the description of the thing) then verb (i.e. the doing word)
# e.g. shotty_instances_stop


#global vars

def filter_instances(project):
    instances = []
    if project:
            filters = [{'Name':'tag:Project', 'Values':[project]}]
            instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

def has_pending_snapshot(volume):
    snapshots = list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

def can_execute_command(project, force):
    if not project and not force:
        return False
    return True

@click.group()
@click.option('--profile', default='shotty',
    help="Optional profile name. Default will be shotty.")

def cli(profile):
    """Shotty manages snapshots"""
    print("Setting up boto3 session with profile name: {0}...".format(profile))
    global session
    global ec2

    try:
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource('ec2')
    except botocore.exceptions.ProfileNotFound as e:
        print(e)
        exit(1)

# what is called when the script is run 'standalone'
if __name__ == '__main__':
    cli()
