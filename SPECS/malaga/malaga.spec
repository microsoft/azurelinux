Summary:        A programming language for automatic language analysis
Name:           malaga
Version:        7.12
Release:        32%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://dynalabs.de/mxp/malaga/
Source0:        https://dynalabs.de/mxp/assets/malaga-7.12.tgz
# Fix map_file symbol conflict with samba. Upstream can be considered
# inactive but as libvoikko >= 2.2 doesn't use libmalaga anymore, these kind
# of problems won't probably come up. The only executables in Fedora which
# link to libmalaga currently are the malaga tools.
Patch0:         malaga-rename-map_file.patch
# Malshow needs to be linked with -lm as Fedora's ld doesn't do implicit
# linking anymore
Patch1:         malaga-malshow-lm.patch
Patch2:         malaga-aarch64.patch
# Disable linking with gtk2
Patch3:         disable_gtk2.patch
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  readline-devel
BuildRequires:  texinfo
Requires:       lib%{name} = %{version}-%{release}

%description
A software package for the development and application of
grammars that are used for the analysis of words and sentences of natural
languages. It is a language-independent system that offers a programming
language for the modelling of the language-dependent grammatical
information. This language is also called Malaga.

Malaga is based on the grammatical theory of the "Left Associative Grammar"
(LAG), developed by Roland Hausser, professor for Computational Linguistics at
University of Erlangen, Germany.

%package        devel
Summary:        Development files for %{name}
Requires:       lib%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n	lib%{name}
Summary:        Library files for %{name}

%description -n	lib%{name}
Library files for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Remove "@" marks so that the build process is more verbose
sed -i.debug -e 's|^\([ \t][ \t]*\)@|\1|' Makefile.in
# Remove "-s" so binaries won't be stripped
sed -i.strip -e 's| -s | |' Makefile.in
# Make libtool output more verbose
sed -i.silent -e 's|--silent||' Makefile.in

%build
%configure --with-readline
cp %{_bindir}/install-info %{_sbindir}/
export PATH="%{_prefix}/local/sbin:%{_prefix}/local/bin:/sbin:/bin:%{_prefix}/sbin:%{_prefix}/bin:/root/bin"
# Remove rpath,
# https://fedoraproject.org/wiki/Packaging/Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL_INFO=%{_bindir}/install-info INSTALL="install -p"
rm -f %{buildroot}%{_infodir}/dir
find %{buildroot} -type f -name "*.la" -delete -print
# Remove static archive
find %{buildroot} -name '*.a' -exec rm -f {} ';'
# Change permission of libmalaga.so*
chmod 0755 %{buildroot}%{_libdir}/libmalaga.so*




%files
%{_infodir}/%{name}*
%{_bindir}/mal*
%{_datadir}/%{name}
%{_mandir}/man1/mal*

%files -n lib%{name}
%license GPL.txt
%doc CHANGES.txt README.txt
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}*.so
%{_includedir}/malaga.h

%changelog
* Fri Sep 16 2022 Osama Esmail <osamaesmail@microsoft.com> - 7.12-32
- Moved from SPECS-EXTENDED to SPECS
- License verified
- Updated source URL

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.12-31
- Making binaries paths compatible with CBL-Mariner's paths.

* Thu Feb 11 2021 Henry Li <lihl@microsoft.com> - 7.12-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove gtk2-devel from BuildRequires
- Add texinfo as BuildRequires

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.12-27
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 7.12-20
- Rebuild for readline 7.x

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 14 2013 Ville-Pekka Vainio <vpvainio@iki.fi> - 7.12-14
- Add aarch64 patch from rhbz #926118

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Ville-Pekka Vainio <vpvainio@iki.fi> - 7.12-10
- Rebuilt for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-8
- The libmalaga subpackage had two defattrs, remove the other

* Wed Feb 10 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 7.12-7
- Add patch to link malshow with -lm, hopefully fixes FTBFS caused by
  https://fedoraproject.org/wiki/Features/ChangeInImplicitDSOLinking

* Wed Sep 16 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 7.12-6
- Remove rpath which was set for the malaga binaries in 64 bit architechtures

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-4
- Add patch to change the (un)map_file functions to malaga_(un)map_file,
  there was a symbol conflict with the samba libraries causing a segfault
  if enchant-voikko and evolution-mapi were both installed when using
  Evolution. Bugs rhbz #502546 and sourceforge #2802548, patch by Harri
  Pitkänen.
- Add defattr to the libmalaga subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-2
- Upstream changed the source tarball of the current release, use the current
  upstream sources

* Sun Mar 02 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-1
- New version
- Drop upstreamed linking patch
- Re-add a Makefile.in sed build verbosity trick, which was done in the
  dropped patch but not upstream

* Sat Feb 23 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-3
- Add Makefile.in patch to link the executables against libmalaga

* Sat Feb 16 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-2
- Rebuild for GCC 4.3

* Mon Oct 29 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-1
- Increment release for the first Fedora build

* Sun Oct 28 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.5
- -devel requires only libmalaga, not malaga

* Sun Oct 28 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.4
- Add option --with-readline to configure
- Add BR readline-devel

* Sat Oct 27 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.3
- Don't strip binaries
- Remove static archive
- Make build procedure more verbose
- Make libtool output more verbose
- Remove redundant requires gtk2
- Add INSTALL="install -p" to make install to preserve timestamps
- Change libmalaga.so* to have permissions 0755

* Wed Oct 24 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.2
- Main package requires libmalaga version-release and gtk2 (malshow needs it)
- libmalaga requires in -devel removed, that's implicit
- install-info called in post of main package
- Unneeded postun line removed
- INSTALL.txt is not needed in this package
- All documents are now in libmalaga
- /usr/share/malaga/ now owned by the malaga package
- A shorter Summary so rpmlint won't complain
- Currently writes an empty debuginfo package, "install -s" is called in 
  Makefile, how do I remove it?

* Mon Oct 22 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.1
- Initial package
