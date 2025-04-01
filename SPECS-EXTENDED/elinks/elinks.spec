%if 0%{?rhel} >= 10 || 0%{?rescue}
%bcond_with gpm
%else
%bcond_without gpm
%endif

Name:      elinks
Summary:   A text-mode Web browser
Version:   0.17.0
Release:   5%{?dist}
License:   GPL-2.0-only
URL:       https://github.com/rkd77/elinks
Source:    https://github.com/rkd77/elinks/releases/download/v%{version}/elinks-%{version}.tar.xz
Source2:   elinks.conf

BuildRequires: automake
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: gcc-c++
BuildRequires: gettext
%if %{with gpm}
BuildRequires: gpm-devel
%endif
BuildRequires: krb5-devel
BuildRequires: libidn2-devel
BuildRequires: lua-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel
Requires(preun): %{_sbindir}/alternatives
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(postun): coreutils
Requires(postun): %{_sbindir}/alternatives
Provides: webclient
Provides: links = 1:0.97-1
Provides: text-www-browser

# Prevent crash when HOME is unset (bug #90663).
Patch0: 0000-elinks-0.15.0-ssl-noegd.patch

# UTF-8 by default
Patch1: 0001-elinks-0.15.1-utf_8_io-default.patch

# Make getaddrinfo call use AI_ADDRCONFIG.
Patch3: elinks-0.11.0-getaddrinfo.patch

# Don't put so much information in the user-agent header string (bug #97273).
Patch4: 0004-elinks-0.15.0-sysname.patch

# Fix xterm terminal: "Linux" driver seems better than "VT100" (#128105)
Patch5: 0005-elinks-0.15.0-xterm.patch

# let list_is_singleton() return false for an empty list (#1075415)
Patch6: elinks-0.12pre6-list_is_singleton.patch

%description
Elinks is a text-based Web browser. Elinks does not display any images,
but it does support frames, tables and most other HTML tags. Elinks'
advantage over graphical browsers is its speed--Elinks starts and exits
quickly and swiftly displays Web pages.

%prep
%autosetup -p1

# remove bogus serial numbers
sed -e 's/^# *serial [AM0-9]*$//' -i config/m4/*.m4

# recreate autotools files
aclocal -I config/m4
autoconf
autoheader

%build
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -D_GNU_SOURCE"

# make the code build with lua-5.4.x
CFLAGS="$CFLAGS -DLUA_COMPAT_5_3"

%configure \
    --enable-256-colors             \
    --enable-bittorrent             \
    --with-gssapi                   \
    --with-lua                      \
    --with-openssl                  \
    %{?with_gpm:--with-gpm}         \
    %{!?with_gpm:--without-gpm}     \
    --without-gnutls                \
    --without-spidermonkey          \
    --without-x

%make_build -j1

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/elinks.conf
touch $RPM_BUILD_ROOT%{_bindir}/links
true | gzip -c > $RPM_BUILD_ROOT%{_mandir}/man1/links.1.gz
%find_lang elinks

%postun
if [ "$1" -ge "1" ]; then
	links=`readlink %{_sysconfdir}/alternatives/links`
	if [ "$links" == "%{_bindir}/elinks" ]; then
		%{_sbindir}/alternatives --set links %{_bindir}/elinks
	fi
fi
exit 0

%post
#Set up alternatives files for links
%{_sbindir}/alternatives --install %{_bindir}/links links %{_bindir}/elinks 90 \
  --slave %{_mandir}/man1/links.1.gz links-man %{_mandir}/man1/elinks.1.gz
links=`readlink %{_sysconfdir}/alternatives/links`
if [ "$links" == "%{_bindir}/elinks" ]; then
	%{_sbindir}/alternatives --set links %{_bindir}/elinks
fi


%preun
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove links %{_bindir}/elinks
fi
exit 0

%files -f elinks.lang
%license COPYING
%doc README.md
%ghost %verify(not md5 size mtime) %{_bindir}/links
%{_bindir}/elinks
%ghost %verify(not md5 size mtime) %{_mandir}/man1/links.1.gz
%config(noreplace) %{_sysconfdir}/elinks.conf
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 01 2024 Lukáš Zaoral <lzaoral@redhat.com> - 0.17.0-4
- disable gpm integration for RHEL 10 (RHEL-23701)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Lukáš Zaoral <lzaoral@redhat.com> - 0.17.0-1
- rebase to latest upstream release (rhbz#2255830)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.16.1.1-1
- new upstream release (rhbz#2192272)

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.16.0-5
- migrate to SPDX license format

* Fri Mar 24 2023 Arjun Shankar <arjun@redhat.com> - 0.16.0-4
- Port configure script to C99

* Mon Feb 20 2023 Jan Rybar <jrybar@redhat.com> - 0.16.0-3
- parallel builds cause FTBFS
- Resolves: bz#2171476

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Kamil Dudka <kdudka@redhat.com> - 0.16.0-1
- make the IDN2 support work again (#1098789)
- new upstream release

* Mon Aug 01 2022 Kamil Dudka <kdudka@redhat.com> - 0.15.1-1
- new upstream release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 11 2022 Kamil Dudka <kdudka@redhat.com> - 0.15.0-1
- new upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.68.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.12-0.67.pre6
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.66.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.65.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Kamil Dudka <kdudka@redhat.com> - 0.12-0.64.pre6
- make the code build with lua-5.4.x

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.63.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.62.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.61.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.60.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Kamil Dudka <kdudka@redhat.com> - 0.12-0.59.pre6
- fix programming mistakes detected by static analysis

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.58.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 0.12-0.57.pre6
- add explicit BR for the gcc compiler

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.56.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 11 2017 Kamil Dudka <kdudka@redhat.com> - 0.12-0.55.pre6
- drop support for JS engine that is no longer maintained
- always build verbosely, drop outdated doc files

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.54.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.53.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 02 2017 Kamil Dudka <kdudka@redhat.com> - 0.12-0.52.pre6
- rebuild against js-devel with ABI-incompatible <js/jsval.h> (#1446545)

* Fri Feb 17 2017 Kamil Dudka <kdudka@redhat.com> - 0.12-0.51.pre6
- fix compatibility with OpenSSL 1.1 (#1423519)
- make configure.ac recognize recent versions of GCC
- apply patches automatically to ease maintenance

* Fri Feb 17 2017 Tomáš Mráz <tmraz@redhat.com> - 0.12-0.50.pre6
- drop disablement of TLS1.0 on second attempt to connect,
  it would not work correctly anyway and the code does not build
  with OpenSSL-1.1.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.49.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-0.48.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 07 2015 Kamil Dudka <kdudka@redhat.com> - 0.12-0.47.pre6
- use the OpenSSL-provided host name check (#881399)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.46.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Kamil Dudka <kdudka@redhat.com> - 0.12-0.45.pre6
- remove an obsolete configuration option from /etc/elinks.conf (#1222555)

* Mon Mar 30 2015 Kamil Dudka <kdudka@redhat.com> - 0.12-0.44.pre6
- use OpenSSL instead of nss_compat_ossl, which is no longer maintained

* Fri Jan 16 2015 Tom Callaway <spot@fedoraproject.org> - 0.12-0.43.pre6
- rebuild for lua 5.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.42.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.41.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Kamil Dudka <kdudka@redhat.com> - 0.12-0.40.pre6
- add support for GNU Libidn2, patch by Robert Scheck (#1098789)

* Wed May 21 2014 Kamil Dudka <kdudka@redhat.com> - 0.12-0.39.pre6
- use later versions of lua since lua50 is not available (#1098392)

* Tue Apr 29 2014 Kamil Dudka <kdudka@redhat.com> - 0.12-0.38.pre6
- let list_is_singleton() return false for an empty list (#1075415)

* Wed Sep 18 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.37.pre6
- verify server certificate hostname with nss_compat_ossl (#881411)

* Tue Sep 03 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.36.pre6
- remove ancient Obsoletes tag against links (#1002132)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.35.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.34.pre6
- update to latest upstream pre-release
- drop unneeded patches
- fix autoconf warnings
- explicitly disable using OpenSSL and GnuTLS

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.33.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.32.pre5
- do not delegate GSSAPI credentials (CVE-2012-4545)

* Mon Oct 08 2012 Kamil Dudka <kdudka@redhat.com> - 0.12-0.31.pre5
- add default "ddg" dumb/smart rewrite prefixes for DuckDuckGo (#856348)

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 0.12-0.30.pre5
- fix specfile issues reported by the fedora-review script

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.29.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Kamil Dudka <kdudka@redhat.com> - 0.12-0.28.pre5
- do not crash if add_heartbeat() returned NULL (#798103)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.27.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 06 2011 Kamil Dudka <kdudka@redhat.com> - 0.12-0.26.pre5
- improve the js-1.8.5 patch (upstream commit 218a225)

* Thu Apr 21 2011 Kamil Dudka <kdudka@redhat.com> - 0.12-0.25.pre5
- port to js-1.8.5 API (upstream commits f31cf6f and 2844f8b)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.24.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 07 2010 Kamil Dudka <kdudka@redhat.com> - 0.12-0.23.pre5
- do not print control characters to build logs
- avoid aclocal warnings

* Thu Jan 07 2010 Kamil Dudka <kdudka@redhat.com> - 0.12-0.22.pre5
- remove patch for configure script to find OpenSSL (we use NSS now)
- remove buildrequires for nss-devel (#550770)

* Sun Dec 27 2009 Kamil Dudka <kdudka@redhat.com> 0.12-0.21.pre5
- add buildrequires for js-devel (#550717) and zlib-devel
- build support for 256 color terminal

* Mon Dec 14 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.20.pre5
- Add buildrequires for gpm-devel to enable gpm support(#547064)

* Fri Aug 14 2009 Orion Poplawski <orion@cora.nwra.com> 0.12-0.19.pre5
- Add Requires(post/postun): coreutils for readlink

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.18.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.17.pre5
- new upstream bugfix prerelease

* Mon Jun 01 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.16.pre4
- new upstream bugfix prerelease
- defuzz patches

* Wed Apr 29 2009 Kamil Dudka <kdudka@redhat.com> 0.12-0.15.pre3
- try to load default NSS root certificates if the configuration option
  connection.ssl.trusted_ca_file is set to an empty string (#497788)

* Tue Apr 28 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.14.pre3
- enable certificate verification by default via configuration
  file(#495532)

* Tue Apr 28 2009 Kamil Dudka <kdudka@redhat.com> 0.12-0.13.pre3
- use appropriate BuildRequires for nss_compat_ossl (#495532)
- support for trusted CA certificates loading from file in PEM format

* Fri Apr 03 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.12.pre3
- use word Elinks instead of Links in package description

* Mon Mar 30 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.11.pre3
- new upstream bugfix prerelease
- defuzz patches

* Wed Mar 25 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.10.pre2
- use better obsoletes/provides for links, use alternatives for
  links manpage and binary(#470703)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.9.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 0.12-0.8.pre2
- rebuild with new openssl

* Wed Jan 14 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.7.pre2
- versioned obsoletes and provides for links

* Wed Oct  1 2008 Kamil Dudka <kdudka@redhat.com> 0.12-0.6.pre2
- port elinks to use NSS library for cryptography (#346861)

* Mon Sep 29 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.5.pre2
- new upstream bugfix prerelease
- Removed already applied patches for tabreload and bittorrent

* Mon Sep  1 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.4.pre1
- upstream fix for bittorrent protocol
- upstream fix for out of screen bittorrent dialog texts

* Tue Jul 15 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.3.pre1
- get rid off fuzz in patches

* Tue Jul 15 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.2.pre1
- fix a crash when opening tab during page reload

* Tue Jul  1 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.1.pre1
- unstable elinks-0.12 pre1, solves several long-term issues 
  unsolvable (or very hard to solve) in 0.11.4 (like #173411),
  in general is elinks-0.12pre1 considered better than 0.11.4
- dropped patches negotiate-auth, chunkedgzip - included in 0.12pre1,
  modified few others due source code changes

* Sat Jun 21 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-1
- new stable upstream release

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.4.rc1
- new upstream release candidate marked stable

* Thu Feb 21 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.3.rc0
- fixed broken output for gzipped chunked pages(#410801)

* Thu Feb 07 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.2.rc0
- used -D_GNU_SOURCE instead of ugly hack/patch to 
  have NI_MAXPATH defined

* Wed Feb 06 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.1.rc0
- new version marked stable by upstream 0.11.4rc0
- enabled experimental bittorent support(#426702)

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-7
- rebuilt because of new OpenSSL

* Thu Oct 11 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-6
- generalized text-www-browser requirements(#174566)

* Tue Aug 28 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-5
- rebuilt because of expat 2.0

* Wed Aug 22 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-4
- rebuilt for F8
- changed license tag to GPLv2

* Thu Aug  9 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-3
- fix of open macro(new glibc) by Joe Orton

* Fri Jul 27 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-2
- cleanup of duplicates in buildreq, added license file to doc 
- (package review by Tyler Owen(#225725))

* Tue Jun  5 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-1
- update to new upstream version
- removed patch for #210103 , included in upstream release
- updated patch elinks-0.11.1-negotiate.patch to pass build

* Mon Mar 26 2007 Karel Zak <kzak@redhat.com> 0.11.2-1
- update to new upstream version
- cleanup spec file

* Wed Oct 11 2006 Karel Zak <kzak@redhat.com> 0.11.1-5
- fix #210103 - elinks crashes when given bad HTTP_PROXY

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.11.1-4.1
- rebuild

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 0.11.1-4
- improved negotiate-auth patch (faster now)

* Fri Jun  9 2006 Karel Zak <kzak@redhat.com> 0.11.1-3
- added negotiate-auth (GSSAPI) support -- EXPERIMENTAL!

* Mon May 29 2006 Karel Zak <kzak@redhat.com> 0.11.1-2
- update to new upstream version

* Wed May 17 2006 Karsten Hopp <karsten@redhat.de> 0.11.0-3
- add buildrequires bzip2-devel, expat-devel,libidn-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.11.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.11.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Karel Zak <kzak@redhat.com> 0.11.0-2
- use upstream version of srcdir.patch

* Tue Jan 10 2006 Karel Zak <kzak@redhat.com> 0.11.0-1
- update to new upstream version
- fix 0.11.0 build system (srcdir.patch)
- regenerate patches:
     elinks-0.11.0-getaddrinfo.patch, 
     elinks-0.11.0-ssl-noegd.patch,
     elinks-0.11.0-sysname.patch,
     elinks-0.11.0-union.patch

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.10.6-2.1
- rebuilt

* Wed Nov  9 2005 Karel Zak <kzak@redhat.com> 0.10.6-2
- rebuild (against new openssl)

* Thu Sep 29 2005 Karel Zak <kzak@redhat.com> 0.10.6-1
- update to new upstream version

* Tue May 17 2005 Karel Zak <kzak@redhat.com> 0.10.3-3
- fix #157300 - Strange behavior on ppc64 (patch by Miloslav Trmac)

* Tue May 10 2005 Miloslav Trmac <mitr@redhat.com> - 0.10.3-2
- Fix checking for numeric command prefix (#152953, patch by Jonas Fonseca)
- Fix invalid C causing assertion errors on ppc and ia64 (#156647)

* Mon Mar 21 2005 Karel Zak <kzak@redhat.com> 0.10.3-1
- sync with upstream; stable 0.10.3

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 0.10.2-2
- rebuilt

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 0.10.2-1
- sync with upstream; stable 0.10.2

* Fri Jan 28 2005 Karel Zak <kzak@redhat.com> 0.10.1-1
- sync with upstream; stable 0.10.1

* Thu Oct 14 2004 Karel Zak <kzak@redhat.com> 0.9.2-2
- the "Linux" driver seems better than "VT100" for xterm (#128105)

* Wed Oct  6 2004 Karel Zak <kzak@redhat.com> 0.9.2-1
- upload new upstream tarball with stable 0.9.2 release

* Mon Sep 20 2004 Jindrich Novy <jnovy@redhat.com> 0.9.2-0.rc7.4
- 0.9.2rc7.
- changed summary in spec to get rid of #41732, #61499

* Mon Sep 13 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc4.3
- Avoid symbol clash (bug #131170).

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc4.2
- 0.9.2rc4.

* Mon Jul 12 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc2.2
- Fix elinks -dump -stdin (bug #127624).

* Thu Jul  1 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc2.1
- 0.9.2rc2.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-3
- Build with LFS support (bug #125064).

* Fri May 28 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-2
- Use UTF-8 by default (bug #76445).

* Thu Mar 11 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-1
- 0.9.1.
- Use %%find_lang.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 0.4.3-1
- 0.4.3.
- Updated pkgconfig patch.

* Mon Aug 11 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-7.1
- Rebuilt.

* Mon Aug 11 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-7
- Don't require XFree86-libs (bug #102072).

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.4.2-6.2
- rebuild

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-6.1
- Rebuilt.

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-6
- Make getaddrinfo call use AI_ADDRCONFIG.
- Don't put so much information in the user-agent header string (bug #97273).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  2 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-4.1
- Rebuild again.

* Mon Jun  2 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-4
- Rebuild.

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-3
- Prevent crash when HOME is unset (bug #90663).

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de> 0.4.2-2
- use relative symlinks to elinks

* Wed Feb  5 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-1
- 0.4.2 (bug #83273).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.3.2-5
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix URL (bug #81987).

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-4
- rebuild

* Mon Dec 23 2002 Tim Waugh <twaugh@redhat.com> 0.3.2-3
- Fix bug #62368.

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl's pkg-config data, if available

* Wed Nov 20 2002 Tim Powers <timp@redhat.com> 0.3.2-2
- rebuild on all arches

* Tue Aug 20 2002 Jakub Jelinek <jakub@redhat.com> 0.3.2-1
- update to 0.3.2 to fix the DNS Ctrl-C segfaults
- update URLs, the project moved
- include man page

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Tim Powers <timp@redhat.com>
- rebuilt against new openssl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Preston Brown <pbrown@redhat.com> 0.96-4
- cookie fix

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-3
- Save some more space in rescue mode

* Wed Jul 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-2
- Add the links manual from links.sourceforge.net (RFE #49228)

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-1
- update to 0.96

* Fri Jun 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually run make in build phase

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Jan  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.95

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94 final

* Sun Dec 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- pre9

* Mon Dec 11 2000 Preston Brown <pbrown@redhat.com>
- Upgraded to pre8.

* Tue Dec  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre7
- Minor fixes to the specfile (s/Copyright:/License:/)
- merge rescue stuff

* Fri Nov 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre5

* Wed Nov 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre4

* Tue Oct 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre1

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.92 (needed - prior versions won't display XHTML properly)

* Thu Jul 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment to work around bugs

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.84

* Sun Jun 11 2000 Preston Brown <pbrown@redhat.com>
- provides virtual package webclient.

* Thu Jan  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial RPM
