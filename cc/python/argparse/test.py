#!/usr/bin/env python3

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upgrade 5.6 RDS Cluster to 5.7')

    parser.add_argument('file', type=argparse.FileType('r'), help='file with list of clusters to upgrade')
    parser.add_argument('-c', "--check", action='store_true', help='check wether cluster can be upgraded')
    parser.add_argument('-r', "--reboot", action='store_true', help='reboot cluster instances after upgrade')

    args = parser.parse_args()

    print(args)

    with args['file'] as f:
        clusters = f.read().splitlines()
    
    print(clusters)

    


