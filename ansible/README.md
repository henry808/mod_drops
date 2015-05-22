# Django Deployment of imager app

This repository contains ansible roles and playbooks which implement a basic
deployment of mod_drops to an AWS ec2 instance.

Created instance with this command (that also builds an inventory):

```bash
$ansible-playbook -i plugins/inventory/ provision_ec2.yml
```

Use this command to deploy mod_drops:

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