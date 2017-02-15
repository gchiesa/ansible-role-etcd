#!/usr/bin/env python
import os
import sys
import uuid
import hashlib

cluster_ips = sys.argv[1]
ip = sys.argv[2]

with open(cluster_ips, 'r') as fp:
    data = fp.readlines()

cluster_token = 'etc_cluster_token'

lines = [line.strip() for line in sorted(data) if line.strip()]

initial_cluster_cmd = {}
initial_cluster = []
for index, elem in enumerate(lines):
    initial_cluster.append('etcd{i}=http://{ip}:2380'.format(i=index, ip=elem))

for index, elem in enumerate(lines):
    initial_cluster_cmd[elem] = [
        '-name etcd{i}'.format(i=index),
        '-advertise-client-urls http://{lip}:2379,http://{lip}:4001'.format(lip=elem),
        '-listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001',
        '-initial-advertise-peer-urls http://{lip}:2380'.format(lip=elem),
        '-listen-peer-urls http://0.0.0.0:2380',
        '-initial-cluster-token {token}'.format(token=cluster_token),
        '-initial-cluster "{initial_cluster}"'.format(initial_cluster=','.join(initial_cluster)),
        '-initial-cluster-state new'
        ]
print(' '.join(initial_cluster_cmd[ip]))
