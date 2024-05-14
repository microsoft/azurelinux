Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global apiversion 0.1

Name: libfreehand
Version: 0.1.2
Release: 7%{?dist}
Summary: A library for import of Macromedia/Adobe FreeHand documents

License: MPLv2.0
URL: https://wiki.documentfoundation.org/DLP/Libraries/libfreehand
Source: https://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: gperf
BuildRequires: help2man
BuildRequires: perl-interpreter
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(zlib)

Patch0: 0001-Add-missing-semicolon-to-fix-build-with-icu-65.1.patch

%description
libfreehand is library providing ability to interpret and import
Macromedia/Adobe FreeHand documents into various applications.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform Macromedia/Adobe FreeHand documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Macromedia/Adobe FreeHand documents into other formats.
Currently supported: SVG, raw, text.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in fh2raw fh2svg fh2text; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 fh2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS
%license COPYING
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING
%doc docs/doxygen/html

%files tools
%{_bindir}/fh2raw
%{_bindir}/fh2svg
%{_bindir}/fh2text
%{_mandir}/man1/fh2raw.1*
%{_mandir}/man1/fh2svg.1*
%{_mandir}/man1/fh2text.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.2-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 16 2017 David Tardon <dtardon@redhat.com> - 0.1.2-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 David Tardon <dtardon@redhat.com> - 0.1.1-1
- new upstream release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.1.0-4
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.1.0-1
- new upstream release

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.0.0-4
- generate man pages

* Mon Nov 04 2013 David Tardon <dtardon@redhat.com> - 0.0.0-3
- fix memory leak

* Thu Oct 31 2013 David Tardon <dtardon@redhat.com> 0.0.0-2
- add gperf to BuildRequires

* Thu Oct 31 2013 David Tardon <dtardon@redhat.com> 0.0.0-1
- initial import
