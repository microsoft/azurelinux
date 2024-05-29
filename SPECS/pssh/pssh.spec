%{?python_enable_dependency_generator}
%global pypi_name pssh

Name:           %{pypi_name}
Version:        2.3.5
Release:        6%{?dist}
Summary:        PSSH provides parallel version of OpenSSH and related tools

License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/lilydjwg/%{pypi_name}
Source0:        https://github.com/lilydjwg/pssh/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel


%description
This package provides various parallel tools based on ssh and scp.
Parallell version includes:
 o ssh : pssh
 o scp : pscp
 o nuke : pnuke
 o rsync : prsync
 o slurp : pslurp

%prep
%autosetup
sed -i -e '1 d' psshlib/askpass_{client,server}.py
sed -i 's/print \([^()]*\)/print (\1)/g' test/test.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

install -D -m 0755 %{buildroot}%{_bindir}/pssh-askpass \
    %{buildroot}%{_libexecdir}/pssh/pssh-askpass
rm -f %{buildroot}%{_bindir}/pssh-askpass
mv %{buildroot}%{_bindir}/pscp %{buildroot}%{_bindir}/pscp.pssh
install -d %{buildroot}%{_mandir}/man1
install -p -m 0644 man/man1/*.1  %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_mandir}/man1/pscp.1 %{buildroot}%{_mandir}/man1/pscp.pssh.1

# No tests, test.py script requires setup for host and user to do ssh communication
# %check
# python3 test/test.py

%files
%license COPYING
%doc AUTHORS ChangeLog
%{_bindir}/pnuke
%{_bindir}/prsync
%{_bindir}/pscp.pssh
%{_bindir}/pslurp
%{_bindir}/pssh
%{_mandir}/man1/pnuke.1*
%{_mandir}/man1/prsync.1*
%{_mandir}/man1/pscp.pssh.1*
%{_mandir}/man1/pslurp.1*
%{_mandir}/man1/pssh.1*
%{_libexecdir}/pssh
%{python3_sitelib}/pssh-%{version}*
%{python3_sitelib}/psshlib

%changelog
* Mon May 20 2024 Alberto David Perez Guevara <aperezguevaar@microsoft.com> - 2.3.5-6
- Initial Azure Linux import from Fedora 40 (license: MIT).
- License verified

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.3.5-2
- Rebuilt for Python 3.12

* Sun Mar 26 2023 Terje Rosten <terje.rosten@ntnu.no> - 2.3.5-1
- 2.3.5

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.4-2
- Rebuilt for Python 3.11

* Tue Mar 1 2022 Pat Riehecky <riehecky@fnal.gov> - 2.3.4-1
- Sync up with upstream

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.3.1-32
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-29
- Rebuilt for Python 3.9

* Mon Apr 13 2020 Terje Rosten <terje.rosten@ntnu.no> - 2.3.1-28
- Add patch to fix Python 3.8 issue bz#1822306

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
