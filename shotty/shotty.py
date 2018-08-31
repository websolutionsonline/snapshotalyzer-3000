# first import the modules
import boto3
import click

#noun (i.e. the description of the thing) then verb (i.e. the doing word)
# e.g. shotty_instances_stop


#global vars
session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

#the @ symbol is a decorator
@click.command()

# functions
def list_instances():
    "List EC2 instances"
    for i in ec2.instances.all():
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name)))

# what is called when the script is run 'standalone'
if __name__ == '__main__':
    list_instances()
