Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: sound-theme-freedesktop
Version: 0.8
Release: 16%{?dist}
Summary: freedesktop.org sound theme
Source0: https://people.freedesktop.org/~mccann/dist/sound-theme-freedesktop-%{version}.tar.bz2
# For details on the licenses used, see CREDITS
License:  CC-BY-SA and CC-BY and GPLv2+
Url: https://www.freedesktop.org/wiki/Specifications/sound-theme-spec
BuildArch: noarch
BuildRequires:  gcc
BuildRequires:  perl(File::Find)
BuildRequires: gettext
BuildRequires: intltool >= 0.40
Requires(post): coreutils
Requires(postun): coreutils

%description
The default freedesktop.org sound theme following the XDG theming
specification.  (https://0pointer.de/public/sound-theme-spec.html).

%prep
%setup -q

%build
%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/sounds/freedesktop %{_datadir}/sounds

%postun
touch --no-create %{_datadir}/sounds/freedesktop %{_datadir}/sounds

%files
%license CREDITS COPYING
%doc README
%dir %{_datadir}/sounds/freedesktop
%dir %{_datadir}/sounds/freedesktop/stereo
%{_datadir}/sounds/freedesktop/index.theme
%{_datadir}/sounds/freedesktop/stereo/*.oga

%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8-16
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8-15
- Adding missing BRs on Perl modules.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8-9
- Replace outdated Requires

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Update to 0.8
- Drop obsolete Obsoletes

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 12 2009 Matthias Clasen <mclasen@redhat.com> - 0.7-2
- Obsolete gnome-audio

* Mon Sep 28 2009 Jon McCann <jmccann@redhat.com> 0.7-1
- Update to 0.7

* Thu Sep 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.6.99-1
- Snapshot from Lennart's git tree

* Fri Aug 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.6-1
- New upstream

* Thu Aug 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.5-1
- New upstream

* Sun Aug 23 2009 Jon McCann <jmccann@redhat.com> 0.4-1
- New release adds screen capture sound

* Tue Jul 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.3-2
- Forgot tarball

* Tue Jul 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.3-1
- Update to 0.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Jon McCann <jmccann@redhat.com> 0.2-2
- Rebuild with BuildRequires intltool

* Wed Oct 22 2008 Jon McCann <jmccann@redhat.com> 0.2-1
- Update to 0.2

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-4
- Fix changelog

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-3
- Touch root dirs, not just theme dirs

* Mon Aug 11 2008 Jeremy Katz <katzj@redhat.com> - 0.1-2
- require touch for scriptlets to not give errors

* Sun Jun 15 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-1
- Initial package
