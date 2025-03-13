
Name:           python-sniffio
Version:        1.3.1
Release:        4%{?dist}
Summary:        Sniff out which async library your code is running under
License:        MIT OR Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/python-trio/sniffio
Source0:       	https://files.pythonhosted.org/packages/source/s/sniffio/sniffio-1.3.1.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires: 	python3-pip
BuildRequires: 	python3-wheel

%global common_description %{expand:
You're writing a library.  You've decided to be ambitious, and support multiple
async I/O packages, like Trio, and asyncio, and ... You've written a bunch of
clever code to handle all the differences.  But... how do you know which piece
of clever code to run?  This is a tiny package whose only purpose is to let you
detect which async library your code is running under.}

%description %{common_description}

%package -n python3-sniffio
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

%description -n python3-sniffio %{common_description}

%prep
%autosetup -n sniffio-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files sniffio

%check
%pytest --verbose

%files -n python3-sniffio -f %{pyproject_files}
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc README.rst

%changelog
* Tue Feb 11 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.3.1-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
- Added `BuildRequires: python3-pip python3-wheel`

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.3.1-2
- Rebuilt for Python 3.13

* Mon Jun 03 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.3.1-1
- Update to version 1.3.1 rhbz#2265958

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 29 2023 Carl George <carlwgeorge@fedoraproject.org> - 1.3.0-1
- Update to version 1.3.0, resolves rhbz#2123340
- Switch to SPDX license notation

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 1.2.0-10
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.2.0-7
- Rebuilt for Python 3.11

* Thu Jan 27 2022 Carl George <carl@george.computer> - 1.2.0-6
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 2020 Joel Capitao <jcapitao@redhat.com> - 1.2.0-1
- Update to 1.2.0 (#1887203)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Carl George <carl@george.computer> - 1.1.0-1
- Latest upstream

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Carl George <carl@george.computer> - 1.0.0-1
- Initial package

