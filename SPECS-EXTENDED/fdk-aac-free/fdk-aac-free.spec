Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           fdk-aac-free
Version:        2.0.0
Release:        5%{?dist}
Summary:        Third-Party Modified Version of the Fraunhofer FDK AAC Codec Library for Android

License:        FDK-AAC
URL:            https://cgit.freedesktop.org/~wtay/fdk-aac/log/?h=fedora
Source0:        https://people.freedesktop.org/~wtay/fdk-aac-free-%{version}.tar.gz

BuildRequires:  gcc gcc-c++
BuildRequires:  automake libtool

%description
The Third-Party Modified Version of the Fraunhofer FDK AAC Codec Library
for Android is software that implements part of the MPEG Advanced Audio Coding
("AAC") encoding and decoding scheme for digital audio.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%prep
%autosetup
autoreconf -vif

%build
%configure \
  --disable-silent-rules \
  --disable-static

%make_build


%install
%make_install INSTALL="install -p"
find %{buildroot} -name '*.la' -print -delete

%ldconfig_scriptlets

%files
%doc ChangeLog README.fedora
%license NOTICE
%{_libdir}/*.so.*

%files devel
%doc documentation/*.pdf
%dir %{_includedir}/fdk-aac
%{_includedir}/fdk-aac/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/fdk-aac.pc


%changelog
* Thu Jul 13 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-5
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Wim Taymans <wtaymans@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Wim Taymans <wtaymans@redhat.com> - 0.1.6-1
- Update to 0.1.6
- Fix url

* Tue Sep 25 2018 Wim Taymans <wtaymans@redhat.com> - 0.1.5-5
- Use %%ldconfig_scriptlets
- Remove Group

* Thu Nov 02 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.5-4
- Fix BuildRequires, fix libtool cleanup

* Tue Oct 10 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.5-3
- Build against stripped fdk-aac library

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.1.5-1
- Update to 1.5

* Wed Sep 07 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.5-0.1.gita0bd8aa
- Update to github snapshot
- Spec file clean-up

* Fri Nov 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.1.4-1
- Update to 1.4

* Sun Jan 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-1
- Update to 1.3.0

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-1
- Update to 0.1.2

* Thu Mar 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-1
- Initial spec
