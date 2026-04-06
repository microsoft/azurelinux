# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          opusfile
Version:       0.12
%global soname_version 0
Release:       17%{?dist}
Summary:       A high-level API for decoding and seeking within .opus files
License:       BSD-3-Clause
URL:           https://www.opus-codec.org/
Source0:       https://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz
# Propagate allocation failure from ogg_sync_buffer.
# https://github.com/xiph/opusfile/commit/0a4cd796df5b030cb866f3f4a5e41a4b92caddf5
#
# Fixes CVE-2022-47021.
# A potential bug of NPD
# https://github.com/xiph/opusfile/issues/36
Patch1:        https://github.com/xiph/opusfile/commit/0a4cd796df5b030cb866f3f4a5e41a4b92caddf5.patch#/CVE-2022-47021.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: pkgconfig(ogg)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(opus)

%description
libopusfile provides a high-level API for decoding and seeking 
within .opus files. It includes:
* Support for all files with at least one Opus stream (including
multichannel files or Ogg files where Opus is muxed with something else).
* Full support, including seeking, for chained files.
* A simple stereo downmixing API (allowing chained files to be
decoded with a single output format, even if the channel count changes).
* Support for reading from a file, memory buffer, or over HTTP(S)
(including seeking).
* Support for both random access and streaming data sources.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# The public API headers include ogg/ogg.h.
Requires: pkgconfig(ogg)

%description devel
Files for development with %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static

%make_build

%install
%make_install

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%files
%license COPYING
%doc AUTHORS
%{_libdir}/libopusfile.so.%{soname_version}{,.*}
%{_libdir}/libopusurl.so.%{soname_version}{,.*}

%files devel
%doc %{_docdir}/%{name}
%{_includedir}/opus/opus*
%{_libdir}/pkgconfig/opusfile.pc
%{_libdir}/pkgconfig/opusurl.pc
%{_libdir}/libopusfile.so
%{_libdir}/libopusurl.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Sep 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12-15
- Identify the license as BSD-3-Clause
- Make opusfile-devel depend on libogg-devel

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.12-14
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 01 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12-9
- Add upstream fix for CVE-2022-47021

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.12-5
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 28 2020 David King <amigadave@amigadave.com> - 0.12-1
- Update to 0.12

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 19 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.11
- Update to 0.11

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.10-3
- Add gcc BR, spec cleanups

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 23 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.10-1
- Update to 0.10

* Thu Aug  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.9-1
- Update to 0.9

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-1
- Update to 0.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-1
- Update to 0.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-1
- Update to 0.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.5-1
- Update to 0.5

* Tue Aug 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4-1
- Update to 0.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.2-1
- Update to 0.2

* Sun Nov  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1-1
- Initial package
