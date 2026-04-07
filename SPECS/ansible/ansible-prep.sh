#!/usr/bin/bash -x

# SPDX-License-Identifier: MIT
# Copyright (C) Fedora Project Authors
# License Text: https://spdx.org/licenses/MIT.txt

set -euo pipefail

# Fix wrong-script-end-of-line-encoding in azure.azcollection
find ansible_collections/azure/azcollection -type f -print -exec dos2unix -k '{}' \;

# Remove unnecessary files and directories included in the Ansible collection release tarballs
# Tracked upstream in part by: https://github.com/ansible-community/community-topics/issues/29
echo "[START] Delete unnecessary files and directories"

# Collection tarballs contain a lot of hidden files and directories
hidden_pattern=".*\.(DS_Store|all-contributorsrc|ansible-lint|azure-pipelines|circleci|codeclimate.yml|flake8|galaxy_install_info|gitattributes|github|gitignore|gitkeep|gitlab-ci.yml|idea|keep|mypy_cache|nojekyll|orig|plugin-cache.yaml|pre-commit-config.yaml|project|pydevproject|pytest_cache|pytest_cache|readthedocs.yml|settings|swp|travis.yml|vscode|yamllint|yamllint.yaml|zuul.d|zuul.yaml|rstcheck.cfg|placeholder)$"
find ansible_collections -depth -regextype posix-egrep -regex "${hidden_pattern}" -print -exec rm -r {} \;

# Not needed for runtime
rm -rv ansible_collections/cisco/meraki/scripts/
rm -rv ansible_collections/community/digitalocean/scripts/
rm -rv ansible_collections/community/grafana/hacking/
rm -rv ansible_collections/community/okd/ci/
rm -rv ansible_collections/community/vmware/tools/
rm -rv ansible_collections/cyberark/conjur/roles/conjur_host_identity/tests/
rm -rv ansible_collections/google/cloud/scripts/
rm -rv ansible_collections/google/cloud/test-fixtures/
rm -rv ansible_collections/grafana/grafana/tools/
rm -rv ansible_collections/hetzner/hcloud/scripts/
rm -rv ansible_collections/netbox/netbox/hacking/
rm -rv ansible_collections/sensu/sensu_go/docker/
rm -rv ansible_collections/sensu/sensu_go/tools/

rm -v ansible_collections/community/mysql/run_all_tests.py
rm -v ansible_collections/dellemc/enterprise_sonic/rebuild.sh
rm -v ansible_collections/ovirt/ovirt/build.sh

# rpmlint W: pem-certificate
find ansible_collections/cyberark/conjur -type f -name "*.pem" -print -delete

# rpmlint E: zero-length
find -type f -name "*requirements.txt" -size 0 -print -delete
rm -v ansible_collections/community/zabbix/roles/zabbix_agent/files/win_sample/doSomething.ps1
rm -v ansible_collections/community/docker/meta/ee-bindep.txt
rm -vr ansible_collections/ibm/spectrum_virtualize/roles/place_holder

echo "[END] Delete unnecessary files and directories"

###
# Fix various shebang related issues to appease brp-managle-shebangs
###
find ansible_collections/community/mongodb/roles/*/{files,templates} -type f '!' -executable -name '*.sh*' \
    -print -exec chmod a+x '{}' \;

# ansible_collections/lowlydba/sqlserver thought it was a good idea to make
# *every* single file, in its repository executable, including .md, .yml, and
# .rst. :facepalm:
#
# TODO: File issue upstream
find ansible_collections/lowlydba/sqlserver/ -executable -type f -print -exec chmod a-x '{}' \;


# Remove shebangs instead of hardocding to %%__python3 to avoid unexpected issues
# from https://github.com/ansible/ansible/commit/9142be2f6cabbe6597c9254c5bb9186d17036d55.
# Upstream, ansible-core has also removed shebangs from its modules.
#
# XXX: Print out the files before they're replaced
find ansible_collections -type f ! -executable -name '*.py' | tee non_exec
echo ansible_collections/community/sap_libs/plugins/module_utils/swpm2_parameters_inifile_generate.py >> non_exec
# xargs is noticably faster than find -exec, because it spawns one sed process
# instead of ~13 thousand!
xargs -a non_exec -d'\n' sed -i -e '1{\@^#!.*@d}'
