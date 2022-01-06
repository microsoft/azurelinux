Vendor:         Microsoft Corporation
Distribution:   Mariner
# Disable CMake in-source builds
#   This is a fix for the https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
#   So the beaviour will be the same also in F31 nad F32
%undefine __cmake_in_source_build



# About:
#   https://dev.mysql.com/doc/connectors/en/connector-odbc-installation-source-unix.html
Name:           mysql-connector-odbc
Version:        8.0.23
Release:        3%{?dist}
Summary:        ODBC driver for MySQL
License:        GPLv2 with exceptions
URL:            https://dev.mysql.com/downloads/connector/odbc/

Source0:        http://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/%{name}-%{version}-src.tar.gz
Patch0:         myodbc-64bit.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  mysql-devel >= 8
BuildRequires:  libiodbc-devel
BuildRequires:  libzstd-devel
BuildRequires:  unixODBC-devel

# Required for GUI
#   GUI currently off. To switch it ON, uncomment gtk buildrequires and change CMake argument DISABLE_GUI
#   GUI does not make any sense on headless servers for example, which is a valid use case. I don't want
#   this tiny package to have dependency on X and GTK.
# BuildRequires:  gtk3-devel

%description
An ODBC (rev 3) driver for MySQL, for use with unixODBC.

%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p1

%build
%cmake \
        -DCMAKE_BUILD_TYPE=RelWithDebinfo \
        -DWITH_UNIXODBC=YES \
        -DRPM_BUILD=YES \
        -DMYSQLCLIENT_STATIC_LINKING=OFF \
        -DDISABLE_GUI=YES \
        -DBUILD_SHARED_LIBS=OFF \
        -B %_vpath_builddir \
        -LAH

%cmake_build

%install
%cmake_install

# Remove stuff not to be packaged, this tool is for archive distribution
# https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-installation-binary-unix-tarball.html
rm %{buildroot}%{_bindir}/myodbc-installer

# Remove any file in /usr
find %{buildroot}/usr/ -maxdepth 1 -type f -delete

# Create a symlink for library to offer name that users are used to
ln -sf libmyodbc8w.so %{buildroot}%{_lib64dir}/libmyodbc8.so


# Upstream provides a test suite with functional and regression tests.
# However, some tests fail, so it would deserve some more investigation.
# We don't include the test suite until it works fine.
rm -rf %{buildroot}/usr/test

%files
%license LICENSE.txt
%doc ChangeLog README.txt
%{_lib64dir}/lib*so

%changelog
* Mon Jan 03 2022 Thomas Crain <thcrain@microsoft.com> - 8.0.23-3
- Require mysql-devel instead of community-mysql-devel
- License verified

* Fri Oct 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.23-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Adding a missing BR for 'libiodbc-devel'.
- Updated the library paths to CBL-Mariner ones.
- Using only one '%%cmake' macro to configure the build.

* Fri Feb 05 2021 Lukas Javorsky <ljavorsk@redhat.com> - 8.0.23-1
- Rebase to 8.0.23

* Fri Feb 05 2021 Michal Schorm <mschorm@redhat.com> 8.0.22-3
- Move the plugins to the new location to reflect fix on unixODBC side

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 29 2020 Michal Schorm <mschorm@redhat.com> 8.0.22-1
- Rebase to 8.0.22

* Tue Aug 25 2020 Michal Schorm <mschorm@redhat.com> 8.0.21-2
- Stop building "libmysql_strings.so" and "libmysql_sys.so" as dynamic libraries.
  They are only used inside of this package and we don't ship them, so it's
  perfectly fine to build them statically.

* Mon Aug 10 2020 Michal Schorm <mschorm@redhat.com> 8.0.21-1
- Rebase to 8.0.21
- Force the CMake change regarding the in-source builds also to F31 and F32
- Use CMake macros instead of cmake & make direct commands
- %%cmake macro covers the %%{set_build_flags}, so they are not needed

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Michal Schorm <mschorm@redhat.com> 8.0.20-1
- Rebase to 8.0.20

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Filip Januš <fjanus@redhat.com> 8.0.19-1
- Rebase to 8.0.19
- Resolves: #1790686
- Previous patches were merged by upstream
- src dir name fix

* Thu Nov 7 2019 Filip Januš <fjanus@redhat.com> 8.0.18-1
- Rebase to 8.0.18
- Resolves: #1704529
- Patch1 was updated
- New Buildrequireiment - libzstd-devel
- Was added patch which resolves missing includes

* Tue Sep 3 2019 Filip Januš <fjanus@redhat.com> 8.0.17-1
- Rebase to 8.0.17
- Resolves: #1704529
- Add patch

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 18 2019 Michal Schorm <mschorm@redhat.com> - 8.0.15-1
- Rebase to 8.0.15

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.13-1
- Rebase to 8.0.13
  Resolves: #1569767
  Resolves: #1604908
- Rediff 64bit patch
- Remove obsolete patches
- Add cmake patch
- Disable building with GUI

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.3.10-1
- Use dynamic linking
- Use license macro
- Remove unused patches
- Simplify build

* Tue Jan 02 2018 Michal Schorm <mschorm@redhat.com> - 5.3.9-2
- Begin building against static library, dynamic linking is not supported from 5.3.6 version
  https://bugs.mysql.com/bug.php?id=82202
- Begin building against community-mysql again, MariaDB files used to build this connectors
  are no longer available
- Drop Group tag as it shouldn't be used anymore
- Disable several patches, they need to be examined if still applicable and updated
- Add Provides for the bundled static library

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Jakub Dorňák <jdornak@redhat.com> - 5.3.4-3
- Fix x_free() call
  Resolves: #1173783

* Tue Jun  9 2015 Jakub Dorňák <jdornak@redhat.com> - 5.3.4-1
- Rebase to version 5.3.4

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.3.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Jakub Dorňák <jdornak@redhat.com> - 5.3.2-1
- Rebase to version 5.3.2
- MariaDB 10 compatibility

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Jakub Dorňák <jdornak@redhat.com> - 5.2.6-1
- Update to 2.5.6
  Resolves: #1047895

* Wed Jan  8 2014 Marcin Juszkiewicz <mjuszkiewicz redhat com> - 5.2.5-5
- Build failed because whether to use lib64 or not is done by checking
  list of known 64-bit architectures. So added AArch64 to that list.
  Resolves: #1041348

* Thu Dec 12 2013 Jakub Dorňák <jdornak@redhat.com> - 5.2.5-4
- format-security
  Resolves: #1037209

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Honza Horak <hhorak@redhat.com> - 5.2.5-2
- Avoid potential segfault
  Resolves: #974794

* Fri May 24 2013 Honza Horak <hhorak@redhat.com> - 5.2.5-1
- Update to 5.2.5
- Enlarge buffer size for query string when getting info about tables
  Related: #948619

* Wed Apr  3 2013 Honza Horak <hhorak@redhat.com> - 5.2.4-2
- Fix libdir in cmake for ppc64

* Tue Mar  5 2013 Honza Horak <hhorak@redhat.com> - 5.2.4-1
- Update to 5.2.4

* Fri Mar  1 2013 Honza Horak <hhorak@redhat.com> - 5.1.11-3
- Fix data types for mariadb

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Tom Lane <tgl@redhat.com> 5.1.11-1
- Update to 5.1.11

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Tom Lane <tgl@redhat.com> 5.1.10-1
- Update to 5.1.10

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> 5.1.9-1
- Update to 5.1.9
- Add --with-unixODBC-libs to configure command for safer multilib behavior
Related: #757088

* Wed Mar 23 2011 Tom Lane <tgl@redhat.com> 5.1.8-3
- Rebuild for libmysqlclient 5.5.10 soname version bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Tom Lane <tgl@redhat.com> 5.1.8-1
- Update to 5.1.8
- Deal with mysql packaging changes that prevent us from using mysys
  utility functions directly

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 5.1.5r1144-7
- Correct Source: tag and comment to reflect how to get the tarball

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.1.5r1144-6
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5r1144-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5r1144-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 5.1.5r1144-3
- Fix some 64-bitness issues with unixODBC 2.2.14.

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 5.1.5r1144-2
- Rebuild for unixODBC 2.2.14.
- Fix problem with null username/password specifications

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.5r1144-1
- Update to mysql-connector-odbc 5.1.5r1144, to go with MySQL 5.1.x.
  Note the library name has changed from libmyodbc3 to libmyodbc5.

* Tue Aug  5 2008 Tom Lane <tgl@redhat.com> 3.51.26r1127-1
- Update to mysql-connector-odbc 3.51.26r1127

* Tue Mar 25 2008 Tom Lane <tgl@redhat.com> 3.51.24r1071-1
- Update to mysql-connector-odbc 3.51.24r1071

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 3.51.23r998-1
- Update to mysql-connector-odbc 3.51.23r998

* Wed Dec  5 2007 Tom Lane <tgl@redhat.com> 3.51.14r248-3
- Rebuild for new openssl

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 3.51.14r248-2
- Update License tag to match code.

* Fri Apr 20 2007 Tom Lane <tgl@redhat.com> 3.51.14r248-1
- Update to mysql-connector-odbc 3.51.14r248
Resolves: #236473
- Fix build problem on multilib machines

* Mon Jul 17 2006 Tom Lane <tgl@redhat.com> 3.51.12-2.2
- rebuild

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 3.51.12-2
- Remove DLL-unload cleanup call from connection shutdown (bz#185343)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.51.12-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.51.12-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Tom Lane <tgl@redhat.com> 3.51.12-1
- New package replacing MyODBC.
