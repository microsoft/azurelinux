#!/bin/bash

# The flow of this script is as such:
# 1. Download prometheus tarball to a temp working directory and extract it.
# 2. Parse prometheus's Makefile.common and grep the promu version from it.
# 3. Make a temp subfolder for the promu vendor cache.
# 4. Download promu & extract it, then build it with `make build`. Then save the go vendor cache.
# 5. Copy the vendor folder from promu to our temp subfolder, then delete the built promu & extract the source tarball again.
# 6. Copy the vendor folder back into the extract promu folder and remove the temp subfolder.
# 7. Reinitialize the temp subfolder and switch back to prometheus. We modify web/ui to add an npm cache, and we modify Makefile.common's promu build to use our local tarball instead of the remote prom.
# 8. Then we run make build on prometheus, and save the go vendor cache after that.
# 9. We copy our npm cache and go vendor cache to the temp subfolder & remove our built prometheus. We re-extract the source tarball and copy the npm cache & go vendor cache into prometheus.
# 10. Make some changes to Makefile.common again and compress our custom prometheus and promu folders into their respective tarballs.
# 11. Print SHA256 of prometheus and promu tarballs


START_DIR=$(pwd)
PROM_TMP=$(mktemp -d)

PROMETHEUS_VERSION=2.37.0
PROMETHEUS_URL="https://github.com/prometheus/prometheus/archive/refs/tags/v$PROMETHEUS_VERSION.tar.gz"

cd "$PROM_TMP"
wget -c $PROMETHEUS_URL -O "prometheus-$PROMETHEUS_VERSION.tar.gz"
tar -xzf "prometheus-$PROMETHEUS_VERSION.tar.gz"
#PROMU_VERSION is found in prometheus-$PROMETHEUS_VERSION/Makefile.common
PROMU_VERSION=$(cat "prometheus-$PROMETHEUS_VERSION/Makefile.common" | grep "PROMU_VERSION ?= " | cut -d' ' -f3)
PROMU_URL="https://github.com/prometheus/promu/archive/refs/tags/v$PROMU_VERSION.tar.gz"
mkdir temp_vendor
wget -c $PROMU_URL -O "promu-$PROMU_VERSION.tar.gz"
tar -xzf "promu-$PROMU_VERSION.tar.gz"

cd "promu-$PROMU_VERSION"
make build
go mod vendor
cp -r vendor "$PROM_TMP/temp_vendor"

cd "$PROM_TMP"
rm -rf "promu-$PROMU_VERSION"
tar -xzf "promu-$PROMU_VERSION.tar.gz"
cp -r "temp_vendor/vendor" "promu-$PROMU_VERSION"
rm -rf "temp_vendor"

echo "cache=.npm_cache" > "prometheus-$PROMETHEUS_VERSION/web/ui/.npmrc"
sed -i "s/\$(eval PROMU_TMP := \$(shell mktemp -d))/cd ..\/promu-\$(PROMU_VERSION)/g" prometheus-$PROMETHEUS_VERSION/Makefile.common
sed -i "s/curl -s -L \$(PROMU_URL) | tar -xvzf - -C \$(PROMU_TMP)/make build/g" prometheus-$PROMETHEUS_VERSION/Makefile.common
sed -i "s/cp \$(PROMU_TMP)\/promu-\$(PROMU_VERSION).\$(GO_BUILD_PLATFORM)\/promu/cp promu-\$(PROMU_VERSION)/g" prometheus-$PROMETHEUS_VERSION/Makefile.common
sed -i "s/rm -r \$(PROMU_TMP)//g" prometheus-$PROMETHEUS_VERSION/Makefile.common

mkdir temp_vendor
cd "prometheus-$PROMETHEUS_VERSION"
make build
go mod vendor

cd "$PROM_TMP"
cp -r "prometheus-$PROMETHEUS_VERSION/vendor" temp_vendor
cp "prometheus-$PROMETHEUS_VERSION/web/ui/.npmrc" temp_vendor
cp -r "prometheus-$PROMETHEUS_VERSION/web/ui/.npm_cache" temp_vendor
rm -rf "prometheus-$PROMETHEUS_VERSION"
tar -xzf "prometheus-$PROMETHEUS_VERSION.tar.gz"
cp -r "temp_vendor/vendor" "prometheus-$PROMETHEUS_VERSION"
cp "temp_vendor/.npmrc" "prometheus-$PROMETHEUS_VERSION/web/ui"
cp -r "temp_vendor/.npm_cache" "prometheus-$PROMETHEUS_VERSION/web/ui"
rm -rf "temp_vendor"

sed -i "s/\$(eval PROMU_TMP := \$(shell mktemp -d))/cd ..\/promu-\$(PROMU_VERSION)/g" prometheus-$PROMETHEUS_VERSION/Makefile.common
sed -i "s/curl -s -L \$(PROMU_URL) | tar -xvzf - -C \$(PROMU_TMP)//g" prometheus-$PROMETHEUS_VERSION/Makefile.common
sed -i "s/cp \$(PROMU_TMP)\/promu-\$(PROMU_VERSION).\$(GO_BUILD_PLATFORM)\/promu/cp promu-\$(PROMU_VERSION)/g" prometheus-$PROMETHEUS_VERSION/Makefile.common
sed -i "s/rm -r \$(PROMU_TMP)//g" prometheus-$PROMETHEUS_VERSION/Makefile.common

tar -czf "$START_DIR/prometheus-$PROMETHEUS_VERSION.tar.gz" prometheus-$PROMETHEUS_VERSION
sha256sum "$START_DIR/prometheus-$PROMETHEUS_VERSION.tar.gz"
tar -czf "$START_DIR/promu-$PROMU_VERSION.tar.gz" promu-$PROMU_VERSION
sha256sum "$START_DIR/promu-$PROMU_VERSION.tar.gz"

rm -rf $PROM_TMP
