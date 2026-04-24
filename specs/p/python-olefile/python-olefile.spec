# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-olefile
Version:        0.47
Release: 13%{?dist}
Summary:        Python package to parse, read and write Microsoft OLE2 files

%global         srcname         olefile
%global         _description    %{expand:
olefile is a Python package to parse, read and write Microsoft OLE2 files
(also called Structured Storage, Compound File Binary Format or Compound
Document File Format), such as Microsoft Office 97-2003 documents,
vbaProject.bin in MS Office 2007+ files, Image Composer and FlashPix files,
Outlook messages, StickyNotes, several Microscopy file formats, McAfee
antivirus quarantine files, etc.
}

License:        BSD-2-Clause
URL:            https://github.com/decalage2/olefile
Source0:        %{pypi_source olefile %version zip}

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  dos2unix
BuildRequires:  /usr/bin/find

%description %{_description}

%package doc
Summary:        %{summary}
BuildArch:      noarch
# Fedora >= 31 does not have python2-sphinx anymore.
# There is python-sphinx in RHEL 7, but it's possibly too old.
# Python26 sphinx works
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%description doc %{_description}
This package contains documentation for %{name}.


%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{srcname} %{_description}
Python3 version.


%prep
%autosetup -p1 -n %{srcname}-%{version}

# Fix windows EOL
find ./ -type f -name '*.py' -exec dos2unix '{}' ';'
dos2unix doc/*.rst


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel
make -C doc html BUILDDIR=_doc_build SPHINXBUILD=sphinx-build-%{python3_version}


%install
%pyproject_install
%pyproject_save_files -l olefile


%check
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} tests/test_olefile.py


%files doc
%doc doc/_doc_build/html

%files -n python3-%{srcname}  -f %{pyproject_files}
%doc README.md
%license doc/License.rst


%changelog
* Sat Dec 27 2025 Sandro Mani <manisandro@gmail.com> - 0.47-12
- Fix project URL

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.47-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.47-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Sandro Mani <manisandro@gmail.com> - 0.47-8
- Use pyproject macros

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.47-7
- Rebuilt for Python 3.14

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.47-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 03 2023 Sandro Mani <manisandro@gmail.com> - 0.47-1
- Update to 0.47

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.46-20
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.46-17
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.46-14
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Sandro Mani <manisandro@gmail.com> - 0.46-11
- Build python2 subpackage on F33, python2-pillow is still around

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.46-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Michal Ambroz <rebus AT_ seznam.cz> - 0.46-8
- rebuild for new version of oletools
- conditional stop building python2 subpackage on fc>32 and rhel>8
- split doc to separate subpackage

* Mon Oct 07 2019 Sandro Mani <manisandro@gmail.com> - 0.46-7
- BR: python-setuptools (#1758972)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.46-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.46-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 Sandro Mani <manisandro@gmail.com> - 0.46-3
- Drop docs in python2 build

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 11 2018 Sandro Mani <manisandro@gmail.com> - 0.46-1
- Update to 0.46

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.45.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.45.1-2
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Sandro Mani <manisandro@gmail.com> - 0.45.1-1
- Update to 0.45.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 04 2017 Robert Scheck <robert@fedoraproject.org> - 0.44-4
- Added spec file conditionals to build for EPEL 7 (#1498616)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Sandro Mani <manisandro@gmail.com> - 0.44-1
- Update to 0.44

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.4.gitbc9d196
- Fix incorrect line endings
- Remove shebang from non-executable scripts

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.3.gitbc9d196
- Further reduce duplicate text
- Add python_provides

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.2.gitbc9d196
- Use %%py_build and %%py_install macros
- Use %%summary, %%url to reduce duplicate text
- Add %%check
- Move BR to subpackages

* Mon Jan 02 2017 Sandro Mani <manisandro@gmail.com> - 0.44-0.1.gitbc9d196
- Initial package
