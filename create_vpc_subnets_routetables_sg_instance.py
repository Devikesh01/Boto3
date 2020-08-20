import boto3

ec2 = boto3.resource('ec2')

client = boto3.client('ec2')

vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')

vpc.wait_until_available()

print("The id of vpc is "+ vpc.id)

ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print("Internet gateway id is "+ig.id)


route_table = vpc.create_route_table()
route = route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id
)
print("Route table id is "+route_table.id)

subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
print("The subnet id is "+subnet.id)

route_table.associate_with_subnet(SubnetId=subnet.id)

sec_group = ec2.create_security_group(
    GroupName='slice_0', Description='slice_0 sec group', VpcId=vpc.id)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='icmp',
    FromPort=-1,
    ToPort=-1
)
print(sec_group.id)

instances = ec2.create_instances(
    ImageId='ami-0ebc1ac48dfd14136', InstanceType='t2.micro', MaxCount=1, MinCount=1,
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}])
instances[0].wait_until_running()
print(instances[0].id)