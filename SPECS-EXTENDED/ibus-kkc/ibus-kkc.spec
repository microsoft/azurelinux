Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		ibus-kkc
Version:	1.5.22
Release:	16%{?dist}
Summary:	Japanese Kana Kanji input method for ibus

License:	GPLv2+
URL:		https://github.com/ueno/ibus-kkc
Source0:	https://github.com/ueno/ibus-kkc/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:		ibus-kkc-content-type.patch
Patch1:         ibus-HEAD.patch

BuildRequires:	vala
BuildRequires:	perl(File::Find)
BuildRequires:	intltool
BuildRequires:	libkkc-devel >= 0.3.4
BuildRequires:	ibus-devel
BuildRequires:	gtk3-devel
BuildRequires:	desktop-file-utils
Requires:	ibus

%description
A Japanese Kana Kanji Input Method Engine for ibus.


%prep
%setup -q
rm src/*vala.stamp
# don't touch XKB layout under Fedora
sed -i 's!<layout>jp</layout>!<layout>default</layout>!' src/kkc.xml.in.in
# for ibus 1.5.4 or later
%patch 0 -p1 -b .content-type
%patch 1 -p1 -b .orig


%build
%configure
make %{?_smp_mflags}


%install
%make_install INSTALL="install -p"

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See https://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/kkc.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>kkc.xml</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>Kana Kanji</name>
  <summary>Japanese input method</summary>
  <description>
    <p>
      The Kana Kanji input method is designed for entering Japanese text.
      It uses the Kana Kanji conversion library as backend, whose algorithm is based
      on 3-gram statistical language model generated from Wikipedia data.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">https://bitbucket.org/libkkc/libkkc/</url>
  <compulsory_for_desktop>GNOME</compulsory_for_desktop>
  <project_group>GNOME</project_group>
  <developer_name>The GNOME Project</developer_name>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="donation">https://www.gnome.org/friends/</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

desktop-file-validate %{buildroot}/%{_datadir}/applications/ibus-setup-kkc.desktop

%find_lang %{name}


%post
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :


%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/ibus-kkc
%{_libexecdir}/ibus-*-kkc
%{_datadir}/ibus/component/kkc.xml
%{_datadir}/applications/ibus-setup-kkc.desktop


%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.22-16
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.22-15
- Adding missing BRs on Perl modules.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.22-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 14 2017 Jens Petersen <petersen@redhat.com> - 1.5.22-8
- update to upstream head (f7516ae)
- fixes FTBFS

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.5.22-2
- Register as an AppStream component.

* Fri Dec 19 2014 Daiki Ueno <dueno@redhat.com> - 1.5.22-1
- new upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul  7 2014 Daiki Ueno <dueno@redhat.com> - 1.5.21-1
- new upstream release
- update required libkkc version to 0.3.4, for libgee compatibility

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  1 2014 Daiki Ueno <dueno@redhat.com> - 1.5.20-1
- new upstream release

* Tue Dec 17 2013 Daiki Ueno <dueno@redhat.com> - 1.5.19-1
- new upstream release

* Thu Nov  7 2013 Daiki Ueno <dueno@redhat.com> - 1.5.18-2
- write ibus registry cache in %%post and %%postun (Closes: #1013980)
- add patch to respect content-type of target application (Closes: #1013398)

* Fri Sep 13 2013 Daiki Ueno <dueno@redhat.com> - 1.5.18-1
- new upstream release, with improved dictionary selection UI (Closes: #1007648)

* Tue Sep 10 2013 Daiki Ueno <dueno@redhat.com> - 1.5.17-1
- new upstream release, to avoid redundant LM loading (Closes: #1004722)

* Thu Jul 25 2013 Daiki Ueno <dueno@redhat.com> - 1.5.16-2
- remove buildroot cleanup
- validate .desktop file on %%install

* Thu Jul 11 2013 Daiki Ueno <dueno@redhat.com> - 1.5.16-1
- new upstream release (Closes: #980872)

* Fri Jul  5 2013 Daiki Ueno <dueno@redhat.com> - 1.5.15-1
- new upstream release

* Fri Jun  7 2013 Daiki Ueno <dueno@redhat.com> - 1.5.14-1
- new upstream release

* Wed May 15 2013 Daiki Ueno <dueno@redhat.com> - 1.5.13-1
- new upstream release

* Thu May  9 2013 Daiki Ueno <dueno@redhat.com> - 1.5.12-1
- new upstream release

* Thu May  2 2013 Daiki Ueno <dueno@redhat.com> - 1.5.11-2
- specify IBus version when configure

* Wed May  1 2013 Daiki Ueno <dueno@redhat.com> - 1.5.11-1
- new upstream release

* Tue Mar 19 2013 Daiki Ueno <dueno@redhat.com> - 1.5.10-1
- new upstream release

* Tue Mar 12 2013 Daiki Ueno <dueno@redhat.com> - 1.5.9-1
- new upstream release (Closes: #911495)

* Fri Feb 22 2013 Daiki Ueno <dueno@redhat.com> - 1.5.7-1
- new upstream release
- don't touch XKB layout (#910959)

* Mon Feb 11 2013 Daiki Ueno <dueno@redhat.com> - 1.5.6-1
- new upstream release
- change the license to GPLv2+

* Tue Feb  5 2013 Daiki Ueno <dueno@redhat.com> - 1.5.5-1
- new upstream release
- re-add README to %%doc

* Mon Feb  4 2013 Daiki Ueno <dueno@redhat.com> - 1.5.4-1
- new upstream release
- change the license to GPLv3+
- remove empty README file from %%doc

* Thu Jan 31 2013 Daiki Ueno <dueno@redhat.com> - 1.5.3-1
- new upstream release

* Thu Jan 24 2013 Daiki Ueno <dueno@redhat.com> - 1.5.0-1
- initial packaging

