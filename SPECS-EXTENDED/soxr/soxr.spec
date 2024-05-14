Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           soxr
Version:        0.1.3
Release:        6%{?dist}
Summary:        The SoX Resampler library

License:        LGPLv2+
URL:            https://sourceforge.net/p/soxr/wiki/Home/ 
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.xz

BuildRequires:  cmake gcc

%description
The SoX Resampler library `libsoxr' performs one-dimensional sample-rate
conversion -- it may be used, for example, to resample PCM-encoded audio.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}-Source


%build
rm -rf build && mkdir build && pushd build
export LDFLAGS="-Wl,--as-needed"
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       ../
%make_build


%install
pushd build
%make_install

# Remove docs and use the rpmbuild macro instead
rm -rf %{buildroot}%{_docdir}/*


%check
pushd build
make test

%ldconfig_scriptlets


%files
%doc NEWS README
%license LICENCE
%{_libdir}/*.so.*

%files devel
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/soxr-lsr.pc
%{_libdir}/pkgconfig/soxr.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.3-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Richard Shaw <hobbes1069@gmail.com> - 0.1.3-1
- Update to 0.1.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep  8 2015 Richard Shaw <hobbes1069@gmail.com> - 0.1.2-1
- Update to latest upstream release.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Richard Shaw <hobbes1069@gmail.com> - 0.1.1-1
- Initial packaging.
