#!/usr/bin/env python

import boto3
import datetime

ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    # Printing Instance INFO ========================================
    print("Instance ID: \t\t" + instance.id)
    print("Instance State: \t" + instance.state['Name'])
    if (instance.state['Name'] == 'running'):
        print("Instance Type: \t\t" + instance.instance_type)
        print("Public IP: \t\t" + instance.public_ip_address)
    print("Current time: \t\t" + datetime.datetime.now().strftime('%H:%M'))

    # Stop/Start instance if it has tag "work_hours"
    for tag in instance.tags:
        if tag['Key'] == 'work_hours':
            print("Instance work hours: \t" + tag['Value'])

            # Parsing working hours =================================
            start_time = tag['Value'].rsplit('-', 1)[0]
            start_time_hour = start_time.rsplit(':', 1)[0]
            start_time_minute = start_time.rsplit(':', 1)[1]

            end_time = tag['Value'].rsplit('-', 1)[1]
            end_time_hour = end_time.rsplit(':', 1)[0]
            end_time_minute = end_time.rsplit(':', 1)[1]

            # Time comparison =======================================
            now = datetime.datetime.now()
            start_at = now.replace(hour=int(start_time_hour), minute=int(start_time_minute))
            stop_at = now.replace(hour=int(end_time_hour), minute=int(end_time_minute))
            if (now > start_at) and (now < stop_at):
                print("Instance " + instance.id + " should be started")
                if (instance.state['Name'] == 'running'):
                    print("Instance " + instance.id + " is already running")
                    continue
                elif (instance.state['Name'] == 'stopped'):
                    print("Starting instance " + instance.id)
                    boto3.client('ec2').start_instances(InstanceIds=[instance.id])

            elif (now < start_at) or (now > stop_at):
                print("Instance " + instance.id + " should be stopped")
                if (instance.state['Name'] == 'stopped'):
                    print("Instance " + instance.id + " is already stopped")
                    continue
                elif (instance.state['Name'] == 'running'):
                    print("Stopping instance " + instance.id)
                    boto3.client('ec2').stop_instances(InstanceIds=[instance.id])
