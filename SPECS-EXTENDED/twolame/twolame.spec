Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		twolame
Version:	0.3.13
Release:	16%{?dist}
Summary:	Optimized MPEG Audio Layer 2 encoding library based on tooLAME
# build-scripts/install-sh is MIT/X11, build-scripts/{libtool.m4, ltmain.sh} are GPLv2+
License:	LGPLv2+
URL:		https://www.twolame.org/
Source:		https://downloads.sourceforge.net/twolame/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:	libsndfile-devel
#BuildRequires:	libtool

%description
TwoLAME is an optimized MPEG Audio Layer 2 encoding library based on tooLAME,
which in turn is based heavily on
- the ISO dist10 code
- improvement to algorithms as part of the LAME project (www.sulaco.org/mp3)

This package contains the command line frontend.

%package libs
Summary:	TwoLAME is an optimized MPEG Audio Layer 2 encoding library based on tooLAME
%description libs
TwoLAME is an optimized MPEG Audio Layer 2 encoding library based on tooLAME,
which in turn is based heavily on
- the ISO dist10 code
- improvement to algorithms as part of the LAME project (www.sulaco.org/mp3)

This package contains the shared library.

%package devel
Summary:	Development tools for TwoLAME applications
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the header files and documentation
needed to develop applications with TwoLAME.

%prep
%autosetup
# convert manpage to UTF8
pushd doc
iconv -f iso8859-1 -t utf8 %{name}.1 > %{name}.1.utf && mv %{name}.1.utf %{name}.1
# fix HTML docs line endings
for file in html/*.html ; do
	tr -d '\r' <$file >$file.unix && mv $file.unix $file
done
popd

%build
#autoreconf -f -i
%configure --disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install
rm %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}

%ldconfig_scriptlets libs

%files
%doc AUTHORS ChangeLog README TODO
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/api.txt doc/html doc/psycho.txt doc/vbr.txt
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.13-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.13-10
- Switch to %%ldconfig_scriptlets

* Tue Jan 16 2018 Zamir SUN <sztsian@gmail.com> - 0.3.13-9
- Build for Fedora

* Fri Jan 12 2018 Zamir SUN <sztsian@gmail.com> - 0.3.13-8
- Prepare for push into Fedora repo

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 18 2016 Sérgio Basto <sergio@serjux.com> - 0.3.13-5
- Clean spec, Vascom patches series, rfbz #4202, add license tag

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.3.13-3
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.3.13-1
- Update to 0.3.13

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.3.12-4
- rebuild for new F11 features

* Mon Aug 04 2008 kwizart < kwizart at gmail.com > - 0.3.12-3
- Remove rpath with the "patch libtool" method instead of autoreconf

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.3.12-2
- rebuild

* Sun Jan 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.3.12-1
- updated to 0.3.12
- updated source URL
- split off libs to avoid multilib conflicts
- move docs processing to prep to avoid problems with shortcut builds
- update license tag

* Thu May 03 2007 Dominik Mierzejewski <rpm@greysector.net> 0.3.10-1
- updated to 0.3.10
- removed redundant BRs

* Wed Nov 01 2006 Dominik Mierzejewski <rpm@greysector.net> 0.3.8-1
- updated to 0.3.8
- rebuild autofiles to get rid of rpath
- disable static library build
- fix manpage encoding
- fix HTML docs line endings

* Sun Mar 12 2006 Dominik Mierzejewski <rpm@greysector.net> 0.3.6-1
- updated to 0.3.6

* Tue Jan 24 2006 Dominik Mierzejewski <rpm@greysector.net> 0.3.5-1
- updated to 0.3.5
- simplified package layout
- FE/livna compliance

* Sun Aug 21 2005 Dominik Mierzejewski <rpm@greysector.net>
- initial package
