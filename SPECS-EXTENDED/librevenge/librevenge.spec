%global apiversion 0.0

Name: librevenge
Version: 0.0.4
Release: 18%{?dist}
Summary: A base library for writing document import filters

# src/lib/RVNGOLEStream.{h,cpp} are BSD
License: (LGPLv2+ or MPLv2.0) and BSD
URL: https://sourceforge.net/p/libwpd/wiki/librevenge/
Source: https://downloads.sourceforge.net/libwpd/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(zlib)

%description
%{name} is a base library for writing document import filters. It has
interfaces for text documents, vector graphics, spreadsheets and
presentations.

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

%if ! 0%{?flatpak}
%package gdb
Summary: gdb pretty printers for %{name}
Requires: gdb
Requires: python3-six
Requires: %{name}%{?_isa} = %{version}-%{release}
Supplements: %{name}-debuginfo%{?_isa} = %{version}-%{release}

%description gdb
The %{name}-devel package contains gdb pretty printers that help with
debugging applications that use %{name}.
%endif

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --disable-static \
    --disable-werror \
%if ! 0%{?flatpak}
    --enable-pretty-printers
%endif

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

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%license COPYING.*
%doc README NEWS
%{_libdir}/%{name}-%{apiversion}.so.*
%{_libdir}/%{name}-generators-%{apiversion}.so.*
%{_libdir}/%{name}-stream-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/%{name}-generators-%{apiversion}.so
%{_libdir}/%{name}-stream-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%{_libdir}/pkgconfig/%{name}-generators-%{apiversion}.pc
%{_libdir}/pkgconfig/%{name}-stream-%{apiversion}.pc

%files doc
%license COPYING.*
%doc docs/doxygen/html

%if ! 0%{?flatpak}
%files gdb
%{_datadir}/gdb/auto-load%{_libdir}/%{name}-%{apiversion}.py*
%{_datadir}/gdb/auto-load%{_libdir}/%{name}-stream-%{apiversion}.py*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/python
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.4-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Sergio Durigan Junior <sergiodj@redhat.com> - 0.0.4-16
- Resolves: rhbz#1786466 Do not use %%{?_isa} for GDB dependency.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Kalev Lember <klember@redhat.com> - 0.0.4-14
- Disable gdb pretty printers when building for flatpak

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.0.4-10
- Rebuilt for Boost 1.66

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 0.0.4-7
- Rebuilt for Boost 1.64

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.0.4-5
- Rebuilt for Boost 1.63

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.0.4-4
- Rebuilt for Boost 1.63

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.0.4-2
- Rebuilt for Boost 1.60

* Tue Jan 12 2016 David Tardon <dtardon@redhat.com> - 0.0.4-1
- new upstream release

* Sat Dec 26 2015 David Tardon <dtardon@redhat.com> - 0.0.3-3
- fix packaging

* Sat Dec 26 2015 David Tardon <dtardon@redhat.com> - 0.0.3-2
- fix gdb pretty printers

* Fri Dec 25 2015 David Tardon <dtardon@redhat.com> - 0.0.3-1
- new upstream release

* Sun Aug 30 2015 Jonathan Wakely <jwakely@redhat.com> - 0.0.2-8
- Rebuilt for Boost 1.59

* Sun Aug 30 2015 David Tardon <dtardon@redhat.com> - 0.0.2-7
- Resolves: rhbz#1258128 fix build with boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.0.2-5
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.0.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.0.2-2
- Rebuild for boost 1.57.0

* Wed Dec 24 2014 David Tardon <dtardon@redhat.com> - 0.0.2-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 David Tardon <dtardon@redhat.com> - 0.0.1-1
- new upstream release

* Tue May 27 2014 David Tardon <dtardon@redhat.com> - 0.0.0-2
- remove extra dirs from filelist

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.0.0-1
- initial import
