Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           meanwhile
Version:        1.1.0
Release:        31%{?dist}
Summary:        Lotus Sametime Community Client library
License:        GPLv2+
URL:            https://%{name}.sourceforge.net

# The source for this package was pulled from upstream's vcs.  Use the following commands to generate the tarball:

# cvs -d:pserver:anonymous@meanwhile.cvs.sourceforge.net:/cvsroot/meanwhile co -d meanwhile-1.1.0 -r meanwhile_v1_1_0 meanwhile
# tar -cvzf meanwhile-1.1.0.tar.gz meanwhile-1.1.0

Source:         %{_distro_sources_url}/%{name}-%{version}.tar.gz
Patch0:         %{name}-crash.patch
Patch1:         %{name}-fix-glib-headers.patch
Patch2:         %{name}-file-transfer.patch
Patch3:         %{name}-status-timestamp-workaround.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1037196
Patch4:         %{name}-format-security-fix.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  glib2-devel
BuildRequires:  doxygen
BuildRequires:  libtool

%description
The heart of the %{name} Project is the %{name} library, providing the basic
Lotus Sametime session functionality along with the core services; Presence
Awareness, Instant Messaging, Multi-user Conferencing, Preferences Storage,
Identity Resolution, and File Transfer.

%package devel
Summary:        Header files, libraries and development documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name}, you
will need to install %{name}-devel.

%package doc
Summary:        Documentation for the %{name} library
License:        GFDL
BuildArch:      noarch
Provides:       meanwhile-docs = %{version}-%{release}
Obsoletes:      meanwhile-docs < 1.1.10-11

%description doc
Documentation for the %{name} library.

%prep
%setup -q
%patch 0 -p0 -b .crash
%patch 1 -p1 -b .fix-glib-headers
%patch 2 -p1 -b .file-transfer
%patch 3 -p1 -b .status-timestamp-workaround
%patch 4 -p1 -b .format-security-fix

%build
export CFLAGS="%{optflags} -fno-tree-vrp"
autoreconf -vif
%configure --enable-doxygen
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

# Prepare documents for inclusion through %%doc in the %%files section
mkdir docs
mv %{buildroot}%{_datadir}/doc/%{name}-doc-%{version}/{html,samples} docs
rm -rf %{buildroot}%{_datadir}/doc/%{name}-doc-%{version}/

%ldconfig_scriptlets libs

%files
%license COPYING LICENSE
%doc AUTHORS ChangeLog README TODO
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc docs/*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-31
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-30
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-29
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Tony Breeds <tony@bakeyournoodle.com> - 1.1.0-24
- Updated to remove %defattr as per packaging standards

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Simone Caronni <negativo17@gmail.com> - 1.1.0-17
- Fix for failed login (#1171300). Thanks Gustavo Luiz Darte.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-14
- Drop empty NEWS from docs, escape macros in %%changelog.

* Tue Dec 03 2013 Tony Breeds <tony@bakeyournoodle.com> - 1.1.0-13
- Closes #1037196

* Thu Aug 08 2013 Simone Caronni <negativo17@gmail.com> - 1.1.0-12
- Fix documentation generation.
- SPEC file cleanup.
- Documentation is now noarch.
- Run autotools on source; remove aarch64 patch.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Simone Caronni <negativo17@gmail.com> - 1.1.0-10
- Added aarch64 patch.

* Tue Mar 26 2013 Simone Caronni <negativo17@gmail.com> - 1.1.0-9
- Added patches for file transfer and status time workaround:
  https://www.lilotux.net/~mikael/pub/meanwhile/
- Spec file formatting.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Josh Boyer <jwboyer@gmail.com> 1.1.0-5
- Fix glib.h build issues (rhbz 750023)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 29 2010 Josh Boyer <jwboyer@gmail.com> - 1.1.0-4
- Remove lib%%{name}.a (#556084)

* Tue Jan 12 2010 Dan Winship <danw@redhat.com> - 1.1.0-3
- Fix Source tag to indicate a CVS snapshot build.
- Resolves: #554446

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.0-1
- Update to %%{name}_v1_1_0 branch from upstream CVS. Fixes bug 490088
