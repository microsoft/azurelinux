# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global git_url https://github.com/arvidn/libtorrent
 
Name:		rb_libtorrent
Version:	2.0.11
Release:	3%{?dist}
Summary:	A C++ BitTorrent library aiming to be the best alternative

License:	BSD
URL:		https://www.libtorrent.org
Source0:	%{git_url}/releases/download/v%{version}/libtorrent-rasterbar-%{version}.tar.gz
Source1:	%{name}-README-renames.Fedora
Source2:	%{name}-COPYING.Boost
Source3:	%{name}-COPYING.zlib

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	ninja-build
BuildRequires:	openssl-devel
%if 0%{?fedora} && 0%{?fedora} >= 40
BuildRequires:	openssl-devel-engine
%endif
BuildRequires:	pkgconfig(zlib)
BuildRequires:	util-linux

%description
%{name} is a C++ library that aims to be a good alternative to all
the other BitTorrent implementations around. It is a library and not a full
featured client, although it comes with a few working example clients.

Its main goals are to be very efficient (in terms of CPU and memory usage) as
well as being very easy to use both as a user and developer.

%package 	devel
Summary:	Development files for %{name}
License:	BSD and zlib and Boost
Requires:	%{name}%{?_isa} = %{version}-%{release}
## FIXME: Same include directory. :(
Conflicts:	libtorrent-devel
## Needed for various headers used via #include directives...
Requires:	boost-devel
Requires:	pkgconfig(openssl)

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

The various source and header files included in this package are licensed
under the revised BSD, zlib/libpng, and Boost Public licenses. See the various
COPYING files in the included documentation for the full text of these
licenses, as well as the comments blocks in the source code for which license
a given source or header file is released under.

%package	examples
Summary:	Example clients using %{name}
License:	BSD
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	examples
The %{name}-examples package contains example clients which intend to
show how to make use of its various features. (Due to potential
namespace conflicts, a couple of the examples had to be renamed. See the
included documentation for more details.)

%package	python3
Summary:	Python bindings for %{name}
# Automatically converted from old format: Boost - review is highly recommended.
License:	BSL-1.0
BuildRequires:	python3-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-python3-devel
BuildRequires:	python3-setuptools
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	python3
The %{name}-python3 package contains Python language bindings
(the 'libtorrent' module) that allow it to be used from within
Python applications.

%prep
%autosetup -p1 -n "libtorrent-rasterbar-%{version}"

## The RST files are the sources used to create the final HTML files; and are
## not needed.
rm -f docs/*.rst
## Ensure that we get the licenses installed appropriately.
install -p -m 0644 COPYING COPYING.BSD
install -p -m 0644 %{SOURCE2} COPYING.Boost
install -p -m 0644 %{SOURCE3} COPYING.zlib
## Finally, ensure that everything is UTF-8, as it should be.
iconv -t UTF-8 -f ISO_8859-15 AUTHORS -o AUTHORS.iconv
mv AUTHORS.iconv AUTHORS

%build
# This is ugly but can't think of an easier way to build the binding
export CPPFLAGS="$CPPFLAGS $(python%{python3_version}-config --includes)"
export LDFLAGS="$LDFLAGS -L%{_builddir}/libtorrent-rasterbar-%{version}/build/src/.libs"
export PYTHON=/usr/bin/python%{python3_version}
export PYTHON_LDFLAGS="$PYTHON_LDFLAGS $(python%{python3_version}-config --libs)"

%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_SKIP_RPATH=TRUE \
	-GNinja \
	-Dbuild_examples=ON \
	-Dbuild_tests=ON \
	-Dbuild_tools=ON \
	-Dpython-bindings=ON \
	-Dpython-egg-info=ON \
	-Dpython-install-system-dir=OFF
%cmake_build

%check
export LD_LIBRARY_PATH=%{_builddir}/libtorrent-rasterbar-%{version}/%{_vpath_builddir}
pushd %{_vpath_builddir}/test
# Skip UPnP test as it requires a UPnP server on the same network, others due to aarch64 failures
# Make test failures non-fatal as they seem to randomly fail.
echo "set (CTEST_CUSTOM_TESTS_IGNORE
 "test_upnp"
)" > CTestCustom.cmake
ctest -j %{_smp_build_ncpus} || :
popd


%install
mkdir -p %{buildroot}%{_bindir}/

%cmake_install
install -p -m 0755 \
 %{_vpath_builddir}/examples/{client_test,connection_tester,custom_storage,dump_torrent,make_torrent,simple_client,stats_counters,upnp_test} \
 %{_vpath_builddir}/tools/{dht,session_log_alerts} \
 %{buildroot}%{_bindir}/

# Written version is malformed
sed -i 's/^Version:.*/Version: %{version}/' %{buildroot}%{python3_sitearch}/libtorrent.egg-info/PKG-INFO

## Do the renaming due to the somewhat limited %%_bindir namespace.
rename client torrent_client %{buildroot}%{_bindir}/*

install -p -m 0644 %{SOURCE1} ./README-renames.Fedora

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %doc}
%doc AUTHORS ChangeLog
%license COPYING
%{_libdir}/libtorrent-rasterbar.so.2.*
%{_libdir}/libtorrent-rasterbar.so.2.0

%files	devel
%doc docs/
%license COPYING.Boost COPYING.BSD COPYING.zlib
%{_libdir}/pkgconfig/libtorrent-rasterbar.pc
%{_includedir}/libtorrent/
%{_libdir}/libtorrent-rasterbar.so
%{_libdir}/cmake/LibtorrentRasterbar/
%{_datadir}/cmake/Modules/FindLibtorrentRasterbar.cmake

%files examples
%doc README-renames.Fedora
%license COPYING
%{_bindir}/*torrent*
%{_bindir}/connection_tester
%{_bindir}/custom_storage
%{_bindir}/dht
%{_bindir}/session_log_alerts
%{_bindir}/stats_counters
%{_bindir}/upnp_test

%files	python3
%doc AUTHORS ChangeLog
%license COPYING.Boost
%{python3_sitearch}/libtorrent.egg-info/
%{python3_sitearch}/libtorrent.cpython-*.so

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.0.11-2
- Rebuilt for Python 3.14

* Wed Jan 29 2025 Michael Cronenworth <mike@cchtml.com> - 2.0.11-1
- Upgrade to 2.0.11

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.10-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.0.10-2
- Rebuilt for Python 3.13

* Sun Mar 31 2024 Leigh Scott <leigh123linux@gmail.com> - 2.0.10-1
- Upgrade to 2.0.10

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Jonathan Wakely <jwakely@redhat.com> - 2.0.9-4
- Rebuilt for Boost 1.83

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.0.9-2
- Rebuilt for Python 3.12

* Fri May 26 2023 Leigh Scott <leigh123linux@gmail.com> - 2.0.9-1
- Upgrade to 2.0.9

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 2.0.8-3
- Rebuilt for Boost 1.81

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Leigh Scott <leigh123linux@gmail.com> - 2.0.8-1
- Upgrade to 2.0.8

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Leigh Scott <leigh123linux@gmail.com> - 2.0.7-1
- Upgrade to 2.0.7

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.6-4
- Rebuilt for Python 3.11

* Thu May 12 2022 Leigh Scott <leigh123linux@gmail.com> - 2.0.6-3
- Fix pkg-config file (rhbz#2084637)

* Sat May 07 2022 Leigh Scott <leigh123linux@gmail.com> - 2.0.6-2
- Fix i686 build

* Thu May 05 2022 Leigh Scott <leigh123linux@gmail.com> - 2.0.6-1
- Upgrade to 2.0.6

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 2.0.5-3
- Rebuilt for Boost 1.78

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 11 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.5-1
- Upgrade to 2.0.5

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.0.4-6
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 09 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.4-5
- Add fix for deluge files tab

* Sat Aug 07 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.4-4
- Fix build failure, remove python2 and old releases

* Sat Aug 07 2021 Jonathan Wakely <jwakely@redhat.com> - 2.0.4-3
- Rebuilt for Boost 1.76

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Michael Cronenworth <mike@cchtml.com> - 2.0.4-1
- Upgrade to 2.0.4

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.3-2
- Rebuilt for Python 3.10

* Mon May 24 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.3-1
- Upgrade to 2.0.3

* Mon May 24 2021 Leigh Scott <leigh123linux@gmail.com> - 1.2.13-1
- Upgrade to 1.2.13

* Thu Mar 25 2021 Leigh Scott <leigh123linux@gmail.com> - 1.2.12-1
- Upgrade to 1.2.12

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 1.2.11-2
- Rebuilt for Boost 1.75

* Wed Nov 25 2020 Michael Cronenworth <mike@cchtml.com> - 1.2.11-1
- Upgrade to 1.2.11
- Switch to build with cmake

* Fri Oct  9 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.10-2
- Use c++14 to fix LTO issue with qbittorrent

* Thu Oct  8 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.10-1
- Upgrade to 1.2.10

* Thu Aug 06 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.8-1
- Upgrade to 1.2.8
- Remove extra debug flags

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.7-1
- Upgrade to 1.2.7

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.6-7
- Fix conditional so aarch64 is included on fedora

* Thu May 28 2020 Jonathan Wakely <jwakely@redhat.com> - 1.2.6-6
- Rebuilt for Boost 1.73

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-5
- Rebuilt for Python 3.9

* Sat May 23 2020 Michael Cronenworth <mike@cchtml.com> - 1.2.6-4
- Enable aarch64 for EPEL8

* Thu May 21 2020 Michael Cronenworth <mike@cchtml.com> - 1.2.6-3
- Fix my boo-boo with the RHEL macro

* Thu Apr 23 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.6-2
- Fix changelog

* Thu Apr 23 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.6-1
- Upgrade to 1.2.6

* Sat Mar 14 2020 leigh123linux <leigh123linux@googlemail.com> - 1.2.5-1
- Upgrade to 1.2.5

* Tue Feb 11 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.2.4-1
- Upgrade to 1.2.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 14 2019 Jeff Law <law@redhat.com> - 1.2.2-2
- Fix missing #include for gcc-10

* Sun Oct 27 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.2-1
- Upgrade to 1.2.2

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.13-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Michael Cronenworth <mike@cchtml.com> - 1.1.13-3
- Drop python 2 bindings in F31+
  https://fedoraproject.org/wiki/Changes/F31_Mass_Python_2_Package_Removal

* Fri May 03 2019 Michael Cronenworth <mike@cchtml.com> - 1.1.13-2
- Fix python3 build (RHBZ#1705690)

* Fri May 03 2019 Michael Cronenworth <mike@cchtml.com> - 1.1.13-1
- Upgrade to 1.1.13

* Thu Jan 31 2019 Kalev Lember <klember@redhat.com> - 1.1.12-2
- Rebuilt for Boost 1.69

* Wed Jan 30 2019 Michael Cronenworth <mike@cchtml.com> - 1.1.12-1
- Upgrade to 1.1.12

* Wed Jan 30 2019 Jonathan Wakely <jwakely@redhat.com> - 1.1.9-2
- Add patch for Boost 1.69 header changes

* Thu Aug 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.9-1
- Upgrade to 1.1.9

* Mon Jul 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.8-4
- Add  BuildRequires gcc-c++
- Disable checking tests

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.8-2
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.8-1
- Upgrade to 1.1.8

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.7-4
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Michael Cronenworth <mike@cchtml.com> - 1.1.7-3
- Add patch to fix rate limiting (rhbz#1544257)

* Tue May 01 2018 Jonathan Wakely <jwakely@redhat.com> - 1.1.7-2
- Use BuildRequires: boost-python2-devel to fix build with boost-1.66.0-7.fc29

* Fri Apr 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.7-1
- Upgrade to 1.1.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-2
- Rebuild for boost-1.66
- Disable checks till they can be fixed

* Sun Jan 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-1
- Upgrade to 1.1.6

* Sat Nov 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.5-3
- Exclude aarch64 for epel7

* Sat Nov 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.5-2
- Fix build for epel7

* Sat Nov 04 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.5-1
- Upgrade to 1.1.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 1.1.2-5
- Rebuilt for Boost 1.64

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.2-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sun Jul 02 2017 Björn Esser <besser82@fedoraproject.org> - 1.1.2-3
- Fix linking for the Python3 bindings (rhbz#1399390)
- Fix filtering provides
- Clean trailing whitespace

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue Feb 28 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.1.2-1
- Upgrade to 1.1.1

* Fri Feb 17 2017 Jonathan Wakely <jwakely@redhat.com> - 1.1.1-4
- Fix failure test due to asio header order issue

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-3
- Rebuild for Python 3.6

* Thu Oct 06 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.1.1-2
- Fix rpath

* Wed Sep 28 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.1.1-1
- Upgrade to 1.1.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.1.0-1
- Upgrade to 1.1.0

* Mon Mar 14 2016 Przemysław Palacz <pprzemal@gmail.com> - 1.0.9-2
- Fix missing Python 3 binding library

* Sat Mar 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0.9-1
- Upgrade to 1.0.9
- Provide -python3 subpackage as well
- Rename -python subpackage as -python2

* Tue Mar 08 2016 Bruno Wolff III <bruno@wolff.to> - 1.0.8-3
- Rebuild for libtommath soname bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0.8-1
- Upstream release 1.0.8

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 1.0.7-3
- Rebuilt for Boost 1.60

* Mon Dec 07 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0.7-2
- Fixes to make it work properly with python2 on F24+
- Remove README since is not shipped any more

* Sat Nov 14 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0.7-1
- Upstream release 1.0.7

* Sat Oct 17 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.0.6-3
- Link with system tommath, drop bundled one

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.0.6-2
- Rebuilt for Boost 1.59

* Sat Aug 15 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.0.6-1
- Upstream release 1.0.6
- Change source URL
- Install license files properly
- Remove pkgconfig requires
- Clean up requires
- Filter private-shared-object-provides on python sub-package
- Specify version for python buildrequires

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Sun Jul 26 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0.5-1
- Upstream release 1.0.5
- Lint the spec file

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.0.4-3
- rebuild for Boost 1.58

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 18 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-1
- upstream release 1.0.4

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.0.3-2
- Rebuild for boost 1.57.0

* Fri Dec 19 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-1
- upstream release 1.0.3

* Tue Sep 16 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-1
- upstream release 1.0.2

* Mon Aug 18 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-1
- upstream release 1.0.1
- update patches

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 22 2014 Leigh Scott <leigh123linux@googlemail.com> - 0.16.17-1
- upstream release 0.16.17

* Sun Jun 15 2014 Leigh Scott <leigh123linux@googlemail.com> - 0.16.16-4
- patch to stop UPNP from openning port 0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 0.16.16-2
- Rebuild for boost 1.55.0

* Mon Apr 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 0.16.16-1
- upstream release 0.16.16
- fix source url

* Sun Aug 18 2013 Leigh Scott <leigh123linux@googlemail.com> - 0.16.11-1
- upstream release 0.16.11

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Petr Machata <pmachata@redhat.com> - 0.16.10-2
- Rebuild for boost 1.54.0
- Change configure invocation to avoid Boost -mt libraries, which are
  not enabled anymore.
- Adjust libtorrent-rasterbar.pc to not mention -mt
  (rb_libtorrent-0.16.10-boost_mt.patch)
- Add a missing Boost.Noncopyable include
  (rb_libtorrent-0.16.10-boost_noncopyable.patch)

* Mon May 13 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.16.10-1
- upstream release 0.16.10

* Thu May 09 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.16.9-1
- upstream release 0.16.9

* Sun Feb 24 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.16.8-1
- upstream release 0.16.8

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.16.7-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.16.7-2
- Rebuild for Boost-1.53.0

* Wed Jan 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 0.16.7-1
- Update to 0.16.7
- Drop gcc patch

* Sun Sep 30 2012 Leigh Scott <leigh123linux@googlemail.com> - 0.16.4-1
- Update to 0.16.4
- Patch for gcc error

* Mon Aug 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 0.16.3-1
- Update to 0.16.3

* Thu Jul 26 2012 Leigh Scott <leigh123linux@googlemail.com> - 0.16.2-3
- Rebuild for boost-1.50.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 0.16.2-1
- Update to 0.16.2

* Sun Jun 24 2012 leigh scott <leigh123linux@googlemail.com> - 0.16.1-1
- Update to 0.16.1
- Remove the -DBOOST_FILESYSTEM_VERSION=2 bits from spec
- Remove unused configure options

* Tue Mar 20 2012 leigh scott <leigh123linux@googlemail.com> - 0.15.9-1
- Update to 0.15.9

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.8-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.15.8-2
- rebuild for https://fedoraproject.org/wiki/Features/F17Boost148

* Fri Sep 30 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.15.8-1
- Update to 0.15.8

* Mon Aug 01 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.15.7-1
- Update to 0.15.7

* Thu Jul 21 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.15.6-2
- rebuild against boost 1.47.0
- drop defattr, clean stage
- change BR from util-linux-ng to util-linux since former has replaced latter
- drop all patches since none of them are being applied anymore

* Sun Apr 10 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.15.6-1
- Update to 0.15.6

* Wed Apr 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.15.5-4
- really build against boost 1.46.1

* Wed Mar 16 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.15.5-3
- rebuild for boost 1.46.1

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.15.5-2
- Add "R: GeoIP-devel" to -devel subpackage

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.15.5-1
- Update to 0.15.5 (bug 654807, Leigh Scott)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.14.11-3
- Add -DBOOST_FILESYSTEM_VERSION=2 also in pkgconfig .pc file
  (bug 654807, Leigh Scott)

* Tue Feb 08 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- Add -DBOOST_FILESYSTEM_VERSION=2

* Sun Feb 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.14.11-2
- rebuild for new boost

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.14.11-1
- rb_libtorrent-0.14.11
- track lib soname

* Thu Jul 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.14.10-4
- Patch for python2.7 and g++4.5
- Pass -fno-strict-aliasing for now
- Copy from F-13 branch (F-14 branch still used 0.14.8)

* Fri May 28 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.14.10-3
- Patch from Bruno Wolff III to fix DSO linking rhbz565082
- Update spec to match current guidelines

* Fri May 28 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.14.10-2
- Fix E-V-R issue that breaks qbittorrent and deluge for upgrades
- Add default attributes to examples

* Sun Apr 04 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.14.10-1
- Update to new upstream release (0.14.10)

* Fri Mar 12 2010 leigh scott <leigh123linux@googlemail.com> - 0.14.9-1
- Update to new upstream release (0.14.9)
- Fix source URL

* Tue Jan 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.14.8-2
- Rebuild per
  http://lists.fedoraproject.org/pipermail/devel/2010-January/129500.html

* Tue Jan 12 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.14.8-1
- Update to new upstream release (0.14.8)

* Wed Nov 25 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.7-1
- Update to new upstream release (0.14.7)
- Resolves: #541026 (rb_libtorrent 0.14.6 crashes)

* Sun Sep 27 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.6-1
- Update to new upstream release (0.14.6)
- Build against system GeoIP libraries.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.14.4-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.4-1
- Update to new upstream release (0.14.4).
- Drop outdated Boost patch.

* Fri May 08 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.3-2
- Rebuild for the Boost 1.39.0 update.

* Mon Apr 27 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.3-1
- Update to new upstream bug-fix release (0.14.3).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.2-1
- Update to new upstream bug-fix release (0.14.2)
- Drop Python 2.6 and configure fix patches (fixed upstream):
  - python26.patch
  - configure-dont-use-locate.patch

* Fri Jan 16 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.1-2
- Rebuild for the soname bump in openssl-0.9.8j

* Mon Jan 05 2009 Peter Gordon <peter@thecodergeek.com> - 0.14.1-1
- Update to new upstream release (0.14.1)
- Add asio-devel as runtime dependency for the devel subpackage (#478589)
- Add patch to build with Python 2.6:
  + python26.patch
- Add patch to make the configure script use the proper python include
  directory instead of calling locate, as that can cause failures in a chroot
  with no db file (and is a bit silly in the first place):
  + configure-dont-use-locate.patch
- Drop manual setup.py for building the python module (fixed upstream):
  - setup.py
- Update Source0 URL back to SourceForge's hosting.
- Reenable the examples, since the Makefiles are fixed.

* Fri Dec 19 2008 Petr Machata <pmachata@redhat.com> - 0.13.1-7
- Rebuild for boost-1.37.0.

* Wed Dec 17 2008 Benjamin Kosnik  <bkoz@redhat.com> - 0.13.1-6
- Rebuild for boost-1.37.0.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.13.1-5
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.13.1-4
- Rebuild for Python 2.6

* Thu Nov 20 2008 Peter Gordon <peter@thecodergeek.com>
- Update Source0 URL, for now.

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13.1-3
- fix license tag

* Mon Jul 14 2008 Peter Gordon <peter@thecodergeek.com> - 0.13.1-2
- Add python bindings in a -python subpackage.

* Mon Jul 14 2008 Peter Gordon <peter@thecodergeek.com> - 0.13.1-1
- Update to new upstream release (0.13.1): Contains an incompatible ABI/API
  bump.
- Drop GCC 4.3 patch (fixed upstream):
  - gcc43.patch
- Disable building the examples for now. (Attempted builds fail due to missing
  Makefile support.)
- Drop the source permissions and pkgconfig file tweaks (fixed upstream).

* Sat Feb 09 2008 Peter Gordon <peter@thecodergeek.com> - 0.12.1-1
- Update to new upstream bug-fix release (0.12.1)
- Rebuild for GCC 4.3
- Drop security fix patch (merged upstream):
  - svn1968-bdecode_recursive-security-fix.patch
- Add GCC 4.3 build fixes (based on patch from Adel Gadllah, bug 432778):
  + gcc43.patch

* Mon Jan 28 2008 Peter Gordon <peter@thecodergeek.com> - 0.12-3
- Add upstream patch (changeset 1968) to fix potential security vulnerability:
  malformed messages passed through the bdecode_recursive routine could cause
  a potential stack overflow.
  + svn1968-bdecode_recursive-security-fix.patch

* Fri Aug 03 2007 Peter Gordon <peter@thecodergeek.com> - 0.12-2
- Rebuild against new Boost libraries.

* Thu Jun 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.12-1
- Update to new upstream release (0.12 Final)
- Split examples into a subpackage. Applications that use rb_libtorrent
  don't need the example binaries installed; and splitting the package in this
  manner is a bit more friendly to multilib environments.

* Sun Mar 11 2007 Peter Gordon <peter@thecodergeek.com> - 0.12-0.rc1
- Update to new upstream release (0.12 RC).
- Forcibly use the system libtool to ensure that we remove any RPATH hacks.

* Sun Jan 28 2007 Peter Gordon <peter@thecodergeek.com> - 0.11-5
- Fix installed pkgconfig file: Strip everything from Libs except for
  '-ltorrent', as its [libtorrent's] DSO will ensure proper linking to other
  needed libraries such as zlib and boost_thread. (Thanks to Michael Schwendt
  and Mamoru Tasaka; bug #221372)

* Sat Jan 27 2007 Peter Gordon <peter@thecodergeek.com> - 0.11-4
- Clarify potential licensing issues in the -devel subpackage:
  + COPYING.zlib
  + COPYING.Boost
- Add my name in the Fedora-specific documentation (README-renames.Fedora) and
  fix some spacing issues in it.
- Strip the @ZLIB@ (and thus, the extra '-lz' link option) from the installed
  pkgconfig file, as that is only useful when building a statically-linked
  libtorrent binary.
- Fix conflict: The -devel subpackage should conflict with the -devel
  subpackage of libtorrent, not the main package.
- Preserve timestamps in %%install.

* Wed Jan 17 2007 Peter Gordon <peter@thecodergeek.com> - 0.11-3
- Fix License (GPL -> BSD)
- Don't package RST (docs sources) files.
- Only make the -devel subpackage conflict with libtorrent-devel.
- Rename some of the examples more appropriately; and add the
  README-renames.Fedora file to %%doc which explains this.

* Fri Jan 05 2007 Peter Gordon <peter@thecodergeek.com> - 0.11-2
- Add Requires: pkgconfig to the -devel subpackage since it installs a .pc
  file.

* Wed Jan 03 2007 Peter Gordon <peter@thecodergeek.com> - 0.11-1
- Initial packaging for Fedora Extras
