# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name: mingw-libunistring
Version: 0.9.10
Release: 18%{?dist}
Summary: MinGW port of GNU Unicode string library
License: GPL-2.0-or-later OR LGPL-3.0-or-later
Url: http://www.gnu.org/software/libunistring/
Source0: http://ftp.gnu.org/gnu/libunistring/libunistring-%{version}.tar.xz

BuildArch: noarch

BuildRequires: make
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package -n mingw32-libunistring
Summary: %{summary}

%description -n mingw32-libunistring
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package -n mingw64-libunistring
Summary: %{summary}

%description -n mingw64-libunistring
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%{?mingw_debug_package}

%prep
%setup -q -n libunistring-%{version}

%build
%mingw_configure \
    --disable-static \
    --disable-rpath

%mingw_make %{?_smp_mflags}

%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{mingw32_infodir}/dir
rm -f $RPM_BUILD_ROOT%{mingw64_infodir}/dir

rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*.la

# Move staged docs so not picked up by %%doc in main package
mv $RPM_BUILD_ROOT%{mingw32_datadir}/doc/libunistring __doc
mv $RPM_BUILD_ROOT%{mingw64_datadir}/doc/libunistring __doc

%files -n mingw32-libunistring
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README HACKING DEPENDENCIES THANKS ChangeLog
%doc __doc/*
%{mingw32_bindir}/libunistring-2.dll
%{mingw32_includedir}/*.h
%{mingw32_includedir}/unistring
%{mingw32_infodir}/libunistring.info*
%{mingw32_libdir}/libunistring.dll.a

%files -n mingw64-libunistring
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README HACKING DEPENDENCIES THANKS ChangeLog
%doc __doc/*
%{mingw64_bindir}/libunistring-2.dll
%{mingw64_includedir}/*.h
%{mingw64_includedir}/unistring
%{mingw64_infodir}/libunistring.info*
%{mingw64_libdir}/libunistring.dll.a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.9.10-15
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.9.10-8
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 0.9.10-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Aug 15 2019 Fabiano Fidêncio <fidencio@redhat.com> - 0.9.10-1
- Initial version
