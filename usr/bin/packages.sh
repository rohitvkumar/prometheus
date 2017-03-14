#!/bin/sh

set -eou

# Install essentials
apk --update add curl python py-pip runit tar

# Install temporary packages
apk add --virtual build-dependencies build-base git openssl

# Install required python packages
pip install --upgrade pip
pip install requests bottle

mkdir /TivoData

curl -sL "https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz" | tar -xz -C /TivoData
ln -s /TivoData/prometheus-$PROMETHEUS_VERSION.linux-amd64 /TivoData/prometheus-install

#cleanup
apk del build-dependencies
rm -rf /var/cache/apk/*