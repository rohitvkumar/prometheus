#!/usr/bin/env python
import glob
import json
import os
import requests
import sys
import types

def constructDynconfigVariableDefinition(base):
    base['service'] = service
    base['type'] = 'dynconfigVariableDefinition'
    if verbose:
        print 'Found {0}'.format(json.dumps(base))
    return base

def collectVariableDefinitionFiles(path, service):
    path = path.rstrip(os.pathsep)
    files = glob.glob('{0}{1}*.json'.format(path, os.pathsep))
    definitions = []
    for file in files:
        with open(file, 'r') as fp:
            defn = json.load(fp)
            if isinstance(defn, list):
                for obj in defn:
                    definitions.append(constructDynconfigVariableDefinition(obj))
            else:
                definitions.append(constructDynconfigVariableDefinition(defn))
    
    return definitions

def register_definitions(dynconfig, definition):
    '''
    Register a single variable definition with dynconfig_server
    '''
    url = 'http://{server}/dynconfigVariableDefinitionStore'.format(server=dynconfig)
    request = {
        'type' : 'dynconfigVariableDefinitionStore',
        'variableDefinition' : definition
        }
    if verbose:
        print url
        print json.dumps(request, indent=2)
    if not simulated:
        r = requests.post(url, json=payload)
        r.raise_for_status()
            

def main():
    '''
    Main entrypoint that does argument parsing
    '''
    parser = argparse.ArgumentParser(
        description='Register variable definitions with dynconfig')
    parser.add_argument('--dynconfig-server',
                        metavar='HOST:PORT',
                        default='localhost:50000',
                        help='Dynconfig server address')
    parser.add_argument('-f', '--definitions-dir',
                        metavar='DIR_PATH',
                        default='/home/tivo/etc/variables',
                        help='Directory containing variable definition json files.')
    parser.add_argument('-s', '--service',
                        metavar='NAME',
                        help='Name of the service for which this variable is being defined.',
                        required=True)
    parser.add_argument('--simulated',
                        default=False,
                        action='store_true',
                        help='Debugging only - no changes made to cluster')
    parser.add_argument('-v', '--verbose',
                        default=False,
                        action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    global verbose
    global simulated

    verbose = args.verbose
    simulated = args.simulated
    
    definitions = collectVariableDefinitionFiles(args.definitions_dir, service)
    
    for definition in definitions:
        register_definitions(args.dynconfig_server, definition)
    
if __name__ == "__main__":
    main()
