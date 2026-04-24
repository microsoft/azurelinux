# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          libmnl
Version:       1.0.5
Release: 9%{?dist}
Summary:       Minimalistic Netlink user-space library

License:       LGPL-2.1-or-later
URL:           https://netfilter.org/projects/libmnl/
Source0:       https://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2
Source1:       https://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2.sig
Source2:       https://netfilter.org/files/coreteam-gpg-key-0xD55D978A8A1420E4.txt

BuildRequires: gcc
BuildRequires: gnupg2
BuildRequires: make

%description
libmnl is a minimalistic user-space library oriented to Netlink developers.
There are a lot of common tasks in parsing, validating, constructing of both
the Netlink header and TLVs that are repetitive and easy to get wrong.
This library aims to provide simple helpers that allows you to re-use code and
to avoid re-inventing the wheel.


%package       devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%package       static
Summary:       Static development files for %{name}
Requires:      %{name}-devel%{?_isa} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description   static
The %{name}-static package contains static libraries for developing
applications that use %{name}.


%prep
%setup -q
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'


%build
%configure --enable-static
%make_build CFLAGS="%{optflags}"


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete
find examples '(' -name 'Makefile.am' -o -name 'Makefile.in' ')' -delete
find examples -type d -name '.deps' -prune -exec rm -rf {} ';'
mv examples examples-%{_arch}


%ldconfig_scriptlets


%files
%license COPYING
%doc README
%{_libdir}/%{name}.so.0*

%files devel
%doc examples-%{_arch}
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%files static
%{_libdir}/%{name}.a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 19 2022 Robert Scheck <robert@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5 (#2072018)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.4-1
- Add gcc BuildReq, cleanup spec

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.4-6
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 15 2016 Hushan Jia <hushan.jia@gmail.com> 1.0.4-1
- Update to 1.0.4.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.0.3-8
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 12 2012 Hushan Jia <hushan.jia@gmail.com> - 1.0.3-4
- use %%doc for each arch to avoid multilib conflict (rhbz 831413)

* Sat Aug 04 2012 Philip Prindeville <philipp@fedoraproject.org> - 1.0.3-3
- Add .a to devel package (rhbz 845793)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Hushan Jia <hushan.jia@gmail.com> 1.0.3-1
- Update to 1.0.3.

* Sat Feb 04 2012 Hushan Jia <hushan.jia@gmail.com> 1.0.2-1
- Update to 1.0.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-4
- fix require of devel package
- add example source files to docs

* Wed Aug 24 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-3
- remove unnecessary buildroot and defattr tags
- remove unnecessary build requires

* Sat Aug 20 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-2
- use upstream released source tarball

* Sat Aug 20 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-1
- initial packaging

