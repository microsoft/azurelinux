# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           netcdf4-python
Version:        1.7.2
Release:        7%{?dist}.1
Summary:        Python/numpy interface to netCDF

License:        MIT
URL:            https://github.com/Unidata/netcdf4-python
Source0:        https://github.com/Unidata/netcdf4-python/archive/refs/tags/v%{version}rel/%{name}-%{version}.tar.gz
# No rpath for library
# https://github.com/Unidata/netcdf4-python/issues/138
Patch0:         netcdf4-python-norpath.patch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  netcdf-devel
Requires:       python%{python3_pkgversion}-netcdf4 = %{version}-%{release}

%description
netCDF version 4 has many features not found in earlier versions of the
library and is implemented on top of HDF5. This module can read and write
files in both the new netCDF 4 and the old netCDF 3 format, and can create
files that are readable by HDF5 clients. The API modeled after
Scientific.IO.NetCDF, and should be familiar to users of that module.

Most new features of netCDF 4 are implemented, such as multiple unlimited
dimensions, groups and zlib data compression. All the new numeric data types
(such as 64 bit and unsigned integer types) are implemented. Compound and
variable length (vlen) data types are supported, but the enum and opaque data
types are not. Mixtures of compound and vlen data types (compound types
containing vlens, and vlens containing compound types) are not supported.


%package -n python%{python3_pkgversion}-netcdf4
Summary:        Python/numpy interface to netCDF

%description -n python%{python3_pkgversion}-netcdf4
netCDF version 4 has many features not found in earlier versions of the
library and is implemented on top of HDF5. This module can read and write
files in both the new netCDF 4 and the old netCDF 3 format, and can create
files that are readable by HDF5 clients. The API modeled after
Scientific.IO.NetCDF, and should be familiar to users of that module.

Most new features of netCDF 4 are implemented, such as multiple unlimited
dimensions, groups and zlib data compression. All the new numeric data types
(such as 64 bit and unsigned integer types) are implemented. Compound and
variable length (vlen) data types are supported, but the enum and opaque data
types are not. Mixtures of compound and vlen data types (compound types
containing vlens, and vlens containing compound types) are not supported.


%prep
%autosetup -p1 -n %{name}-%{version}rel


%generate_buildrequires
%pyproject_buildrequires


%build
# Set to get libs from ncconfig to avoid directly linking to -lhdf5
export USE_NCCONFIG=1
# This causes the plugins to be duplicated into the python package
# https://github.com/Unidata/netcdf4-python/issues/1263
#export NETCDF_PLUGIN_DIR=%%{_libdir}/hdf5/plugin
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l netCDF4

 
%check
cd test
export NO_NET=1
%ifarch s390x
# FAIL: runTest (tst_compoundvar.VariablesTestCase) -> assert (cmptype4 == dtype4a) # data type should be aligned
# https://github.com/Unidata/netcdf4-python/issues/1124
PYTHONPATH=$(echo ../build/lib.linux-*) %{__python3} run_all.py || :
%else
PYTHONPATH=$(echo ../build/lib.linux-*) %{__python3} run_all.py
%endif


%files
%license LICENSE
%{_bindir}/nc3tonc4
%{_bindir}/nc4tonc3
%{_bindir}/ncinfo


%files -n python%{python3_pkgversion}-netcdf4 -f %{pyproject_files}
%doc Changelog docs examples README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7.2-7.1
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7.2-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Sun Jul 27 2025 Orion Poplawski <orion@nwra.com> - 1.7.2-6
- Use pyproject macros (rhbbz#2377339)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.7.2-4
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 15 2024 Orion Poplawski <orion@nwra.com> - 1.7.2-2
- Rebuild against numpy 2.0 (rhbz#2332500)

* Thu Oct 24 2024 Orion Poplawski <orion@nwra.com> - 1.7.2-1
- Update to 1.7.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 23 2024 Orion Poplawski <orion@nwra.com> - 1.7.1-1
- Update to 1.7.1

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.6.5-4
- Rebuilt for Python 3.13

* Wed May 08 2024 Orion Poplawski <orion@nwra.com> - 1.6.5-4
- Add patch to fix incompatible pointer type (FTBFS)
- Add dependency on python3-certifi (bz#2250858)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Orion Poplawski <orion@nwra.com> - 1.6.5-1
- Update to 1.6.5

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.6.4-2
- Rebuilt for Python 3.12

* Wed Jun 07 2023 Orion Poplawski <orion@nwra.com> - 1.6.4-1
- Update to 1.6.4

* Sun Mar 05 2023 Orion Poplawski <orion@nwra.com> - 1.6.3-1
- Update to 1.6.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Orion Poplawski <orion@nwra.com> - 1.6.2-1
- Update to 1.6.2

* Fri Sep 23 2022 Orion Poplawski <orion@nwra.com> - 1.6.1-1
- Update to 1.6.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 26 2022 Orion Poplawski <orion@nwra.com> - 1.6.0-1
- Update to 1.6.0

* Mon Jun 20 2022 Charalampos Stratakis <cstratak@redhat.com> - 1.5.8-3
- Fix FTBFS with the latest setuptools
Resolves: rhbz#2097125

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.5.8-2
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Orion Poplawski <orion@nwra.com> - 1.5.8-1
- Update to 1.5.8

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 1.5.7-2
- Rebuild for hdf5 1.12.1

* Mon Aug 30 2021 Orion Poplawski <orion@nwra.com> - 1.5.7-1
- Update to 1.5.7

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 1.5.6-4
- Rebuild for netcdf 4.8.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.5.6-2
- Rebuilt for Python 3.10

* Sun Feb 14 2021 Orion Poplawski <orion@nwra.com> - 1.5.6-1
- Update to 1.5.6

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Orion Poplawski <orion@nwra.com> - 1.5.5.1-1
- Update to 1.5.5.1

* Thu Sep 17 20:16:46 MDT 2020 Orion Poplawski <orion@nwra.com> - 1.5.4-1
- Update to 1.5.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.3-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Orion Poplawski <orion@nwra.com> - 1.5.3-1
- Update to 1.5.3

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Sep 10 2019 Orion Poplawski <orion@nwra.com> - 1.5.2-1
- Update to 1.5.2

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.1.2-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May  6 2019 Orion Poplawski <orion@nwra.com> - 1.5.1.2-1
- Update to 1.5.1.2

* Wed May  1 2019 Orion Poplawski <orion@nwra.com> - 1.5.1-1
- Update to 1.5.1

* Tue Apr  2 2019 Orion Poplawski <orion@nwra.com> - 1.5.0.1-1
- Update to 1.5.0.1

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com> - 1.4.3.2-2
- Rebuild for netcdf 4.6.3

* Sat Mar  9 2019 Orion Poplawski <orion@nwra.com> - 1.4.3.2-1
- Update to 1.4.3.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 7 2018 Orion Poplawski <orion@nwra.com> - 1.3.1-1
- Update to 1.3.1
- Drop Python 2 in Fedora (bugz #1634978)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.9-6
- Rebuilt for Python 3.7

* Tue Mar 13 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.9-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2.9-1
- Update to 1.2.9

* Tue Mar 7 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2-7-4
- Provide python-netcdf4

* Thu Mar 2 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2-7-3
- Move python libraries into python?- sub-packages
- Make python3 default for Fedora

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 8 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2.7-1
- Update to 1.2.7

* Wed Dec 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.6-2
- Add upstream patch for python 3.6 support

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.6-1
- Update to 1.2.6

* Tue Nov 29 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.5-1
- Update to 1.2.5
- Enable python 3 for EPEL

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 15 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.4-1
- Update to 1.2.4
- Add pthon2/3-netcdf4 provides

* Fri Mar 11 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.3-1
- Update to 1.2.3
- Drop numpy patch
- Use %%license

* Sun Feb 7 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.2-1
- Update to 1.2.2
- Modernize spec
- Add upstream patch for numpy support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.6-4
- Rebuild for netcdf 4.4.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.6-1
- Update to 1.1.6

* Sat Feb 21 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.4-1
- Update to 1.1.4

* Sun Dec 21 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.3-1
- Update to 1.1.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.9-2
- Rebuild for Python 3.4

* Fri May 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.9-1
- Update to 1.0.9
- Remove rpaths
- Add BR python{,3}-dateutil for tests
- Add BR/R on Cython

* Thu Mar 6 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.8-1
- Update to 1.0.8
- Update URL/source to github

* Thu Feb 6 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.7-1
- Update to 1.0.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 21 2013 Orion Poplawski <orion@cora.nwra.com> - 1.0.2-1
- Update to 1.0.2
- Remove bundled ordereddict (Bug #913528), require it on EL6
- Run tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3.fix1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 12 2012 Orion Poplawski <orion@cora.nwra.com> - 1.0-2.fix1
- Add patch to link only against netcdf

* Thu May 24 2012 Orion Poplawski <orion@cora.nwra.com> - 1.0-1.fix1
- Update to 1.0fix1

* Thu Apr 5 2012 Orion Poplawski <orion@cora.nwra.com> - 0.9.9-1
- Update to 0.9.9

* Thu Sep 8 2011 Orion Poplawski <orion@cora.nwra.com> - 0.9.7-1
- Initial package
