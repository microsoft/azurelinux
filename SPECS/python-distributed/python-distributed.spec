## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global forgeurl https://github.com/dask/distributed
%global srcname distributed

# Can be used to deal with the dependency loop:
# dask -> dask-expr -> distributed -> dask -> distributed
# drops the dask requirement, so this can be built before
# dask-expr and then dask
%bcond bootstrap 0

Name:           python-%{srcname}
Version:        2025.10.0
%global tag     %{version}
Release:        %autorelease
Summary:        Distributed scheduler for Dask
%forgemeta

# Main files: BSD-3-Clause
# distributed/comm/tcp.py
#   - Backport from Tornado 6.2: Apache-2.0
#   - Backport from Trio: Apache-2.0 OR MIT
# distributed/compatibility.py:
#   - Backport from Tornado 6.2: Apache-2.0
#   - Backport from Python 3.12 and 3.10: Python-2.0.1
# distributed/_concurrent_futures_thread.py:
#   - Copied from Python 3.6: Python-2.0.1
# distributed/threadpoolexecutor.py:
#   - Copied from Python 3.5: Python-2.0.1
# distributed/http/static/js/anime.min.js: MIT 
# distributed/http/static/js/reconnecting-websocket.min.js: MIT
License:        BSD-3-Clause AND Apache-2.0 AND (Apache-2.0 OR MIT) AND Python-2.0.1 AND MIT
URL:            https://distributed.dask.org
# PyPI sources do not contain tests.
Source:         %forgesource
# Fedora specific.
Patch:          0001-Increase-test-timeout-for-slower-architectures.patch
Patch:          0002-Install-test-packages.patch
Patch:          0003-Disable-warnings-as-errors-in-tests.patch
Patch:          0004-Loosen-up-some-dependencies.patch
# https://github.com/dask/distributed/pull/7765
Patch:          0005-Skip-doc-test-when-not-running-from-a-git-checkout.patch
# Fix TLS certs to work with OpenSSL 3.
# https://github.com/dask/distributed/issues/8701
# https://github.com/dask/distributed/pull/8707
Patch:          0006-Update-make_tls_certs.py-work-with-openssl-3-8701.patch
# Point the test at the uninstalled version.
Patch:          0007-Avoid-using-sys.prefix-in-CLI-test.patch

BuildArch:      noarch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

BuildRequires:  gcc
BuildRequires:  python3-devel
# Test dependencies
BuildRequires:  python3dist(aiohttp)
# asyncssh must be skipped because we don't have an ssh server we can connect to.
# BuildRequires:  python3dist(asyncssh)
# Tests need a newer version than currently available.
# BuildRequires:  python3dist(bokeh)
BuildRequires:  python3dist(crick)
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(h5py)
BuildRequires:  python3dist(ipykernel)
BuildRequires:  python3dist(ipython)
BuildRequires:  python3dist(ipywidgets)
BuildRequires:  python3dist(joblib)
BuildRequires:  python3dist(jsonschema)
BuildRequires:  python3dist(jupyter-client)
BuildRequires:  python3dist(lz4)
BuildRequires:  python3dist(matplotlib)
BuildRequires:  python3dist(netcdf4)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(pandas)
# paramiko must be skipped because we don't have an ssh server we can connect to.
# BuildRequires:  python3dist(paramiko)
BuildRequires:  python3dist(prometheus-client)
BuildRequires:  python3dist(pyarrow)
BuildRequires:  python3dist(pytest) >= 4
BuildRequires:  python3dist(pytest-repeat)
BuildRequires:  python3dist(pytest-rerunfailures)
BuildRequires:  python3dist(pytest-timeout)
# https://github.com/dask/distributed/issues/5186
# BuildRequires:  python3dist(pytest-xdist)
BuildRequires:  python3dist(pyzmq)
BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(scipy)
BuildRequires:  python3dist(python-snappy)
BuildRequires:  python3dist(zstandard)

%description
Dask.distributed is a lightweight library for distributed computing in Python.
It extends both the concurrent.futures and dask APIs to moderate sized
clusters.


%package -n     python3-%{srcname}
Summary:        %{summary}

BuildArch:      noarch

%description -n python3-%{srcname}
Dask.distributed is a lightweight library for distributed computing in Python.
It extends both the concurrent.futures and dask APIs to moderate sized
clusters.


%prep
%forgeautosetup -p1

%if %{with bootstrap}
# patch out the dask dependency so we can bootstrap it
sed -r -i '/(dask)[<=> ]+[0-9]+/d' pyproject.toml
%endif

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
%if %{without bootstrap}
pushd docs

# protocol/tests/test_protocol.py
# https://github.com/dask/distributed/issues/8700
k="${k-}${k+ and }not test_deeply_nested_structures"

# tests/test_client.py
# https://github.com/dask/distributed/issues/8708
k="${k-}${k+ and }not test_upload_file_zip"

# https://github.com/dask/distributed/pull/8709
k="${k-}${k+ and }not test_git_revision"

# https://github.com/dask/distributed/issues/8437
k="${k-}${k+ and }not test_steal_twice"

# Test started failing with `--reruns`. It seems to succeed without.
# Yet we'd like to rerun the truly flaky tests.
# https://github.com/dask/distributed/issues/9053
k="${k-}${k+ and }not test_computation_object_code_dask_compute"

pytest_args=(
  -m 'not avoid_ci and not flaky and not slow'

  -k "${k-}"

  # Some tests are flaky. Some timing issue with server already
  # shut down it seems.
  --reruns 3 --reruns-delay 1

  --timeout_method=signal

  --pyargs %{srcname}
)

# Remove JUPYTER_PLATFORM_DIRS after we get jupyter-core >=7.
# Disable IPv6 because it sometimes doesn't work:
# https://github.com/dask/distributed/issues/4514
DESTDIR=%{buildroot} DISABLE_IPV6=1 JUPYTER_PLATFORM_DIRS=1 \
    %{pytest} "${pytest_args[@]}"
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%doc AUTHORS.md CONTRIBUTING.md README.rst
%{_bindir}/dask-scheduler
%{_bindir}/dask-ssh
%{_bindir}/dask-worker

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 2025.10.0-2
- Latest state for python-distributed

* Tue Dec 02 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.10.0-1
- Update to latest version

* Sun Sep 21 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.9.1-1
- Update to latest version

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2025.9.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Sun Sep 14 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.9.0-1
- Update to latest version

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 05 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.4.1-1
- Update to latest version

* Thu Apr 24 2025 Sandro <devel@penguinpee.nl> - 2025.4.0-1
- Update to 2025.4.0

* Fri Apr 18 2025 Sandro <devel@penguinpee.nl> - 2025.3.0-1
- Update to 2025.3.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.12.1-1
- Update to latest version

* Wed Nov 27 2024 Richard W.M. Jones <rjones@redhat.com> - 2024.11.2-2
- Rebuild for libarrow 18

* Sun Nov 17 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.11.2-1
- Update to latest version (#2319337)

* Sun Oct 13 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.9.1-1
- Update to latest version (#2309030)

* Mon Sep 23 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.9.0-2
- Correct patches that weren't applying

* Mon Sep 23 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.9.0-1
- Update to latest version

* Sun Aug 18 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.8.0-3
- Increase timeouts on more tests

* Sun Aug 18 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.8.0-2
- Also skip flaky test_steal_twice

* Wed Aug 07 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.8.0-1
- Update to latest version

* Sat Jul 20 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.7.1-1
- Update to latest version

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.6.2-3
- Switch back to noarch build

* Fri Jun 21 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.6.2-1
- Update to latest version

* Tue Jun 18 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.6.0-1
- Update to latest version

* Sun Apr 09 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.3.2.1-1
- Update to latest version

* Mon Nov 28 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.7.1-1
- Update to latest version

* Sun Mar 06 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.2.1-1
- Update to latest version

* Wed Sep 22 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.9.1-1
- Update to latest version

* Sat Aug 21 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.8.1-1
- Update to latest version

* Sat Aug 07 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.7.2-1
- Update to latest version
- Use latest Python macros

* Mon Jul 12 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.7.0-1
- Update to latest version

* Sun Sep 06 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.25.0-1
- Update to latest version

* Sun May 10 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.16.0-1
- Update to latest version

* Sat Feb 29 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.11.0-1
- Update to latest version

* Mon Nov 25 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.8.1-1
- Update to latest version

* Thu Sep 12 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.3.2-1
- Update to latest version

* Wed May 15 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.28.1-1
- Initial package.

## END: Generated by rpmautospec
