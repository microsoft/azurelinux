%global srcname s3transfer
%global _description \
S3transfer is a Python library for managing Amazon S3 transfers.

Name:           python-%{srcname}
Version:        0.10.4
Release:        1%{?dist}
Summary:        Amazon S3 Transfer Manager

License:        Apache-2.0
URL:            https://pypi.org/project/s3transfer/
Source0:        %{pypi_source}

BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}

BuildRequires:  python3-devel
# required to run the test suite
BuildRequires:  python3dist(botocore) >= 1.12.36
BuildRequires:  python3dist(botocore) < 2.0
BuildRequires:  python3dist(pytest)

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%pytest tests/unit tests/functional

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst


%changelog
* Thu Nov 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.4-1
- 0.10.4

* Thu Oct 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.3-1
- 0.10.3

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.2-1
- 0.10.2

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.10.1-2
- Rebuilt for Python 3.13

* Mon Mar 18 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.10.1-1
- 0.10.1

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.0-1
- Update to 0.10.0 (close RHBZ#2255577; fix RHBZ#2255624)

* Thu Dec 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.9.0-1
- 0.9.0

* Thu Nov 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.8.2-1
- 0.8.2

* Mon Nov 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.8.0-1
- 0.8.0

* Thu Sep 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.7.0-1
- 0.7.0

* Wed Aug 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.6.2-1
- 0.6.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 0.6.1-2
- Rebuilt for Python 3.12

* Fri May 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.6.1-1
- 0.6.1

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.6.0-5
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.6.0-2
- Rebuilt for Python 3.11

* Wed Jun 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.6.0-1
- 0.6.0

* Tue May 10 2022 Major Hayden <major@mhtx.net> - 0.5.2-2
- Switch to pyproject-rpm-macros.

* Fri Feb 25 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.5.2-1
- 0.5.2

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.5.1-1
- 0.5.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.5.0-1
- 0.5.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.2-3
- Rebuilt for Python 3.10

* Fri May 14 2021 Felix Schwarz <fschwarz@fedoraproject.org> - 0.4.2-2
- run test suite as part of the build process

* Fri Apr 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.4.2-1
- 0.4.2

* Thu Apr 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.4.1-1
- 0.4.1

* Mon Apr 19 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.4.0-1
- 0.4.0

* Wed Apr 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.3.7-1
- 0.3.7

* Mon Mar 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.3.6-1
- 0.3.6

* Thu Mar 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.3.5-1
- 0.3.5

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

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
