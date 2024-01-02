# pkgconf acts as pkgconfig for Mariner
%bcond_without pkgconfig_compat
%if %{with pkgconfig_compat}
%global pkgconfig_ver 0.29.1
# For obsoleting pkgconfig
%global pkgconfig_verrel %{pkgconfig_ver}-3
%global pkgconfig_evr %{pkgconfig_verrel}
%endif
# Search path for pc files for pkgconf
%global pkgconf_libdirs %{_libdir}/pkgconfig:%{_datadir}/pkgconfig
Summary:        Package compiler and linker metadata toolkit
Name:           pkgconf
Version:        2.0.2
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://pkgconf.org/
# Mirror at https://releases.pagure.org/pkgconf/pkgconf/
Source0:        https://distfiles.dereferenced.org/%{name}/%{name}-%{version}.tar.xz
# Simple wrapper script to offer platform versions of pkgconfig
Source1:        platform-pkg-config.in
# For regenerating autotools scripts
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
# pkgconf uses libpkgconf internally
Requires:       lib%{name}%{?_isa} = %{version}-%{release}
# This is defined within pkgconf code as a virtual pc (just like in pkgconfig)
Provides:       pkgconfig(pkgconf) = %{version}

%description
pkgconf is a program which helps to configure compiler and linker flags
for development frameworks. It is similar to pkg-config from freedesktop.org
and handles .pc files in a similar manner as pkg-config.

%package -n lib%{name}
Summary:        Backend library for %{name}
License:        ISC

%description -n lib%{name}
This package provides libraries for applications to use the functionality
of %{name}.

%package -n lib%{name}-devel
Summary:        Development files for lib%{name}
License:        ISC
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n lib%{name}-devel
This package provides files necessary for developing applications
to use functionality provided by %{name}.

%if %{with pkgconfig_compat}
%package m4
Summary:        m4 macros for pkgconf
License:        GPLv2+ WITH exceptions
# Ensure that it Conflicts and Obsoletes pkgconfig since it contains content formerly from it
Conflicts:      pkgconfig < %{pkgconfig_evr}
Obsoletes:      pkgconfig < %{pkgconfig_evr}
BuildArch:      noarch

%description m4
This package includes m4 macros used to support PKG_CHECK_MODULES
when using pkgconf with autotools.

%package pkg-config
Summary:        %{name} shim to provide %{_bindir}/pkg-config
License:        ISC
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-m4 = %{version}-%{release}
# Ensure that it Conflicts with pkgconfig and is considered "better"
Conflicts:      pkgconfig < %{pkgconfig_evr}
Obsoletes:      pkgconfig < %{pkgconfig_evr}
Provides:       pkgconfig = %{pkgconfig_evr}
Provides:       pkgconfig%{?_isa} = %{pkgconfig_evr}
# This is in the original pkgconfig package, set to match output from pkgconf
Provides:       pkgconfig(pkg-config) = %{version}
# Generic pkg-config Provides for those who might use alternate package name
Provides:       pkg-config = %{pkgconfig_verrel}
Provides:       pkg-config%{?_isa} = %{pkgconfig_verrel}

%description pkg-config
This package provides the shim links for pkgconf to be automatically
used in place of pkgconfig. This ensures that pkgconf is used as
the system provider of pkg-config.

%endif


%prep
%autosetup -p1

%build
autoreconf -fiv
%configure --disable-static \
           --with-pkg-config-dir=%{pkgconf_libdirs} \
           --with-system-includedir=%{_includedir} \
           --with-system-libdir=%{_libdir}

%make_build V=1

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print

mkdir -p %{buildroot}%{_sysconfdir}/pkgconfig/personality.d
mkdir -p %{buildroot}%{_datadir}/pkgconfig/personality.d

# pkgconf rpm macros
mkdir -p %{buildroot}%{_rpmmacrodir}/

cat > %{buildroot}%{_rpmmacrodir}/macros.pkgconf <<EOM
%%pkgconfig_personalitydir %{_datadir}/pkgconfPig/personality.d
EOM

%if %{with pkgconfig_compat}
install -pm 0755 %{SOURCE1} %{buildroot}%{_bindir}/%{_target_platform}-pkg-config

sed -e "s|@TARGET_PLATFORM@|%{_target_platform}|" \
    -e "s|@PKGCONF_LIBDIRS@|%{pkgconf_libdirs}|" \
    -e "s|@PKGCONF_SYSLIBDIR@|%{_libdir}|" \
    -e "s|@PKGCONF_SYSINCDIR@|%{_includedir}|" \
    -i %{buildroot}%{_bindir}/%{_target_platform}-pkg-config

ln -sf pkgconf %{buildroot}%{_bindir}/pkg-config

# Link pkg-config(1) to pkgconf(1)
echo ".so man1/pkgconf.1" > %{buildroot}%{_mandir}/man1/pkg-config.1

mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_datadir}/pkgconfig
%endif

# If we're not providing pkgconfig override & compat
# we should not provide the pkgconfig m4 macros
%if ! %{with pkgconfig_compat}
rm -rf %{buildroot}%{_datadir}/aclocal
%endif

%ldconfig_scriptlets -n lib%{name}

%files
%license COPYING
%doc README.md AUTHORS NEWS
%{_bindir}/%{name}
%{_bindir}/bomtool
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/pc.5*
%{_mandir}/man5/%{name}-personality.5*
%{_rpmmacrodir}/macros.pkgconf
%dir %{_sysconfdir}/pkgconfig
%dir %{_sysconfdir}/pkgconfig/personality.d
%dir %{_datadir}/pkgconfig/personality.d

%files -n lib%{name}
%license COPYING
%{_libdir}/lib%{name}*.so.*

%files -n lib%{name}-devel
%{_libdir}/lib%{name}*.so
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/lib%{name}.pc

%if %{with pkgconfig_compat}
%files m4
%{_datadir}/aclocal/pkg.m4
%{_mandir}/man7/pkg.m4.7*

%files pkg-config
%{_bindir}/pkg-config
%{_bindir}/%{_target_platform}-pkg-config
%{_mandir}/man1/pkg-config.1*
%dir %{_libdir}/pkgconfig
%dir %{_datadir}/pkgconfig
%endif

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 2.0.2-1
- Upgrade to version 2.0.2

* Wed Feb 01 2023 Daniel McIlvaney <damcilva@microsoft.com> - 1.8.0-3
- Add patch for CVE-2023-24056

* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.0-2
- Removing epoch.

* Tue Dec 07 2021 Chris Co <chrco@microsoft.com> - 1.8.0-1
- Update to 1.8.0

* Thu Oct 08 2020 Joe Schmitt <joschmit@microsoft.com> - 1.7.0-3
- License verified.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.7.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon May 25 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 13:23:30 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3

* Fri Jul 12 09:36:57 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Mon Mar 25 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Sat Feb 09 2019 Neal Gompa <ngompa13@gmail.com> - 1.6.0-1
- Update to 1.6.0
- Add personality.d directories for cross-targets
- Add pkgconf rpm macros for pkgconf directories

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.5.3-2
- Rebuild with fixed binutils

* Sun Jul 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Neal Gompa <ngompa13@gmail.com> - 1.5.1-2
- Add patch to fix system path override issue

* Wed Jun 27 2018 Neal Gompa <ngompa13@gmail.com> - 1.5.1-1
- Upgrade to 1.5.1

* Sat Mar 31 2018 Neal Gompa <ngompa13@gmail.com> - 1.4.2-1
- Update to 1.4.2
- Drop conditionals for old Fedora releases

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.1-2
- Switch to %%ldconfig_scriptlets

* Tue Jan 23 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Sun Jan 07 2018 Neal Gompa <ngompa13@gmail.com> - 1.4.0-2
- Move pc(5) manpage to main pkgconf package

* Fri Jan 05 2018 Neal Gompa <ngompa13@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Fri Jan 05 2018 Neal Gompa <ngompa13@gmail.com> - 1.3.90-2
- Add simple wrapper to support platform-specific pkg-config paths (#1513810)

* Tue Dec 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.90-1
- Update to 1.3.90

* Sun Dec 10 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.12-1
- Update to 1.3.12

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.10-1
- Update to 1.3.10

* Wed Sep 20 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.9-1
- Update to 1.3.9

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.8-1
- Update to 1.3.8

* Sun May 28 2017 Neal Gompa <ngompa13@gmail.com> - 1.3.7-1
- Update to 1.3.7

* Wed May 10 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.6-1
- Update to 1.3.6

* Tue Apr 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.5-1
- Update to 1.3.5

* Thu Mar 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4

* Mon Mar 27 2017 Neal Gompa <ngompa13@gmail.com> - 1.3.3-1
- Update to 1.3.3

* Fri Mar 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Sat Feb 25 2017 Neal Gompa <ngompa13@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Tue Feb 07 2017 Neal Gompa <ngompa13@gmail.com> - 1.2.2-2
- Backport patch from upstream to remove extraneous whitespace (#1419685)

* Fri Feb 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Thu Feb 02 2017 Neal Gompa <ngompa13@gmail.com> - 1.2.1-3
- Fix Obsoletes and Conflicts to prevent self-conflicts

* Thu Feb 02 2017 Neal Gompa <ngompa13@gmail.com> - 1.2.1-2
- Adjust Obsoletes and Conflicts to use inclusive range

* Tue Jan 24 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Sat Jan 21 2017 Neal Gompa <ngompa13@gmail.com> - 1.2.0-1
- Upgrade to 1.2.0
- Enable pkgconf-pkg-config and pkgconf-m4 for F26+

* Sat Jan 14 2017 Neal Gompa <ngompa13@gmail.com> - 1.1.1-3
- Add missing pkgconfig() Provides for virtual .pc files defined in pkgconf

* Fri Jan 13 2017 Neal Gompa <ngompa13@gmail.com> - 1.1.1-2
- Add missing Epoch to pkgconfig Provides/Conflicts for pkgconf-pkg-config
- Add copy of pkgconf.1 as pkg-config.1 in pkgconf-pkg-config

* Sat Jan 07 2017 Neal Gompa <ngompa13@gmail.com> - 1.1.1-1
- Upgrade to 1.1.1
- Add missing directories to pkgconf-pkg-config

* Sun Jan 01 2017 Neal Gompa <ngompa13@gmail.com> - 1.1.0-3
- Fix up spec per package review (#1409332)

* Sat Dec 31 2016 Neal Gompa <ngompa13@gmail.com> - 1.1.0-2
- Rework package to not generate conflict with pkgconfig
- Disable pkgconf-m4 and pkgconf-pkg-config by default

* Sat Dec 31 2016 Neal Gompa <ngompa13@gmail.com> - 1.1.0-1
- Upgrade to 1.1.0
- Enable libpkgconf libraries now that they are ABI+API stable

* Tue Oct 25 2016 Neal Gompa <ngompa13@gmail.com> - 1.0.2-1
- Upgrade to 1.0.2

* Fri Aug 26 2016 Neal Gompa <ngompa13@gmail.com> - 1.0.1-2
- Add subpackage for providing pkg-config shim
- Enable tests

* Thu Aug 25 2016 Neal Gompa <ngompa13@gmail.com> - 1.0.1-1
- Upgrade to 1.0.1

* Wed Aug 24 2016 Neal Gompa <ngompa13@gmail.com> - 1-1
- Initial packaging
