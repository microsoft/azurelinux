Summary:        Contains a utility for determining file types
Name:           file
Version:        5.45
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://www.darwinsys.com/file
Source0:        http://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Requires:       %{name}-libs = %{version}-%{release}
Conflicts:      toybox

%description
The package contains a utility for determining the type of a
given file or files

%package        libs
Summary:        Library files for file

%description    libs
It contains the libraries to run the application.

%package        devel
Summary:        Header and development files for file
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%package -n python3-magic
Summary:        Python 3 bindings for the libmagic API
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description -n python3-magic
This package contains the Python 3 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%prep
%autosetup -p1

rm -rf %{py3dir}
cp -a python %{py3dir}

%build
%configure \
    --disable-silent-rules
%make_build

cd %{py3dir}
CFLAGS="%{optflags}" python3 setup.py build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

cd %{py3dir}
python3 setup.py install -O1 --skip-build --root %{buildroot}

%check
%make_build check

%ldconfig_scriptlets -n libs

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*man1/*
%{_mandir}/*man4/*

%files libs
%defattr(-,root,root)
%license COPYING
%{_libdir}/libmagic.so.1*
%{_datarootdir}/misc/magic.mgc

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/*man3/*

%files -n python3-magic
%doc python/README.md python/example.py
%{python3_sitelib}/magic.py
%{python3_sitelib}/*egg-info
%{python3_sitelib}/__pycache__/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.45-1
- Auto-upgrade to 5.45 - Azure Linux 3.0 - package upgrades

* Tue Mar 15 2022 Bala <balakumaran.kannan@microsoft.com> - 5.40-2
- Add patch to fix xz mime type reporting

* Tue Sep 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 5.40-1
- Update to latest upstream version
- Move license to libs subpackage
- Change source URL to http version

* Tue Jul 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.38-2
- Adding the "python3-magic" subpackage.

* Mon Jun 08 2020 Joe Schmitt <joschmit@microsoft.com> - 5.38-1
- Update to version 5.38 to resolve CVE-2019-18218.
- License verified.
- Remove sha1 macro.
- Update URL to use https.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.34-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.34-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 20 2018 Sujay G <gsujay@vmware.com> - 5.34-1
- Bump file version to 5.34

* Fri Dec 15 2017 Divya Thaluru <dthaluru@vmware.com> - 5.30-3
- Added seperate package for libraries
- Added toybox as conflict package

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.30-2
- Add devel package.

* Tue Apr 04 2017 Chang Lee <changlee@vmware.com> - 5.30-1
- Updated to version 5.30

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 5.24-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 5.24-1
- Updated to version 5.24

* Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> - 5.22-1
- Initial build. First version
