Name:           python-sphinxygen
Version:        1.0.2
Release:        7%{?dist}
Summary:        A script to read Doxygen XML output and emit ReST for Sphinx
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# All files under ISC, though some tests and
# unpackaged files are under 0BSD
License:        ISC
URL:            https://gitlab.com/drobilla/sphinxygen
# Source from Pypi does not include all test files
Source:        %{url}/-/archive/v%{version}/sphinxygen-v%{version}.tar.gz#/%{name}-v%{version}.tar.gz
# https://gitlab.com/drobilla/sphinxygen/-/merge_requests/1
Patch:         anonymous-struct.patch

BuildRequires:  sed
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(wheel)
# Needed for tests
BuildRequires:  doxygen
BuildRequires:  python3dist(html5lib)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-webencodings

BuildArch: noarch

%global _description %{expand:
Sphinxygen is a Python module/script that generates Sphinx markup to describe
a C API, from an XML description extracted by Doxygen.}

%description %_description

%package -n python3-sphinxygen
Summary:        %{summary}

%description -n python3-sphinxygen %_description


%prep
%autosetup -p1 -n sphinxygen-v%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files sphinxygen
# fix permissions
chmod 644 %{buildroot}%{python3_sitelib}/sphinxygen/sphinxygen.py
# remove shebang line
sed -i '/^#!\/usr\/bin/d' %{buildroot}%{python3_sitelib}/sphinxygen/sphinxygen.py

# install manpage
mkdir -p %{buildroot}%{_mandir}/man1
install -Dpm 0644 doc/sphinxygen.1 -t %{buildroot}%{_mandir}/man1/

%check
%pytest test


%files -n python3-sphinxygen -f %{pyproject_files}
%doc README.md NEWS
%{_bindir}/sphinxygen
%{_mandir}/man1/sphinxygen.1*
 
%changelog
* Mon Feb 24 2025 Jyoti kanase <v-jykanase@microsoft.com> -  1.0.2-7
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.2-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 08 2023 Benson Muite <benson_muite@emailplus.org> - 1.0.2-2
- Add patch to for change in behavior of Doxygen 1.9.7

* Wed Aug 02 2023 Benson Muite <benson_muite@emailplus.org> - 1.0.2-1
- Upgrade to latest release

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0.0-2
- Rebuilt for Python 3.12

* Thu Feb 09 2023 Benson Muite <benson_muite@emailplus.org> - 1.0.0-1
- Initial packaging
