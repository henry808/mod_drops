# Django Deployment of imager app

This repository contains ansible roles and playbooks which implement a basic
deployment of Django imager app to an AWS ec2 instance.

Use this command to deploy imager app:

```bash
$ansible-playbook -i plugins/inventory deploy_django.yml
```

To create an inventory of all instances:

```bash
$python ./plugins/inventory/ec2.py
```

To set ssh key:

```bash
$ ssh-agent bash
$ ssh-add ~/.ssh/pk-aws.pem
```