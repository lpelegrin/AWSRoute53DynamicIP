import boto3
import requests
import time
import os


class AWSRoute53DynamicIP:
    r53client = boto3.client('route53')
    route53_arn_id = ""
    route53_records = ""
    loop_time = None
    default_ttl = None
    debug = False
    pub_ip = ""

    def __init__(self):
        # Get Input from environment variables
        self.route53_arn_id  = os.getenv("AWS_ROUTE53_HZ_ARN", "")
        self.route53_records = os.getenv("AWS_ROUTE53_RECORDS", "")
        self.default_ttl = int(os.getenv("AWS_ROUTE53_TTL", 120))
        self.loop_time = int(os.getenv("LOOP_TIME", 120))
        self.debug = bool(os.getenv("DEBUG", False))

        # Parse inputs 
        if self.route53_arn_id == "":
            raise ValueError('AWS_ROUTE53_HZ_ARN environment variable is empty ')
        if self.route53_records == "":
            raise ValueError('AWS_ROUTE53_RECORDS environment variable is empty')

        # Parse multiple records from input
        self.route53_records = self.route53_records.replace(' ','').split(',')

        if self.debug:
            print(self.route53_records)


    def __hasPublicIPChanged(self):
        has_changed = False
        msg = requests.get('http://ip.42.pl/raw').text
        if msg != self.pub_ip:
            has_changed = True
            self.pub_ip = msg

        if self.debug:
            print("__getCurrentPublicIP: current public ip is(%s)" % (msg))
        
        return has_changed


    def __upsertRoute53RecordValue(self):
        self.r53client.change_resource_record_sets(
            HostedZoneId=self.route53_arn_id,
            ChangeBatch={
                'Changes':[
                    {'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': 'A',
                        'ResourceRecords': [{'Value': self.pub_ip}],
                        'TTL': self.default_ttl }} 
                    for name in self.route53_records ]})

    def run(self):
        while(1):
            if self.__hasPublicIPChanged():
                self.__upsertRoute53RecordValue()
            time.sleep(self.loop_time)