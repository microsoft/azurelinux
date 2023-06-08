#!/bin/bash
mv /etc/yum.repos.d/local_repo.not_a_repo /etc/yum.repos.d/local_repo.repo
pushd /repo
createrepo .

echo ""
echo ">>>>> The local repo is enabled. You can install the following packages from it:"
echo ""

#tdnf repoquery --repoid=local_build_repo 2>/dev/null