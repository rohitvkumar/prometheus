from bottle import route, run, HTTPResponse
import glob
import json
import os
import signal
import subprocess

@route('/health')
def health():
    status = subprocess.check_output(["sv", "status", "prometheus"])
    if status.startswith("run: prometheus:"):
        return "Prometheus is running\n"
    else:
        return HTTPResponse(body='Prometheus is not running\n', status=500)
    
    
@route('/check')
def check():
    return health()

@route('/info')
def info():
    buildinfo = {}
    files = glob.glob("/TivoData/etc/buildinfo/*.json")
    for full_path in files:
        just_file = os.path.basename(full_path)
        no_extension = just_file[:-len(".json")]
        fp = open(full_path)
        try:
            js = json.load(fp)
            buildinfo[no_extension] = js
        except ValueError as e:
            print "Error while parsing file %s: %s" % (full_path, str(e))
            continue
    return buildinfo

@route('/metrics')
def metrics():
    return {}

@route('/releaseRollToken')
def release():
    return health()

@route('/shutdown')
def shutdown():
    os.kill(1, signal.SIGHUP);
    return "Shutting down!\n"

def main():
    run(host='0.0.0.0', port=40101)

if __name__ == '__main__':
    main()

