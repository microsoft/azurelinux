Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global apiversion 0.0

Name: libqxp
Version: 0.0.2
Release: 7%{?dist}
Summary: Library for import of QuarkXPress documents

License: MPLv2.0
URL: https://wiki.documentfoundation.org/DLP/Libraries/libqxp
Source: https://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: help2man
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)

%description
libqxp is library providing ability to interpret and import QuarkXPress
document formats into various applications. Currently it only supports
QuarkXPress 3.1-4.1.

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
Summary: Tools to transform QuarkXPress documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform QuarkXPress documents into other formats.
Currently supported: SVG, plain text, raw.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static
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
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in qxp2raw qxp2svg qxp2text; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 qxp2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS NEWS README
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
%{_bindir}/qxp2raw
%{_bindir}/qxp2svg
%{_bindir}/qxp2text
%{_mandir}/man1/qxp2raw.1*
%{_mandir}/man1/qxp2svg.1*
%{_mandir}/man1/qxp2text.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.2-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 0.0.2-5
- Rebuild for ICU 65

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 0.0.2-2
- Rebuild for ICU 63

* Sat Dec 29 2018 David Tardon <dtardon@redhat.com> - 0.0.2-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 0.0.1-4
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 0.0.1-3
- Rebuild for ICU 61.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 David Tardon <dtardon@redhat.com> - 0.0.1-1
- new upstream release

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 0.0.0-2
- Rebuild for ICU 60.1

* Sun Aug 27 2017 David Tardon <dtardon@redhat.com> - 0.0.0-1
- initial import

