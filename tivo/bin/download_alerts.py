#!/usr/bin/env python

import argparse
import json
import os
import requests
import sys


def get_alerts(dynhost, dynport, datacenter):
    payload = {
               "type": "dynconfigAlertSearch",
               "datacenter": datacenter
               }
    resp = requests.post("http://{host}:{port}/dynconfigAlertSearch".format(host=dynhost, port=dynport),
                         json=json.loads(payload))
    resp.raise_for_status()
    return resp.json["dynconfigAlert"]

def main():
    parser = argparse.ArgumentParser(description="Export events to prometheus.")
    
    parser.add_argument("-v", "--verbose", help="Verbose output.", action="store_true")
    parser.add_argument("-s", "--simulated", help="Debugging only - no changes will be made to cluster.", action="store_true")
    parser.add_argument("-h", "--dynhost", help="Dynconfig host", metavar="hostname", default="localhost")
    parser.add_argument("-p", "--dynport", help="Dynconfig port", metavar="port", type=int, default=50000)
    parser.add_argument("-f", "--folder-path", help="Drop this metric", metavar="PATH", default="/home/tivo/etc/alerts")
    
    
    args = parser.parse_args()
    
    global VERBOSE
    global SIMULATED
    
    VERBOSE = args.verbose
    SIMULATED = args.simulated
    
    if VERBOSE:
        logger.info(args)
        
        
if __name__ == "__main__":
    main()