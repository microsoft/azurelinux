# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         srcname  asyncssh
%global         desc     Python 3 library for asynchronous client and\
server-side SSH communication. It uses the Python asyncio module and\
implements many SSH protocol features such as the various channels,\
SFTP, SCP, forwarding, session multiplexing over a connection and more.

Name:           python-%{srcname}
Version:        2.21.0
Release:        5%{?dist}
Summary:        Asynchronous SSH for Python

# Automatically converted from old format: EPL-2.0 or GPLv2+ - review is highly recommended.
License:        EPL-2.0 OR GPL-2.0-or-later
URL:            https://github.com/ronf/asyncssh
Source0:        %pypi_source


BuildArch:      noarch

# required by unittests
BuildRequires:  nmap-ncat
BuildRequires:  openssh-clients
BuildRequires:  openssl
BuildRequires:  python3-gssapi


# for ed25519 etc.
Recommends:     python3-libnacl

# for OpenSSH private key encryption
Suggests:       python3-bcrypt
# for GSSAPI key exchange/authentication
Suggests:       python3-gssapi
# for X.509 certificate authentication
Suggests:       python3-pyOpenSSL
# for U2F etc. support
Suggests:       python3-fido2

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%prep
%autosetup -p1 -n %{srcname}-%{version}
# XXX remove again when python3-cryptography dependency spec
#     of python3-fido2 is fixed in rawhide
#     cf. https://bugzilla.redhat.com/show_bug.cgi?id=2368966
sed -i '/fido2/d' pyproject.toml tox.ini


%generate_buildrequires
%pyproject_buildrequires -t


%build
sed -i '1,1s@^#!.*$@#!%{__python3}@' examples/*.py
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
%{__python3} -m unittest discover -s tests -t . -v

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE COPYRIGHT
%doc README.rst examples


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.21.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.21.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.21.0-2
- Rebuilt for Python 3.14

* Sat May 31 2025 Georg Sauthoff <mail@gms.tf> - 2.21.0-1
- Update to latest upstream version (fixes fedora#2346174, fixes fedora#2325445)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Georg Sauthoff <mail@gms.tf> - 2.19.0-1
- Update to latest upstream version (fixes fedora#2321945)

* Mon Sep 09 2024 Georg Sauthoff <mail@gms.tf> - 2.17.0-1
- Update to latest upstream version (fixes fedora#2295694)

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 2.14.2-7
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 27 2024 Georg Sauthoff <mail@gms.tf> - 2.14.2-5
- Fix Python 3.13 compatibility (fixes fedora#2251916)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.14.2-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 21 2023 Georg Sauthoff <mail@gms.tf> - 2.14.2-1
- Update to latest upstream version (fixes fedora#2255038)
- Fix CVE-2023-48795 ssh: Prefix truncation attack on Binary Packet Protocol (BPP) (fixes fedora#2254210)

* Sat Nov 11 2023 Georg Sauthoff <mail@gms.tf> - 2.14.1-1
- Update to latest upstream version (fixes fedora#2241582)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Georg Sauthoff <mail@gms.tf> - 2.13.2-3
- Re-enable tests on RHEL (fixes fedora#2196046)

* Tue Jul 11 2023 Georg Sauthoff <mail@gms.tf> - 2.13.2-2
- Fix test_stdout_stream test case failure (fixes fedora#2220123)

* Tue Jul 11 2023 Georg Sauthoff <mail@gms.tf> - 2.13.2-1
- Update to latest upstream version (fixes fedora#2216606)

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.13.1-2
- Rebuilt for Python 3.12

* Sun Mar 26 2023 Georg Sauthoff <mail@gms.tf> - 2.13.1-1
- Update to latest upstream version (fixes fedora#2156599)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 29 2022 Georg Sauthoff <mail@gms.tf> - 2.12.0-1
- Update to latest upstream version (fixes fedora#2117472)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Georg Sauthoff <mail@gms.tf> - 2.11.0-3
- Fix test cases

* Sat Jul 09 2022 Georg Sauthoff <mail@gms.tf> - 2.11.0-2
- Fix test cases

* Sat Jul 09 2022 Georg Sauthoff <mail@gms.tf> - 2.11.0-1
- Update to latest upstream version (fixes fedora#2068852)

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.9.0-5
- Rebuilt for Python 3.11

* Sat Feb 05 2022 Georg Sauthoff <mail@gms.tf> - 2.9.0-4
- Fix test cases

* Sat Feb 05 2022 Georg Sauthoff <mail@gms.tf> - 2.9.0-3
- Fix dependencies

* Sat Feb 05 2022 Georg Sauthoff <mail@gms.tf> - 2.9.0-1
- Update to latest upstream version (fixes fedora#2044074)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 11 2021 Georg Sauthoff <mail@gms.tf> - 2.8.1-1
- Update to latest upstream version (fixes fedora#2020121)

* Wed Sep 22 2021 Ken Dreyer <kdreyer@redhat.com> - 2.7.2-1
- Update to latest upstream version (fixes fedora#2001701)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 04 2021 Georg Sauthoff <mail@gms.tf> - 2.7.0-1
- Update to latest upstream version (fixes fedora#1955952)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.5.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Georg Sauthoff <mail@gms.tf> - 2.5.0-1
- Update to latest upstream version (fixes fedora#1910426)
- Also fixes openssl test case, cf. https://github.com/ronf/asyncssh/issues/326
  and https://github.com/openssl/openssl/issues/13471

* Sun Sep 20 2020 Georg Sauthoff <mail@gms.tf> - 2.4.2-1
- Update to latest upstream version

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Georg Sauthoff <mail@gms.tf> - 2.2.1-3
- Be more explicit regarding setuptools depenency,
  cf. https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/GCPGM34ZGEOVUHSBGZTRYR5XKHTIJ3T7/

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.9

* Fri May 01 2020 Georg Sauthoff <mail@gms.tf> - 2.2.1-1
- Update to latest upstream version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Georg Sauthoff <mail@gms.tf> - 2.1.0-1
- Update to latest upstream version

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.16.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.16.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild


* Sat Apr 13 2019 Georg Sauthoff <mail@gms.tf> - 1.16.1-1
- Update to latest upstream version
* Tue Mar 26 2019 Georg Sauthoff <mail@gms.tf> - 1.15.1-1
- Update to more recent upstream version
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Dec  8 2018 Georg Sauthoff <mail@gms.tf> - 1.15.0-1
- Update to latest upstream version
* Sun Sep  9 2018 Georg Sauthoff <mail@gms.tf> - 1.14.0-1
- Update to latest upstream version
* Sat Jul 28 2018 Georg Sauthoff <mail@gms.tf> - 1.13.3-1
- initial packaging
