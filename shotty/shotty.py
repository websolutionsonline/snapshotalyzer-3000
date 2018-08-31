# first import the modules
import boto3
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


#the @ symbol is a decorator
@click.group()
def instances():
    """COmmands for instances"""

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

# functions
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no-project>')
            )))
    return

@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')
def stop_instances(project):
    "Stop EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return
@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project')
def start_instances(project):
    "Start EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return

# what is called when the script is run 'standalone'
if __name__ == '__main__':
    instances()
