Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname s3transfer
%global _description \
S3transfer is a Python library for managing Amazon S3 transfers.

Name:           python-%{srcname}
Version:        0.3.4
Release:        2%{?dist}
Summary:        Amazon S3 Transfer Manager

License:        ASL 2.0
URL:            https://pypi.org/project/s3transfer/
Source0:        %{pypi_source}

BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}
rm -vrf *.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.4-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Tue Jan 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.3.4-1
- 0.3.4

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-2
- Rebuilt for Python 3.9

* Thu Mar 12 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.3.3-1
- 0.3.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.3.0-1
- Update to 0.3.0 (rhbz#1717156)

* Tue Nov 19 2019 Orion Poplawski <orion@nwra.com> - 0.2.1-1
- Update to 0.2.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.13-5
- Bump spec to ensure rawhide version > stable releases

* Mon Jan 14 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.13-2
- specify python3 subpackage in files section

* Thu Dec 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.13-1
- Initial package
