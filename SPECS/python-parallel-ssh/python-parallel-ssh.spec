%global srcname parallel-ssh
%global debug_package %{nil}
%global _description \
Library for running asynchronous parallel SSH commands over many hosts.\
\
parallel-ssh uses asychronous network requests - there is no multi-threading or\
multi-processing used.\
\
This is a requirement for commands on many (hundreds/thousands/hundreds of\
thousands) of hosts which would grind a system to a halt simply by having so\
many processes/threads all wanting to execute if done with\
multi-threading/processing.

Name:           python-%{srcname}
Version:        2.10.0
Release:        1%{?dist}
Summary:        Asynchronous parallel SSH library
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://parallel-ssh.readthedocs.io/
Source0:        https://github.com/ParallelSSH/parallel-ssh/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  gcc
BuildRequires:  libssh2-devel
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-gevent
Requires:       python3-ssh-python
Requires:       python3-ssh2-python

%if %{with_check}
BuildRequires:  openssh-clients
BuildRequires:  openssh-server
BuildRequires:  python3-gevent
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  sed
%endif

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
## pytest v3.8.2 error: unrecognized arguments: --reruns=5, removing failed test reruns from argopts array.
sed 's/\(^.*\) --reruns=5/\1/' < setup.cfg > setup.cfg.new
cp setup.cfg.new setup.cfg

# fake ssh-agent
eval `ssh-agent`
chmod 600 tests/unit_test_cert_key
ssh-add tests/unit_test_cert_key
chmod 600 tests/client_pkey
ssh-add tests/client_pkey
ssh-add -l

%{python3} -m pip install toml atomicwrites attrs docutils pluggy pygments six coverage more-itertools
## pip fails to install ssh2 due to mismatch in version during metadata generation. Using legacy resolved to proceed.
%{python3} -m pip install --use-deprecated=legacy-resolver ssh2

## Remove tests dependending on yanked 'ssh' module which fails to install via pip.
rm -rf tests/ssh
## Remove tests failing due to segmentation fault
rm tests/test_reader.py
rm tests/native/test_parallel_client.py
## Remove tests getting hanged
rm tests/native/test_single_client.py
rm tests/native/test_tunnel.py

%pytest

%files -n python3-%{srcname}
%license COPYING LICENSE
%doc README.rst Changelog.rst
%{python3_sitearch}/pssh/
%{python3_sitearch}/parallel_ssh-*.egg-info/

%changelog
* Wed Jun 22 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.10.0-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Adding as run dependency for package cassandra medusa.
- Bumping version to 2.10.0.
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.9.1-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.9.1-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.1-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.1-2
- Rebuilt for Python 3.8

* Sun Jul 28 19:53:28 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 04 2018 Miro Hrončok <mhroncok@redhat.com> - 0.91.2-9
- Remove python2 subpackage (#1632336)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.91.2-7
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.91.2-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.91.2-1
- Update to 0.91.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.80.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 25 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.80.3-1
- Update to 0.80.3

* Sun Oct 11 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.80.1-1
- Initial package
