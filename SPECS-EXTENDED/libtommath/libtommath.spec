Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libtommath
Version:        1.3.1~rc1
Release:        3%{?dist}
Summary:        A portable number theoretic multiple-precision integer library
License:        Public Domain
URL:            http://www.libtom.net/

Source0:        https://github.com/libtom/%{name}/archive/v%{version_no_tilde}.tar.gz#/%{name}-%{version_no_tilde}.tar.gz

BuildRequires:  make
BuildRequires:  libtool

%description
A free open source portable number theoretic multiple-precision integer library
written entirely in C. (phew!). The library is designed to provide a simple to
work with API that provides fairly efficient routines that build out of the box
without configuration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-%{version_no_tilde}
# Fix permissions on installed library
sed -i -e 's/644 $(LIBNAME)/755 $(LIBNAME)/g' makefile.shared
# Fix pkgconfig path
sed -i \
    -e 's|^prefix=.*|prefix=%{_prefix}|g' \
    -e 's|^libdir=.*|libdir=%{_libdir}|g' \
    %{name}.pc.in

%build
%set_build_flags
%make_build V=1 CFLAGS="$CFLAGS -I./" -f makefile.shared

%check
make test
./test

%install
%make_install V=1 CFLAGS="$CFLAGS -I./" PREFIX=%{_prefix} LIBPATH=%{_libdir} -f makefile.shared

find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Nov 14 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 1.3.1~rc1-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1~rc1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 30 2024 Frantisek Sumsal <frantisek@sumsal.cz> - 1.3.1~rc1-1
- Bump to v1.3.1-rc1 (rhbz#2275490)

* Wed Mar 27 2024 Frantisek Sumsal <frantisek@sumsal.cz> - 1.3.0-1
- Bump to v1.3.0

* Wed Mar 20 2024 Frantisek Sumsal <frantisek@sumsal.cz> - 1.3.0~rc1-1
- Bump to v1.3.0-rc1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Frantisek Sumsal <frantisek@sumsal.cz> - 1.2.1-1
- Bump to 1.2.1

* Fri Sep 08 2023 Frantisek Sumsal <frantisek@sumsal.cz> - 1.2.0-14
- Run unit tests

* Sat Sep 02 2023 Frantisek Sumsal <frantisek@sumsal.cz> - 1.2.0-13
- Fix CVE-2023-36328 (#2236877,#2236878)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 13 2021 Frantisek Sumsal <frantisek@sumsal.cz> - 1.2.0-6
- Add a couple of missing BRs (texlive-kpathsea and texlive-metafont)

* Wed Nov 03 2021 Frantisek Sumsal <frantisek@sumsal.cz> - 1.2.0-5
- Drop an obsoleted texlive-updmap-map build dependency (#1999507, #1987664)
- (see: #1965446)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Than Ngo <than@redhat.com> - 1.2.0-3
- Add missing BRs

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 09 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.2.0-1
- Update to 1.2.0.
- Remove poster make tag
- Add BuildRequires texlive-appendix

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Simone Caronni <negativo17@gmail.com> - 1.1.0-1
- Update to 1.1.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-9
- Disable parallel build for docs

* Tue May 14 2019 Scott Talbert <swt@techie.net> - 1.0.1-8
- Add BR texlive-updmap-map to fix FTBFS when building docs (#1675313)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 05 2018 Rafael Santos <rdossant@redhat.com> - 1.0.1-5
- Resolves #1548832 - Fix Fedora build flags injection

* Sun Feb 25 2018 Florian Weimer <fweimer@redhat.com> - 1.0.1-4
- Add BuildRequires: ghostscript-tools-dvipdf

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-2
- Switch to %%ldconfig_scriptlets

* Mon Sep 11 2017 Simone Caronni <negativo17@gmail.com> - 1.0.1-1
- Update to 1.0.1.
- Trim changelog.
- Clean up SPEC file.
- Remove RHEL 6 support.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 25 2017 Simone Caronni <negativo17@gmail.com> - 1.0-7
- Update URL (#1463608, #1463547).

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 1.0-4
- Fix installs with non-standard buildroots (#1299860).

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 1.0-3
- Remove useless latex build requirements.

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 1.0-2
- Use proper source URL.
- Cleanup SPEC file.

* Tue Feb 23 2016 Simone Caronni <negativo17@gmail.com> - 1.0-1
- Fix FTBFS (#1307741).
- Update to 1.0.
- Update URL.
- Use license macro.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
