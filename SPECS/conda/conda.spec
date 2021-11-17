%{!?_with_bootstrap: %global bootstrap 0}

Summary:        Cross-platform, Python-agnostic binary package manager
Name:           conda
Version:        4.10.1
Release:        2%{?dist}
License:        BSD and ASL 2.0 and LGPLv2+ and MIT
# The conda code is BSD
# progressbar is LGPLv2+
# six is MIT/X11
# adapters/ftp.py is ASL 2.0
URL:            http://conda.pydata.org/docs/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/conda/conda/archive/%{version}/%{name}-%{version}.tar.gz
# bash completion script moved to a separate project
Source1:        https://raw.githubusercontent.com/tartansandal/conda-bash-completion/1.5/conda
Patch0:         conda_sys_prefix.patch
Patch1:         conda_gateways_disk_create.patch
Patch2:         setup.patch
# Use system cpuinfo
Patch3:         conda-cpuinfo.patch

Patch10001:     0001-Fix-toolz-imports.patch
Patch10003:     0003-Drop-fs-path-encoding-manipulation-under-python2.patch
Patch10004:     0004-Do-not-try-to-run-usr-bin-python.patch
Patch10005:     0005-Fix-failing-tests-in-test_api.py.patch
Patch10006:     0006-shell-assume-shell-plugins-are-in-etc.patch

BuildArch:      noarch

# Temp: Do not build with x86_64 due to docker build issue
ExclusiveArch:  aarch64

BuildRequires:  bash-completion-devel
%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '/etc/bash_completion.d')
BuildRequires:  sed

Requires:       python%{python3_pkgversion}-conda = %{version}-%{release}

%?python_enable_dependency_generator


%global _description %{expand:
Conda is a cross-platform, Python-agnostic binary package manager. It
is the package manager used by Anaconda installations, but it may be
used for other systems as well. Conda makes environments first-class
citizens, making it easy to create independent environments even for
C libraries. Conda is written entirely in Python.

The Fedora conda base environment is special.  Unlike a standard
anaconda install base environment it is essentially read-only.  You
can only use conda to create and manage new environments.}


%description %_description

%global _py3_reqs \
        python%{python3_pkgversion}-cpuinfo \
        python%{python3_pkgversion}-conda-package-handling >= 1.3.0 \
        python%{python3_pkgversion}-distro >= 1.0.4 \
        python%{python3_pkgversion}-frozendict >= 1.2 \
        python%{python3_pkgversion}-pycosat >= 0.6.3 \
        python%{python3_pkgversion}-pyOpenSSL >= 16.2.0 \
        python%{python3_pkgversion}-requests >= 2.18.4 \
        python%{python3_pkgversion}-ruamel-yaml >= 0.11.14 \
        python%{python3_pkgversion}-tqdm >= 4.22.0 \
        python%{python3_pkgversion}-urllib3 >= 1.19.1
%global py3_reqs %(c="%_py3_reqs"; echo "$c" | xargs)


%package -n python%{python3_pkgversion}-conda
Summary:        %{summary}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  %py3_reqs
# For tests
BuildRequires:  python3
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-responses
%endif

Requires:       %py3_reqs
Requires:       python%{python3_pkgversion}-cytoolz >= 0.8.2
Provides:       bundled(python%{python3_pkgversion}-appdirs) = 1.2.0
Provides:       bundled(python%{python3_pkgversion}-auxlib)
Provides:       bundled(python%{python3_pkgversion}-boltons) = 18.0.0
Provides:       bundled(python%{python3_pkgversion}-six) = 1.10.0
Provides:       bundled(python%{python3_pkgversion}-toolz) = 0.8.2

%{?python_provide:%python_provide python%{python3_pkgversion}-conda}

%description -n python%{python3_pkgversion}-conda %_description

%prep
%autosetup -p1

sed -r -i 's/^(__version__ = ).*/\1"%{version}"/' conda/__init__.py

# delete interpreter line, the user can always call the file
# explicitly as python3 /usr/lib/python3.6/site-packages/conda/_vendor/appdirs.py
# or so.
sed -r -i '1 {/#![/]usr[/]bin[/]env/d}' conda/_vendor/appdirs.py

# Use Fedora's cpuinfo since it supports more arches
rm conda/_vendor/cpuinfo.py

# Use system versions
# TODO - urllib3 - results in test failures: https://github.com/conda/conda/issues/9512
#rm -r conda/_vendor/{distro.py,frozendict.py,tqdm,urllib3}
#find conda -name \*.py | xargs sed -i -e 's/^\( *\)from .*_vendor\.\(\(distro\|frozendict\|tqdm\|urllib3\).*\) import/\1from \2 import/'
rm -r conda/_vendor/{distro.py,frozendict.py,tqdm}
find conda -name \*.py | xargs sed -i -e 's/^\( *\)from .*_vendor\.\(\(distro\|frozendict\|tqdm\).*\) import/\1from \2 import/'

%ifnarch x86_64
# Tests on non-x86_64
cp -a tests/data/conda_format_repo/{linux-64,%{python3_platform}}
sed -i -e s/linux-64/%{python3_platform}/ tests/data/conda_format_repo/%{python3_platform}/*json
%endif


%build
# build conda executable
%define py_setup utils/setup-testing.py
%py3_build

%install
# install conda executable
%define py_setup utils/setup-testing.py
%py3_install

mkdir -p %{buildroot}%{_datadir}/conda/condarc.d
cat >%{buildroot}%{_datadir}/conda/condarc.d/defaults.yaml <<EOF
pkgs_dirs:
 - /var/cache/conda/pkgs
 - ~/.conda/pkgs
EOF

mkdir -p %{buildroot}%{_localstatedir}/cache/conda/pkgs/cache

install -m 0644 -Dt %{buildroot}/etc/profile.d/ conda/shell/etc/profile.d/conda.{sh,csh}
sed -r -i '1i CONDA_EXE=%{_bindir}/conda' %{buildroot}/etc/profile.d/conda.sh
sed -r -i -e '1i set _CONDA_EXE=%{_bindir}/conda\nset _CONDA_ROOT=' \
          -e 's/CONDA_PFX=.*/CONDA_PFX=/' %{buildroot}/etc/profile.d/conda.csh
install -m 0644 -Dt %{buildroot}/etc/fish/conf.d/ conda/shell/etc/fish/conf.d/conda.fish
sed -r -i -e '1i set -gx CONDA_EXE "/usr/bin/conda"\nset _CONDA_ROOT "/usr"\nset _CONDA_EXE "/usr/bin/conda"\nset -gx CONDA_PYTHON_EXE "/usr/bin/python3"' \
          %{buildroot}/etc/fish/conf.d/conda.fish

# Install bash completion script
install -m 0644 -Dt %{buildroot}%{bash_completionsdir}/ %SOURCE1


%check
export PATH=%{buildroot}%{_bindir}:$PATH
PYTHONPATH=%{buildroot}%{python3_sitelib} conda info

# Integration tests generally require network, so skip them.

# TestJson.test_list does not recognize /usr as a conda environment
# These fail on koji with PackageNotFound errors likely due to network issues
# test_cli.py::TestRun.test_run_returns_int
# test_cli.py::TestRun.test_run_returns_nonzero_errorlevel
# test_cli.py::TestRun.test_run_returns_zero_errorlevel

# test_ProgressiveFetchExtract_prefers_conda_v2_format, test_subdir_data_prefers_conda_to_tar_bz2,
# test_use_only_tar_bz2 fail, but not with mock --enablerepo=local. Let's disable
# them for now.
# tests/core/test_initialize.py tries to unlink /usr/bin/python3 and fails when python is a release candidate
# tests/core/test_solve.py::test_cuda_fail_1 fails on non-x86_64

# tests/base/test_context.py::ContextCustomRcTests::test_target_prefix 

# The following fail trying to raise a pytest exception.
# The tests change a file to read-only and expect an exception when trying to open the file for appending
# The exception does occur for normal users but not for root 
# Since root is required for pytest and build tools, skip:
# tests/core/test_package_cache_data.py::test_instantiating_package_cache_when_both_tar_bz2_and_conda_exist_read_only \
# tests/gateways/disk/test_delete.py::test_remove_file \
# tests/gateways/disk/test_delete.py::test_remove_file_to_trash \
# tests/gateways/disk/test_permissions.py::test_make_writable \
# tests/gateways/disk/test_permissions.py::test_recursive_make_writable \
# tests/gateways/disk/test_permissions.py::test_make_executable 


mkdir /tmp

pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    ruamel.yaml>=0.11.14 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest>=5.4.0 \
    pytest-cov>=2.7.1 
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -vv -m "not integration" \
    --deselect=tests/test_cli.py::TestJson::test_list \
    --deselect=tests/test_cli.py::TestRun::test_run_returns_int \
    --deselect=tests/test_cli.py::TestRun::test_run_returns_nonzero_errorlevel \
    --deselect=tests/test_cli.py::TestRun::test_run_returns_zero_errorlevel \
    --deselect=tests/core/test_package_cache_data.py::test_ProgressiveFetchExtract_prefers_conda_v2_format \
    --deselect=tests/core/test_subdir_data.py::test_subdir_data_prefers_conda_to_tar_bz2 \
    --deselect=tests/core/test_subdir_data.py::test_use_only_tar_bz2 \
    --deselect=tests/core/test_initialize.py \
    --deselect=tests/core/test_solve.py::test_cuda_fail_1 \
    --deselect=tests/base/test_context.py::ContextCustomRcTests::test_target_prefix \
    --deselect=tests/core/test_package_cache_data.py::test_instantiating_package_cache_when_both_tar_bz2_and_conda_exist_read_only \
    --deselect=tests/gateways/disk/test_delete.py::test_remove_file \
    --deselect=tests/gateways/disk/test_delete.py::test_remove_file_to_trash \
    --deselect=tests/gateways/disk/test_permissions.py::test_make_writable \
    --deselect=tests/gateways/disk/test_permissions.py::test_recursive_make_writable \
    --deselect=tests/gateways/disk/test_permissions.py::test_make_executable 


%files
%{_bindir}/conda
%{_bindir}/conda-env
%{bash_completionsdir}/conda
# TODO - better ownership/requires for fish
%dir /etc/fish
%dir /etc/fish/conf.d
/etc/fish/conf.d/conda.fish
/etc/profile.d/conda.sh
/etc/profile.d/conda.csh

%files -n python%{python3_pkgversion}-conda
%license LICENSE.txt
%doc CHANGELOG.md README.rst
%{python3_sitelib}/conda/
%{python3_sitelib}/conda_env/
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/test_data/
%{_localstatedir}/cache/conda/
%{_datadir}/conda/


%changelog
* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.10.1-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Thu Apr 15 2021 Orion Poplawski <orion@nwra.com> - 4.10.1-1
- Update to 4.10.1

* Fri Apr 02 2021 Orion Poplawski <orion@nwra.com> - 4.10.0-1
- Update to 4.10.0

* Tue Jan 26 2021 Orion Poplawski <orion@nwra.com> - 4.9.2-3
- Add patch to support python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Orion Poplawski <orion@nwra.com> - 4.9.2-1
- Update to 4.9.2

* Tue Oct 27 2020 Orion Poplawski <orion@nwra.com> - 4.9.1-1
- Update to 4.9.1

* Sun Oct 18 2020 Orion Poplawski <orion@nwra.com> - 4.9.0-1
- Update to 4.9.0

* Mon Sep 21 2020 Orion Poplawski <orion@nwra.com> - 4.8.5-2
- Add note to description about base environment

* Mon Sep 14 2020 Orion Poplawski <orion@nwra.com> - 4.8.5-1
- Update to 4.8.5
- Install conda.fish (bz#1878306)

* Sat Aug 08 2020 Orion Poplawski <orion@nwra.com> - 4.8.4-1
- Update to 4.8.4

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.8.3-2
- Rebuilt for Python 3.9

* Sun Mar 15 2020 Orion Poplawski <orion@nwra.com> - 4.8.3-1
- Update to 4.8.3

* Tue Feb  4 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.8.2-2
- Fix import for python3.9 compatiblity (#1797691)

* Tue Jan 28 2020 Orion Poplawski <orion@nwra.com> - 4.8.2-1
- Update to 4.8.2 (#1785658)
- Obtain bash completion file from github - tartansandal/conda-bash-completion

* Mon Jan 20 2020 Orion Poplawski <orion@nwra.com> - 4.8.0-2
- Install bash completion file (bz#1791068)

* Sat Dec 14 2019 Orion Poplawski <orion@nwra.com> - 4.8.0-1
- Update to 4.8.0
- Make "conda shell.bash hook" work (bz#1737165)
- Unbundle more libraries

* Sat Sep 14 2019 Orion Poplawski <orion@nwra.com> - 4.7.12-1
- Update to 4.7.12

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.7.11-2
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Orion Poplawski <orion@nwra.com> - 4.7.11-1
- Update to 4.7.11
- Use system py-cpuinfo

* Fri Aug 16 2019 Orion Poplawski <orion@nwra.com> - 4.7.10-2
- Cleanup requires some (drop crypto, yaml; add pyOpenSSL; 
  add versions for requests and ruamel-yaml

* Sat Aug  3 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.7.10-1
- Fix 'conda shell.* hook' invocations (#1737165)

* Wed Jul 31 2019 Orion Poplawski <orion@nwra.com> - 4.7.10-1
- Update to 4.7.10

* Mon Jul 29 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.7.6-1
- Update to latest version (#1678578)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Orion Poplawski <orion@nwra.com> - 4.7.2-1
- Update to 4.7.2

* Sun Jun  9 2019 Orion Poplawski <orion@nwra.com> - 4.7.1-1
- Update to 4.7.1

* Tue Apr 16 2019 Orion Poplawski <orion@nwra.com> - 4.6.13-1
- Update to 4.6.13

* Thu Apr  4 2019 Orion Poplawski <orion@nwra.com> - 4.6.11-1
- Update to 4.6.11

* Tue Apr  2 2019 Orion Poplawski <orion@nwra.com> - 4.6.9-2
- Fix conda profile scripts
- Do not build for python2 on EPEL
- Ignore test failures on EPEL7

* Sat Mar 30 2019 Orion Poplawski <orion@nwra.com> - 4.6.9-1
- Update to 4.6.9

* Wed Feb 13 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.6.5-1
- Update to latest upstream version (#1668145)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 31 2018 Orion Poplawski <orion@nwra.com> - 4.5.12-1
- Update to 4.5.12

* Mon Dec 31 2018 Orion Poplawski <orion@nwra.com> - 4.5.11-2
- EPEL7 compatability

* Fri Sep 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.5.11-1
- Update to latest stable version (#1570217)
- Disable python2 subpackage on F30+

* Fri Jul 13 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.4.11-4
- Pull in python[23]-cytoolz to replace bundled toolz

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.4.11-3
- Rebuilt for Python 3.7

* Wed Apr 18 2018 Orion Poplawski <orion@nwra.com> - 4.4.11-2
- Set _CONDA_ROOT in /etc/profile.d/conda.csh
- Fix python2 requires
- Require pycosat >= 0.6.3

* Sat Apr 14 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.4.11-1
- Update to latest upstream version in the 4.4.x branch (#1544046)

* Wed Feb  7 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.4.9-1
- Update to v4.4.9 (#1542874)
- conda-activate binary rpm is retired. The new way to activate the environment
  is to say 'conda activate'. See
  https://github.com/conda/conda/releases/tag/4.4.0 for more information.

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.3.24-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.24-3
- Install just one version of the executables (python 2 or 3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.24-2
- Add all licenses to the License tag
- Add Provides: bundled(...) for all the "vendored" dependencies
- Update descriptions and simplify the spec file a bit
- Move condarc.d directory under /usr/share/conda

* Thu Aug  3 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.24-1
- Update to latest version
- Switch /usr/bin/conda to python3

* Thu Jul 21 2016 Orion Poplawski <orion@cora.nwra.com> - 4.1.6-1
- Update to 4.1.6

* Thu Dec 31 2015 Orion Poplawski <orion@cora.nwra.com> - 3.19.0-1
- Update to 3.19.0

* Thu Dec 31 2015 Orion Poplawski <orion@cora.nwra.com> - 3.18.8-2
- Add python 3 version

* Mon Dec 7 2015 Orion Poplawski <orion@cora.nwra.com> - 3.18.8-1
- Update to 3.18.8

* Thu Sep 24 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-6
- Do not create broken symlinks if activate/deactivate are not installed
- Do not create /usr/conda-meta to prevent accidental installs into system

* Thu Sep 24 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-5
- Non-bootstrap build

* Wed Sep 23 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-4
- Add patch to support rootless mode
- Require python-crypto
- Create /usr/conda-meta, /usr/.condarc, /var/cache/conda

* Tue Sep 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-3
- Require python-requests, python-yaml

* Tue Sep 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-2
- Add patch to allow overriding pkgs_dirs in .condarc

* Mon Sep 21 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-1
- Initial package
