from setuptools import setup

setup(
    name='snapshotalyzer-3000',
    version='0.1',
    author="Nathan",
    author_email="nathan@test.com",
    description="SnapshotAlyzer 3000 is a tool to manage AWS EC2 snapshots",
    licence="GPLv3+",
    pacakges=['shotty'],
    url="https://github.com/websolutionsonline/snapshotalyzer-3000",
    install_required=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
        '''
)
