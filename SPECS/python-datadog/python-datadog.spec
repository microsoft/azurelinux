Name:           python-datadog
Version:        0.44.0
Release:        2%{?dist}
Summary:        Python wrapper for the Datadog API
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/DataDog/datadogpy
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/datadogpy-%{version}.tar.gz
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
Datadogpy is a collection of tools suitable for inclusion in existing Python
projects or for development of standalone scripts. It provides an abstraction on
top of Datadog's raw HTTP interface and the Agent's StatsD metrics aggregation
server, to interact with Datadog and efficiently report events and metrics.

%package -n python%{python3_pkgversion}-datadog
Summary:        Python wrapper for the Datadog API
Requires:       python3
Requires:       python3-requests >= 2.6.0

%description -n python%{python3_pkgversion}-datadog
Datadogpy is a collection of tools suitable for inclusion in existing Python
projects or for development of standalone scripts. It provides an abstraction on
top of Datadog's raw HTTP interface and the Agent's StatsD metrics aggregation
server, to interact with Datadog and efficiently report events and metrics.

%prep
%autosetup -n datadogpy-%{version} -p1

%build
%py3_build

%install
%py3_install

# Datadog has deprecated this binary name as it conflicts with the sheepdog
# package, but it still gets built right now.
rm %{buildroot}/%{_bindir}/dog{,wrap}

%check
%{python3} -m pip install tox
tox -e py%{python3_version_nodots} -v

%files -n python%{python3_pkgversion}-datadog
%license LICENSE
%{python3_sitelib}/datadog*
%{_bindir}/dogshell
%{_bindir}/dogshellwrap

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.44.0-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Adding as run dependency for package cassandra medusa
- License verified

* Wed Mar 16 2022 Dalton Miner <daltonminer@gmail.com> - 0.44.0-1
- Update to 0.44.0
- Remove python2/older distribution support

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.23.0-11
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Dalton Miner <daltonminer@gmail.com> - 0.23.0-2
- Added a patch to rename binaries that conflicted with sheepdog
* Thu Oct 25 2018 Dalton Miner <daltonminer@gmail.com> - 0.23.0-1
- Initial packaging
