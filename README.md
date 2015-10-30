xenvm Module
============
Requirements
------------
This module requires the XenAPI and provision python libraries.  Both of these libraries are available via pip
```shellcode
pip install XenAPI
pip install provision
```
Example
-------
The following template will create a VM in the default storage repository with the name "example-server" and an interface on the "Private1" network and auto-start the VM once it is created
```yaml
- name: provision ldap server
  hosts: localhost
  tasks:
    #- include: xen_provision.yml 
    - name: provision vm
      xenvm: url=https://<hypervisor address>/ username=<user> password=<pass> name=example-server src="<template uuid>" power_state=on network="Private1"
```
Caveat
------
This module is still very beta and does not support most VM creation parameters.  Currently there is no way to change the amount of resources available to the server.  VM resources default to the values of the sourced template