# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-pickleshare
Version:        0.7.5
Release: 24%{?dist}
Summary:        Tiny 'shelve'-like database with concurrency support

License:        MIT
URL:            https://github.com/ipython/pickleshare
Source:         %{pypi_source pickleshare}

BuildArch:      noarch
 
BuildRequires:  python3-devel

%global _description %{expand:
PickleShare - a small ‘shelve’ like data store with concurrency support.

Like shelve, a PickleShareDB object acts like a normal dictionary. 
Unlike shelve, many processes can access the database simultaneously. 
Changing a value in database is immediately visible to other processes 
accessing the same database.

Concurrency is possible because the values are stored in separate files. 
Hence the “database” is a directory where all files are governed 
by PickleShare.}

%description %_description

%package -n     python3-pickleshare
Summary:        %{summary}

%description -n python3-pickleshare %_description


%prep
%autosetup -n pickleshare-%{version}

# fix interpreter
sed -i 's/\/usr\/bin\/env python/\/usr\/bin\/python/' pickleshare.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%pyproject_install
%pyproject_save_files -l pickleshare


%check
%pyproject_check_import


%files -n python3-pickleshare -f %{pyproject_files}


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.5-23
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.5-22
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.5-20
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Michel Lind <salimma@fedoraproject.org> - 0.7.5-18
- Modernize spec to follow latest packaging guidelines
- Update URL

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.5-16
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.7.5-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.7.5-9
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.7.5-6
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.5-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 11 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.7.5-1
- Update to 0.7.5

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-15
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-14
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-12
- Subpackage python2-pickleshare has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-9
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7.4-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-4
- Rebuild for Python 3.6

* Wed Nov 16 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.7.4-3
- Do not own __pycache__ dir

* Sat Oct 01 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.7.4-2
- Fix typos and interpreter strings

* Sat Sep 24 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4

* Fri Aug 12 2016 Mukundan Ragavan <nonamedotc@gmail.com> - 0.7.3-1
- Initial package.
