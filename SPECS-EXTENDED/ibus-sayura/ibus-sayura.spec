Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:       ibus-sayura
Version:    1.3.2
Release:    20%{?dist}
Summary:    The Sinhala engine for IBus input platform
License:    GPLv2+
URL:        https://pagure.io/ibus-sayura
Source0:    https://releases.pagure.org/ibus-sayura/%{name}-%{version}.tar.gz

# This is a test patch so not submitted to upstream yet
# This patch is created by Mike Fabian
Patch0:     fix-for-wayland-rhbz1724759.patch

BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  ibus-devel
Requires:   ibus
%description
The Sayura engine for IBus platform. It provides Sinhala input method.

%prep
%autosetup -p1

%build
%configure --disable-static
# make -C po update-gmo
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See https://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/sayura.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>sayura.xml</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>Sayura</name>
  <summary>Sihali input method</summary>
  <description>
    <p>
      The Sayura input method is designed for entering Sinhala text.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">https://fedorahosted.org/ibus-sayura/</url>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <languages>
    <lang percentage="100">si</lang>
  </languages>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang %{name}

%post
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README
%{_libexecdir}/ibus-engine-sayura
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/ibus-sayura
%{_datadir}/ibus/component/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.2-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.3.2-17
- Fix Sayura rendering issue (rh#1724759), Thanks to Mike Fabian

* Wed Jul 17 2019 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.3.2-16
- Fix Sayura cache issue on Silverblue (rh#1730242)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 09 2017 Pravin Satpute <psatpute@redhat.com> - 1.3.2-10
- Change in project hosting and source tarball location - fedorahosted to pagure.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 16 2015 Richard Hughes <rhughes@redhat.com> - 1.3.2-7
- Increase AppStream search result weighting when using the 'si' locale.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.3.2-5
- Register as an AppStream component.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Pravin Satpute <psatpute@redhat.com> - 1.3.2-1
- configured with autoconf-2.69

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 1.3.1-6
- spec file clean up

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 07 2012 Pravin Satpute <psatpute@redhat.com> - 1.3.1-4
- rebuild for broken dependancies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Pravin Satpute <psatpute@redhat.com> - 1.3.1-2
- Resolved bug #741176

* Thu Feb 24 2011 Pravin Satpute <psatpute@redhat.com> - 1.3.1-1
- upstream release 1.3.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.20100716-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.0.20100716-3
- adding rank to ibus-sayura

* Mon Nov 08 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.0.20100716-2
- rebuild for broken dependancies

* Fri Jul 16 2010 Pravin Satpute <psatpute@redhat.com> - 1.3.0.20100716-1
- upstream new release

* Tue Jun 15 2010 Pravin Satpute <psatpute@redhat.com> - 1.2.99.20100209-2
- fixed bug 601568

* Tue Feb 09 2010 Pravin Satpute <pravin.d.s@gmail.com> - 1.2.99.20100209-1
- updated patches for code enhancements from phuang for ibus-1.2.99

* Mon Feb 08 2010 Adam Jackson <ajax@redhat.com> 1.2.0.20090703-4
- Rebuild for new libibus.so.2 ABI

* Tue Nov 17 2009 Pravin Satpute <psatpute@redhat.com> - @VERSON@-3
- fixed bug 528405

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090703-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Pravin Satpute <psatpute@redhat.com> - @VERSON@-1
- upstream release 1.2.0

* Mon Jun 29 2009 Pravin Satpute <pravin.d.s@gmail.com> - @VERSON@-4
- fix for bug 507209

* Mon Jun 29 2009 Parag <panemade@gmail.com> - 1.0.0.20090326-3
- Rebuild against newer ibus

* Thu Mar 26 2009 Pravin Satpute <pravin.d.s@gmail.com> - @VERSON@-2
- updated as per fedora spec review

* Fri Mar 20 2009 Pravin Satpute <pravin.d.s@gmail.com> - 1.0.0.20090326-1
- The first version.
