# If a new upstream release changes some, but not all of these
# version numbers, remember to keep the Release tag in order to
# allow clean upgrades!
%global path_utils_version 0.2.1
%global dhash_version 0.5.0
%global collection_version 0.7.0
%global ref_array_version 0.1.5
%global basicobjects_version 0.1.1
%global ini_config_version 1.3.1
Summary:        "Ding is not GLib" assorted utility libraries
Name:           ding-libs
Version:        0.6.2
Release:        55%{?dist}
License:        LGPLv3+ AND GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/SSSD/ding-libs
Source0:        https://github.com/SSSD/ding-libs/releases/download/%{version}/%{name}-%{version}.tar.gz

### Patches ###

### Build Dependencies ###

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  doxygen
BuildRequires:  pkgconfig
BuildRequires:  check-devel
BuildRequires:  make

### Dependencies ###
# ding-libs is a meta-package that will pull in all of its own
# sub-packages
Requires:       libpath_utils = %{path_utils_version}-%{release}
Requires:       libdhash = %{dhash_version}-%{release}
Requires:       libcollection = %{collection_version}-%{release}
Requires:       libref_array = %{ref_array_version}-%{release}
Requires:       libbasicobjects = %{basicobjects_version}-%{release}
Requires:       libini_config = %{ini_config_version}-%{release}

%description
A meta-package that pulls in libcollection, libdhash, libini_config,
librefarray libbasicobjects, and libpath_utils.

%package devel
Summary:        Development packages for ding-libs
License:        LGPLv3+

# ding-libs is a meta-package that will pull in all of its own
# sub-packages
Requires:       libpath_utils-devel = %{path_utils_version}-%{release}
Requires:       libdhash-devel = %{dhash_version}-%{release}
Requires:       libcollection-devel = %{collection_version}-%{release}
Requires:       libref_array-devel = %{ref_array_version}-%{release}
Requires:       libbasicobjects-devel = %{basicobjects_version}-%{release}
Requires:       libini_config-devel = %{ini_config_version}-%{release}

%description devel
A meta-package that pulls in development libraries for libcollection,
libdhash, libini_config, librefarray and libpath_utils.

##############################################################################
# Path Utils
##############################################################################

%package -n libpath_utils
Summary:        Filesystem Path Utilities
Version:        %{path_utils_version}
License:        LGPLv3+

%description -n libpath_utils
Utility functions to manipulate filesystem pathnames

%package -n libpath_utils-devel
Summary:        Development files for libpath_utils
Version:        %{path_utils_version}
License:        LGPLv3+

Requires:       libpath_utils = %{path_utils_version}-%{release}

%description -n libpath_utils-devel
Utility functions to manipulate filesystem pathnames

%ldconfig_scriptlets -n libpath_utils

%files -n libpath_utils
%doc COPYING COPYING.LESSER
%{_libdir}/libpath_utils.so.1
%{_libdir}/libpath_utils.so.1.0.1

%files -n libpath_utils-devel
%{_includedir}/path_utils.h
%{_libdir}/libpath_utils.so
%{_libdir}/pkgconfig/path_utils.pc
%doc path_utils/README.path_utils
%doc path_utils/doc/html/


##############################################################################
# dhash
##############################################################################

%package -n libdhash
Summary:        Dynamic hash table
Version:        %{dhash_version}
License:        LGPLv3+

%description -n libdhash
A hash table which will dynamically resize to achieve optimal storage & access
time properties

%package -n libdhash-devel
Summary:        Development files for libdhash
Version:        %{dhash_version}
License:        LGPLv3+

Requires:       libdhash = %{dhash_version}-%{release}

%description -n libdhash-devel
A hash table which will dynamically resize to achieve optimal storage & access
time properties

%ldconfig_scriptlets -n libdhash

%files -n libdhash
%doc COPYING COPYING.LESSER
%{_libdir}/libdhash.so.1
%{_libdir}/libdhash.so.1.1.0

%files -n libdhash-devel
%{_includedir}/dhash.h
%{_libdir}/libdhash.so
%{_libdir}/pkgconfig/dhash.pc
%doc dhash/README.dhash
%doc dhash/examples/*.c


##############################################################################
# collection
##############################################################################
%package -n libcollection
Summary:        Collection data-type for C
Version:        %{collection_version}
License:        LGPLv3+

%description -n libcollection
A data-type to collect data in a hierarchical structure for easy iteration
and serialization

%package -n libcollection-devel
Summary:        Development files for libcollection
Version:        %{collection_version}
License:        LGPLv3+

Requires:       libcollection = %{collection_version}-%{release}

%description -n libcollection-devel
A data-type to collect data in a hierarchical structure for easy iteration
and serialization

%ldconfig_scriptlets -n libcollection


%files -n libcollection
%doc COPYING
%doc COPYING.LESSER
%{_libdir}/libcollection.so.*

%files -n libcollection-devel
%{_includedir}/collection.h
%{_includedir}/collection_tools.h
%{_includedir}/collection_queue.h
%{_includedir}/collection_stack.h
%{_libdir}/libcollection.so
%{_libdir}/pkgconfig/collection.pc
%doc collection/doc/html/


##############################################################################
# ref_array
##############################################################################

%package -n libref_array
Summary:        A refcounted array for C
Version:        %{ref_array_version}
License:        LGPLv3+

%description -n libref_array
A dynamically-growing, reference-counted array

%package -n libref_array-devel
Summary:        Development files for libref_array
Version:        %{ref_array_version}
License:        LGPLv3+

Requires:       libref_array = %{ref_array_version}-%{release}

%description -n libref_array-devel
A dynamically-growing, reference-counted array

%ldconfig_scriptlets -n libref_array

%files -n libref_array
%doc COPYING
%doc COPYING.LESSER
%{_libdir}/libref_array.so.1
%{_libdir}/libref_array.so.1.2.1

%files -n libref_array-devel
%{_includedir}/ref_array.h
%{_libdir}/libref_array.so
%{_libdir}/pkgconfig/ref_array.pc
%doc refarray/README.ref_array
%doc refarray/doc/html/

##############################################################################
# basicobjects
##############################################################################

%package -n libbasicobjects
Summary:        Basic object types for C
Version:        %{basicobjects_version}
License:        GPLv3+

%description -n libbasicobjects
Basic object types

%package -n libbasicobjects-devel
Summary:        Development files for libbasicobjects
Version:        %{basicobjects_version}
License:        GPLv3+

Requires:       libbasicobjects = %{basicobjects_version}-%{release}

%description -n libbasicobjects-devel
Basic object types

%ldconfig_scriptlets -n libbasicobjects

%files -n libbasicobjects
%doc COPYING
%doc COPYING.LESSER
%{_libdir}/libbasicobjects.so.0
%{_libdir}/libbasicobjects.so.0.1.0

%files -n libbasicobjects-devel
%{_includedir}/simplebuffer.h
%{_libdir}/libbasicobjects.so
%{_libdir}/pkgconfig/basicobjects.pc

##############################################################################
# ini_config
##############################################################################

%package -n libini_config
Summary:        INI file parser for C
Version:        %{ini_config_version}
License:        LGPLv3+

Requires:       libcollection%{?_isa} = %{collection_version}-%{release}
Requires:       libref_array%{?_isa} = %{ref_array_version}-%{release}
Requires:       libbasicobjects%{?_isa} = %{basicobjects_version}-%{release}
Requires:       libpath_utils%{?_isa} = %{path_utils_version}-%{release}

%description -n libini_config
Library to process config files in INI format into a libcollection data
structure

%package -n libini_config-devel
Summary:        Development files for libini_config
Version:        %{ini_config_version}
License:        LGPLv3+

Requires:       libini_config = %{ini_config_version}-%{release}
Requires:       libcollection-devel = %{collection_version}-%{release}
Requires:       libref_array-devel = %{ref_array_version}-%{release}
Requires:       libbasicobjects-devel = %{basicobjects_version}-%{release}

%description -n libini_config-devel
Library to process config files in INI format into a libcollection data
structure

%ldconfig_scriptlets -n libini_config

%files -n libini_config
%doc COPYING
%doc COPYING.LESSER
%{_libdir}/libini_config.so.5
%{_libdir}/libini_config.so.5.2.1

%files -n libini_config-devel
%{_includedir}/ini_config.h
%{_includedir}/ini_configobj.h
%{_includedir}/ini_valueobj.h
%{_includedir}/ini_comment.h
%{_includedir}/ini_configmod.h
%{_libdir}/libini_config.so
%{_libdir}/pkgconfig/ini_config.pc
%doc ini/doc/html/


##############################################################################
# Build steps
##############################################################################

%prep
%autosetup -S git

%build
autoreconf -ivf
%configure \
    --disable-static

make %{?_smp_mflags} all docs

%check
make %{?_smp_mflags} check

%install
make install DESTDIR=%{buildroot}

# Remove .la files created by libtool
rm -f %{buildroot}/%{_libdir}/*.la

# Remove the example files from the output directory
# We will copy them directly from the source directory
# for packaging
rm -f \
    %{buildroot}%{_datadir}/doc/ding-libs/README.* \
    %{buildroot}%{_datadir}/doc/ding-libs/examples/dhash_example.c \
    %{buildroot}%{_datadir}/doc/ding-libs/examples/dhash_test.c

# Remove document install script. RPM is handling this
rm -f */doc/html/installdox

%changelog
* Wed Jan 17 2024 Alberto Perez <aperezguevar@microsoft.com> - 0.6.2-55
- Upgrade ding-libs to version 0.6.2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jan 25 2022 Alexey Tikhonov <atikhono@redhat.com> - 0.6.2-51
- New upstream release 0.6.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-47
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Sep 02 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.1-45
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 Michal Židek <mzidek@redhat.com> - 0.6.1-41
- Resolves: rhbz#1603785 - ding-libs: FTBFS in Fedora rawhide

* Fri Jul 20 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.6.1-40
- BuildRequires: gcc
- Resolves: rhbz#1603785 - ding-libs: FTBFS in Fedora rawhide

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.1-37
- Switch to %%ldconfig_scriptlets

* Thu Nov 16 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.1-36
- INI: Remove definiton of TRACE_LEVEL

* Tue Nov 14 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.1-35
- INI: Silence ini_augment match failures

* Wed Oct 04 2017 Lukas Slebodnik <lslebodn@redhat.com> - 0.6.1-34
- New upstream release 0.6.1

* Wed Aug 09 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.0-33
- Backport INI merge detection support
- Migrate to autosetup

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 23 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.6.0-29
- New upstream release 0.6.0
- https://fedorahosted.org/sssd/wiki/Releases/DingNotes-0.6.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Robbie Harwood <rharwood@redhat.com> - 0.5.0-27
- Merge most changes from the upstream spec file

* Wed Aug 26 2015 Robbie Harwood <rharwood@redhat.com> - 0.5.0-26
- New upstream release 0.5.0
- https://fedorahosted.org/sssd/wiki/Releases/DingNotes-0.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Jakub Hrozek <jhrozek@redhat.com> 0.4.0-22
- New upstream release 0.4.0
- https://fedorahosted.org/sssd/wiki/Releases/DingNotes-0.4.0

* Sat Jan 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.3.0.1-21
- Fix FTBFS on rawhide
- update spec

* Fri Sep 27 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0.1-20
- Merge Doxygen patch from f19 branch to avoid regressions

* Fri Sep 27 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0.1-19
- Apply a patch by Dmitri Pal to strip trailing whitespace

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0.1-17
- Apply patch by Ondrej Kos to bump libtool version info

* Fri Apr 05 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0.1-16
- Fix libiniconfig_devel Requires

* Thu Apr 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0.1-15
- Increase the release number to -13 to allow clean upgrade path from
  0.2 since some of the components kept their version the same in 0.3

* Mon Apr 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.3.0.1-3
- Bumping revision to fix build glitch

* Fri Mar 29 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0.1-1
- New upstream release 0.3.0.1
- https://fedorahosted.org/sssd/wiki/Releases/DingNotes-0.3.0.1
- obsoletes patch0001

* Thu Mar 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0-2
- Remove cast to allow INI to work on 32bits

* Thu Mar 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.3.0-1
- New upstream release 0.3.0
- https://fedorahosted.org/sssd/wiki/Releases/DingNotes-0.3.0

* Mon Mar 25 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.2.91-14
- include a patch to get rid of autoreconf warnings
- run autoreconf before configure
- Resolves: #925258

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.91-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 31 2012 Ondrej Kos <okos@redhat.com> - 0.2.91-12
- Fixes missing devel dependency

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.91-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Jan Zeleny <jzeleny@redhat.com> - 0.2.91-10
- a bunch of fixes in spec file

* Fri May 25 2012 Jan Zeleny <jzeleny@redhat.com> - 0.2.91-9
- Bumped the release number to 9 for smooth upgrade

* Fri May 25 2012 Jan Zeleny <jzeleny@redhat.com> - 0.2.91-1
- Rebase to 0.3.0beta1, changelog available at
  https://fedorahosted.org/sssd/wiki/Releases/DingNotes-0.2.91

* Tue Mar 06 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.1.3-8
- Make path_concat return empty string on ENOBUFS

* Tue Mar 06 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.1.3-7
- Fix off-by-one bug in path_concat()
- Resolves: rhbz#799347 - path_utils:test_path_concat_neg fails on 64-bit big
                          endians

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.1.3-5
- New upstream release 0.1.3
- Fixes a serious issue with libdhash and large initial hash sizes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 15 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.1.2-3
- New upsteam release 0.1.2
- Fixes a serious issue with libdhash where hash_enter() would never update
- existing entries for a key.

* Thu Sep 23 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.1.1-2
- Fix invalid source URL

* Thu Sep 23 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.1.1-1
- Initial release of ding-libs
