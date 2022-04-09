def get_regions(session, region='us-east-1'):
    client = session.client('ec2', region_name=region)
    describe_args = {
        'AllRegions': False
    }
    return [region['RegionName'] for region in client.describe_regions(**describe_args)['Regions']]


def get_instance_types(session, region):
    client = session.client('ec2', region_name=region)
    describe_args = {}
    while True:
        describe_result = client.describe_instance_types(**describe_args)
        yield from [instance['InstanceType'] for instance in describe_result['InstanceTypes']]
        if 'NextToken' not in describe_result:
            break
        describe_args['NextToken'] = describe_result['NextToken']


def get_availability_zones(session, region):
    client = session.client('ec2', region_name=region)
    describe_args = {
        'AllAvailabilityZones': False
    }
    return [az['ZoneName'] for az in client.describe_availability_zones(**describe_args)['AvailabilityZones']]


def get_it_az(session, region):
    client = session.client('ec2', region_name=region)
    describe_args = {
        'LocationType': 'availability-zone',
    }

    while True:
        response = client.describe_instance_type_offerings(**describe_args)
        for obj in response['InstanceTypeOfferings']:
            it, region, az = obj.values()
            yield it
        if 'NextToken' not in response:
            break
        describe_args['NextToken'] = response['NextToken']
