Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gitfullrev 08767aa863cd27d1755ba0aff65b8cc1a0c1446a
%global gitrev %(c=%{gitfullrev}; echo ${c:0:6})
Name:           urlview
Version:        0.9
Release:        29%{?dist}
Summary:        URL extractor/launcher

License:        GPLv2
URL:            https://github.com/sigpipe/urlview
Source0:        https://github.com/sigpipe/urlview/archive/%{gitrev}/urlview-%{gitrev}.tar.gz

BuildRequires:  gcc
BuildRequires:  ncurses-devel

Patch1:         urlview-default.patch

%description
urlview is a screen oriented program for extracting URLs from text
files and displaying a menu from which you may launch a command to
view a specific item.

%prep
%setup -q -n %{name}-%{gitfullrev}
%patch1 -p1 -b .default

%build
%configure
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_mandir}/man{1,5}}
install -p -m644 urlview.conf.suse $RPM_BUILD_ROOT%{_sysconfdir}/urlview.conf
install -p urlview url_handler.sh $RPM_BUILD_ROOT%{_bindir}
install -p -m644 urlview.man $RPM_BUILD_ROOT%{_mandir}/man1/urlview.1
echo '.so man1/urlview.1' > $RPM_BUILD_ROOT%{_mandir}/man5/urlview.conf.5
echo '.so man1/urlview.1' > $RPM_BUILD_ROOT%{_mandir}/man1/url_handler.sh.1

%files
%license COPYING
%doc AUTHORS ChangeLog README sample.urlview
%config(noreplace) %{_sysconfdir}/urlview.conf
%{_bindir}/urlview
%{_bindir}/url_handler.sh
%{_mandir}/man1/urlview.1*
%{_mandir}/man1/url_handler.sh.1*
%{_mandir}/man5/urlview.conf.5*

%changelog
* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9-29
- Removing 'Conflicts' on an older package never present in CBL-Mariner.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9-28
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-27.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-26.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-25.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-24.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-23.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-22.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-21.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-20.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-19.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-18.20131022git08767a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 24 2015 Miroslav Lichvar <mlichvar@redhat.com> 0.9-17.20131022git08767a
- update to 20131022git08767a

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-16.20121210git6cfcad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-15.20121210git6cfcad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-14.20121210git6cfcad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Miroslav Lichvar <mlichvar@redhat.com> 0.9-13.20121210git6cfcad
- add man page link for url_handler.sh
- fix default paths in man page

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-12.20121210git6cfcad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Miroslav Lichvar <mlichvar@redhat.com> 0.9-11.20121210git6cfcad
- update to 20121210git6cfcad
- remove obsolete macros

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Miroslav Lichvar <mlichvar@redhat.com> 0.9-7
- add man page link for urlview.conf (#526162)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-4
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.9-3
- update license tag

* Fri Jun 29 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.9-2
- add conflict with mutt, fix URL (#245951)

* Wed Jun 27 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.9-1
- split from mutt package
