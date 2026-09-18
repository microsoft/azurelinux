# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global common_description %{expand:
websocket-client is a WebSocket client for Python.  It provides access to low
level APIs for WebSockets.  websocket-client implements version hybi-13 of the
WebSocket protocol.  This client does not currently support the
permessage-deflate extension from RFC 7692.}


Name:               python-websocket-client
Version:            1.8.0
Release:            7%{?dist}
Summary:            WebSocket client for python
License:            Apache-2.0
URL:                https://github.com/websocket-client/websocket-client
BuildArch:          noarch
Source:             %{pypi_source websocket_client}

# https://github.com/websocket-client/websocket-client/pull/998
Patch:              0001-Include-pytest-in-test-extra.patch


%description %{common_description}


%package -n python3-websocket-client
Summary:            %{summary}
BuildRequires:      python3-devel


%description -n python3-websocket-client %{common_description}


%prep
%autosetup -p 1 -n websocket_client-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l websocket


%check
%pytest -v websocket/tests


%files -n python3-websocket-client -f %{pyproject_files}
%doc README.md ChangeLog
%{_bindir}/wsdump


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.8.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.8.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.8.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 30 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.8.0-2
- Remove explicit pytest buildreq by including it in the test extra
- Remove duplicate license file

* Fri Aug 30 2024 Michel Lind <salimma@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0
- Don't use macros for names
- Resolves: rhbz#2276771

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.7.0-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.7.0-2
- Rebuilt for Python 3.13

* Mon Apr 15 2024 Lumír Balhar <lbalhar@redhat.com> - 1.7.0-1
- Update to 1.7.0 (rhbz#2121193)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.3.3-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Major Hayden <major@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1.3.2-2
- Rebuilt for Python 3.11

* Wed Apr 06 2022 Major Hayden <major@mhtx.net> - 1.3.2-1
- Update to 1.3.2

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Carl George <carl@george.computer> - 1.2.3-1
- Latest upstream
- Resolves: rhbz#1990682

* Sun Aug 01 2021 Carl George <carl@george.computer> - 1.1.0-1
- Latest upstream
- Resolves: rhbz#1934343

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.57.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.57.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.57.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Joel Capitao <jcapitao@redhat.com> - 0.57.0-1
- Update to 0.57.0
- Remove python2 subpackage

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.56.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.56.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.56.0-4
- Rebuilt for Python 3.8

* Wed Aug 07 2019 Carl George <carl@george.computer> - 0.56.0-3
- Disable python2 subpackage on F31+ rhbz#1738467

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Carl George <carl@george.computer> - 0.56.0-1
- Latest upstream

* Tue Feb 12 2019 Yatin Karel <ykarel@redhat.com> - 0.54.0-1
- Update to 0.54.0
- Change license to BSD as source has changed it.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.53.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 28 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.53.0-1
- Update to 0.53.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.47.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.47.0-3
- Rebuilt for Python 3.7

* Tue Mar 27 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.47.0-2
- Conditionalize the Python 2 subpackage
- Don't build the Python 2 subpackage on EL > 7

* Mon Mar 26 2018 Jan Beran <jberan@redhat.com> - 0.47.0-1
- Latest upstream (rhbz# 1548228)
- Fixes python3-websocket-client requires both Python 2 and 3 (rhbz# 1531541)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Carl George <carl@george.computer> - 0.46.0-1
- Latest upstream rhbz#1462523
- Only ship one version of wsdump
- Properly install LICENSE file
- Remove tests from buildroot
- Use Python build, install, and provides macros

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.40.0-4
- Python 2 binary package renamed to python2-websocket-client
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.40.0-3
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Ralph Bean <rbean@redhat.com> - 0.40.0-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.37.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Ralph Bean <rbean@redhat.com> - 0.37.0-1
- new version

* Mon Apr 04 2016 Ralph Bean <rbean@redhat.com> - 0.35.0-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 Ralph Bean <rbean@redhat.com> - 0.34.0-1
- new version

* Tue Oct 27 2015 Ralph Bean <rbean@redhat.com> - 0.33.0-1
- new version

* Mon Jul 27 2015 Ralph Bean <rbean@redhat.com> - 0.32.0-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May 22 2014 Ralph Bean <rbean@redhat.com> - 0.14.1-1
- Latest upstream with python3 support.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Ralph Bean <rbean@redhat.com> - 0.10.0-1
- Latest upstream release.
- Removed executable bit from installed lib files for rpmlint.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 0.9.0-2
- Replaced websocket_client with %%{eggname} as per review by Palle Ravn
  https://bugzilla.redhat.com/show_bug.cgi?id=909644#c4
- Removed a few unnecessary newlines.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 0.9.0-1
- Latest upstream.

* Sat Feb 09 2013 Ralph Bean <rbean@redhat.com> - 0.8.0-1
- Initial package for Fedora
