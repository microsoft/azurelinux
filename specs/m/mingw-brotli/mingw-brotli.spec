# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name: mingw-brotli
Version: 1.0.7
Release: 15%{?dist}
Summary: MinGW port of Lossless compression algorithm

License: MIT
URL: https://github.com/google/brotli
Source0: %{url}/archive/v%{version}/brotli-%{version}.tar.gz

BuildArch: noarch

BuildRequires: make
BuildRequires: cmake

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc

%description
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.

%package -n mingw32-brotli
Summary: %{summary}

%description -n mingw32-brotli
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.

%package -n mingw64-brotli
Summary: %{summary}

%description -n mingw64-brotli
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.

%{?mingw_debug_package}

%prep
%autosetup -n brotli-%{version}
# fix permissions for -debuginfo
# rpmlint will complain if I create an extra %%files section for
# -debuginfo for this so we'll put it here instead
chmod 644 c/enc/*.[ch]
chmod 644 c/include/brotli/*.h
chmod 644 c/tools/brotli.c

%build
%mingw_cmake
%mingw_make %{?_smp_mflags}

%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

# Remove static libraries but DON'T remove *.dll.a files.
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*-static.a
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*-static.a

# Libtool files don't need to be bundled
find $RPM_BUILD_ROOT -name "*.la" -delete

# Manpages don't need to be bundled
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/man
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/man

rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/gtk-doc
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/gtk-doc

%files -n mingw32-brotli
%{mingw32_bindir}/brotli.exe
%{mingw32_bindir}/libbrotlicommon.dll
%{mingw32_bindir}/libbrotlidec.dll
%{mingw32_bindir}/libbrotlienc.dll
%{mingw32_includedir}/brotli
%{mingw32_libdir}/libbrotlicommon.dll.a
%{mingw32_libdir}/libbrotlidec.dll.a
%{mingw32_libdir}/libbrotlienc.dll.a
%{mingw32_libdir}/pkgconfig/libbrotlicommon.pc
%{mingw32_libdir}/pkgconfig/libbrotlidec.pc
%{mingw32_libdir}/pkgconfig/libbrotlienc.pc
%license LICENSE

%files -n mingw64-brotli
%{mingw64_bindir}/brotli.exe
%{mingw64_bindir}/libbrotlicommon.dll
%{mingw64_bindir}/libbrotlidec.dll
%{mingw64_bindir}/libbrotlienc.dll
%{mingw64_includedir}/brotli
%{mingw64_libdir}/libbrotlicommon.dll.a
%{mingw64_libdir}/libbrotlidec.dll.a
%{mingw64_libdir}/libbrotlienc.dll.a
%{mingw64_libdir}/pkgconfig/libbrotlicommon.pc
%{mingw64_libdir}/pkgconfig/libbrotlidec.pc
%{mingw64_libdir}/pkgconfig/libbrotlienc.pc
%license LICENSE

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.0.7-7
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 15 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.0.7-1
- Initial package
