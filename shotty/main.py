# first import the modules
import boto3
import botocore
import click


#noun (i.e. the description of the thing) then verb (i.e. the doing word)
# e.g. shotty_instances_stop

#global vars
session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

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

@click.group()

def cli():
    """Shotty manages snapshots"""





# what is called when the script is run 'standalone'
if __name__ == '__main__':
    cli()
