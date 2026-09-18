# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libspectre
Version:        0.2.12
Release:        10%{?dist}
Summary:        A library for rendering PostScript(TM) documents

License:        GPL-2.0-or-later
URL:            http://libspectre.freedesktop.org
Source0:        http://libspectre.freedesktop.org/releases/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires:  gcc
%if 0%{?fedora} > 27
BuildRequires: libgs-devel
%else
BuildRequires: ghostscript-devel >= 8.61
%endif

%description
%{name} is a small library for rendering PostScript(TM) documents.
It provides a convenient easy to use API for handling and rendering
PostScript documents.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%configure \
  --disable-silent-rules \
  --disable-static

%make_build


%install
%make_install

rm -fv %{buildroot}%{_libdir}/libspectre.la


%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS NEWS README TODO
%{_libdir}/libspectre.so.1*

%files devel
%{_includedir}/libspectre/
%{_libdir}/libspectre.so
%{_libdir}/pkgconfig/libspectre.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Marek Kasik <mkasik@redhat.com> - 0.2.12-3
- Rebuild for ghostscript-10.0.0
- Related: #2128814

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Marek Kasik <mkasik@redhat.com> - 0.2.12-1
- Update to 0.2.12
- Resolves: #2159146

* Mon Nov 07 2022 Marek Kasik <mkasik@redhat.com> - 0.2.11-1
- Update to 0.2.11
- Resolves: #2139968

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 02 2022 Marek Kasik <mkasik@redhat.com> - 0.2.10-1
- Update to 0.2.10
- Resolves: #2053818

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 03 2021 Marek Kasik <mkasik@redhat.com> - 0.2.9-5
- Set alignment for rendering to default
- Resolves: #1938506

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 07 2020 Marek Kasik <mkasik@redhat.com> - 0.2.9-1
- Update to 0.2.9
- Resolves: #1832567

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.2.8-6
- BR: gcc, use %%ldconfig_scriptlets %%make_build %%make_install

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.2.8-5
- BR: libgs-devel (f28+)
- .spec cleanup/cosmetics (drop deprecated tags, use %%autosetup/%%license, tighten subpkg dep)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Martin Hatina <mhatina@redhat.com> - 0.2.8-1
- Update to 0.2.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 31 2015 Marek Kasik <mkasik@redhat.com> - 0.2.7-7
- Rotate result of rendering in libspectre
- Resolves: #1172317

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 19 2012 Marek Kasik <mkasik@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.6-3
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.2.6-2
- rebuild (ghostscript)
- %%files: track sonames (and friends) closer

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Wed Mar  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.4-1
- Update to 0.2.4
- See http://mail.gnome.org/archives/gnome-announce-list/2010-February/msg00059.html

* Fri Jan  8 2010  Marek Kasik <mkasik@redhat.com> - 0.2.3-4
- Correct release number

* Fri Jan  8 2010  Marek Kasik <mkasik@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec  3 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Sun Aug 10 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Sat Feb  9 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.0-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008  Matthias Clasen <mclasen@redhat.com> - 0.2.0-1
- Initial packaging 
