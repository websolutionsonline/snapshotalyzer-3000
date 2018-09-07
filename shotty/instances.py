# first import the modules
from shotty.main import *


#the @ symbol is a decorator
@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

@click.option('--force', 'force_action', default=False, is_flag=True,
    help="If '--project' isn't set, the 'snapshot' command will not execute unless the '--force option is set'")

def create_snapshots(project, force):
    "Create snapshots for EC2 instances"
    if not can_execute_command(project, force):
        print ('Cannot force instances, no project was specified or force option was not specified')
        return
    instances = filter_instances(project)

    for i in instances:

        print("Stopping {0}...".format(i.id))

        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            if has_pending_snapshot(v):
                print(" Skipping {0}, snapshot already in progress.".format(v.id))
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by SnapshotAlyzer 3000")

        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()
    print("Job Done!")
    return

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

@click.option('--force', default=False, is_flag=True,
    help="If '--project' isn't set, the 'stop' command will not execute unless the '--force option is set'")

def stop_instances(project, force):
    "Stop EC2 instances"
    if not can_execute_command(project, force):
        print ('Cannot stop instances, no project was specified or force option was not specified')
        return

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0}. ".format(i.id) + str(e))
            continue

    return
@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project')

@click.option('--force', default=False, is_flag=True,
    help="If '--project' isn't set, the 'start' command will not execute unless the '--force option is set'")

def start_instances(project, force):
    "Start EC2 instances"
    if not can_execute_command(project, force):
        print ('Cannot start instances, no project was specified or force option was not specified')
        return

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))

        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0}. ".format(i.id) + str(e))
            continue
    return

@instances.command('reboot')
@click.option('--project', default=None,
    help='Only instances for project')

@click.option('--force', default=False, is_flag=True,
    help="If '--project' isn't set, the 'reboot' command will not execute unless the '--force option is set'")

def reboot_instances(project, force):
    "Reboot EC2 instances"
    if not can_execute_command(project, force):
        print ('Cannot reboot instances, no project was specified or force option was not specified')
        return

    instances = filter_instances(project)

    for i in instances:
        print("Rebooting {0}...".format(i.id))

        try:
            i.reboot()
        except botocore.exceptions.ClientError as e:
            print(" Could not reboot {0}. ".format(i.id) + str(e))

    return



#except botocore.exceptions.ClientError as e:
#        code = e.response['Error']['Code']
#        message = e.response['Error']['Message']
#        if code == 'IncorrectState':
#            print('retry')
