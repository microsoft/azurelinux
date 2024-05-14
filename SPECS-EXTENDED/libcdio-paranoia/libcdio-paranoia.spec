Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: libcdio-paranoia
Version: 10.2+2.0.0
Release: 5%{?dist}
Summary: CD paranoia on top of libcdio
License: GPLv3+
URL: https://www.gnu.org/software/libcdio/
Source0: https://ftp.gnu.org/gnu/libcdio/libcdio-paranoia-%{version}.tar.bz2
Patch0: libcdio-paranoia-manpage.patch
BuildRequires: gcc
BuildRequires: pkgconfig
BuildRequires: gettext-devel
BuildRequires: chrpath
BuildRequires: libcdio-devel

%description
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from the
CDROM directly as data, with no analog step between, and writes the
data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

Split off from libcdio to allow more flexible licensing and to be compatible
with cdparanoia-III-10.2's license. And also, libcdio is just too large.

%package devel
Summary: Header files and libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.


%prep
%setup -q
%patch 0 -p1

# fix pkgconfig files
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_paranoia.pc.in
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_cdda.pc.in

f=doc/ja/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f
iconv -f ISO88591 -t utf-8 -o THANKS.utf8 THANKS && mv THANKS.utf8 THANKS

%build
%configure \
	--disable-dependency-tracking \
	--disable-static \
	--disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/{jp,ja}

# copy include files to an additional directory for backward compatibility
# this is where most software still expects those files
cp -a $RPM_BUILD_ROOT%{_includedir}/cdio/paranoia/*.h $RPM_BUILD_ROOT%{_includedir}/cdio/

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so.*

%check
make %{?_smp_mflags} check

%files
%license COPYING
%doc AUTHORS NEWS README.md THANKS
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*


%files devel
%doc doc/overlapdef.txt
%{_includedir}/cdio/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.2+2.0.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Adrian Reber <adrian@lisas.de> - 10.2+2.0.0-1
- updated to 10.2+2.0.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+0.94+2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+0.94+2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Adrian Reber <adrian@lisas.de> - 10.2+0.94+2-2
- updated to 10.2+0.94+2

* Tue Oct 17 2017 Marek Kasik <mkasik@redhat.com> - 10.2+0.93+1-11
- Enable unit tests
- Backport fix for a NULL pointer dereference
- Resolves: #1502655

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+0.93+1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+0.93+1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+0.93+1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Adrian Reber <adrian@lisas.de> - 10.2+0.93+1-7
- Rebuilt for new libcdio-0.94

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.2+0.93+1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2+0.93+1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Kalev Lember <kalevlember@gmail.com> - 10.2+0.93+1-3
- Obsolete compat-libcdio-paranoia1

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 10.2+0.93+1-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Oct 31 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 10.2+0.93+3-1
- rebase
- license changed

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2+0.90+1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2+0.90+1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90+1-2
- Rebuilt for new libcdio-0.92

* Tue Aug 20 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90+1-1
- updated to 10.2+0.90+1
- removed all patches previously taken from git

* Wed Jul 31 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 10.2+0.90-8
- long name in manual page caused 'whatis' to misbehave

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2+0.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Adrian Reber <adrian@lisas.de> - 10.2+0.90-6
- remove sed changes on non-installed file
- fix -devel subpackage Require

* Sat Dec 22 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-5
- provide include files also in the paranoia directory (like in upstream's git)

* Thu Nov 22 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-4
- fix pkgconfig files to point to right include directory

* Mon Nov 05 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-3
- included upstreamed patches which are changing the license
  headers to be LGPLv2+ for the library parts and GPLv2+ for the
  binaries

* Tue Oct 30 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-2
- added missing files from git: COPYING-GPL and COPYING-LGPL
- added patch from git for missing pkgconfig requires
  and fixed FSF address

* Mon Oct 29 2012 Adrian Reber <adrian@lisas.de> - 10.2+0.90-1
- initial release
