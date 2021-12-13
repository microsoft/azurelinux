Vendor:         Microsoft Corporation
Distribution:   Mariner
%global apiversion 0.0

Name: libstaroffice
Version: 0.0.7
Release: 2%{?dist}
Summary: A library for import of binary StarOffice documents

License: MPLv2.0 or LGPLv2+
URL: https://github.com/fosnola/libstaroffice/wiki
Source: https://github.com/fosnola/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: help2man
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)
BuildRequires: pkgconfig(zlib)

%description
%{name} is a library for import of binary StarOffice documents.

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
Summary: Tools to transform StarOffice documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform StarOffice documents into other formats. Currently
supported: CSV, HTML, plain text, SVG, raw.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-silent-rules --enable-zip
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
%make_install
rm -f %{buildroot}/%{_libdir}/*.la
# rhbz#1001245 we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in sd2raw sd2svg sd2text sdc2csv sdw2html; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 sd2*.1 sd?2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%files
%doc CREDITS NEWS README
%license COPYING.LGPL COPYING.MPL
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING.LGPL COPYING.MPL
%doc docs/doxygen/html

%files tools
%{_bindir}/sdw2html
%{_bindir}/sd2raw
%{_bindir}/sd2svg
%{_bindir}/sd2text
%{_bindir}/sdc2csv
%{_mandir}/man1/sdw2html.1*
%{_mandir}/man1/sd2raw.1*
%{_mandir}/man1/sd2svg.1*
%{_mandir}/man1/sd2text.1*
%{_mandir}/man1/sdc2csv.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.7-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Apr 05 2020 David Tardon <dtardon@redhat.com> - 0.0.7-1
- new upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 David Tardon <dtardon@redhat.com> - 0.0.6-1
- new upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 David Tardon <dtardon@redhat.com> - 0.0.5-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 16 2017 David Tardon <dtardon@redhat.com> - 0.0.4-1
- new upstream release

* Tue Jun 06 2017 David Tardon <dtardon@redhat.com> - 0.0.3-3
- Resolves: rhbz#1458800 CVE-2017-9432 Stack-buffer overflow in the
  StarWriterStruct::DatabaseName::read

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed Feb 22 2017 David Tardon <dtardon@redhat.com> - 0.0.3-1
- new upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 11 2016 David Tardon <dtardon@redhat.com> - 0.0.2-1
- new upstream release

* Thu Feb 11 2016 David Tardon <dtardon@redhat.com> - 0.0.1-1
- initial import
