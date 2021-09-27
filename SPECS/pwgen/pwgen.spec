Name:           pwgen
Version:        2.08
Release:        8%{?dist}
Summary:        Automatic password generation
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        GPL+
URL:            https://sf.net/projects/pwgen
Source0:        https://download.sf.net/pwgen/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc

%description
pwgen generates random, meaningless but pronounceable passwords. These
passwords contain either only lowercase letters, or upper and lower case, or
upper case, lower case and numeric digits. Upper case letters and numeric
digits are placed in a way that eases memorizing the password.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%doc debian/changelog
%license debian/copyright
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Sep 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.08-8
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Vasiliy N. Glazov <vascom2@gmail.com> 2.08-1
- Update to 2.08
- Clean spec

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 5 2014 Orion Poplawski <orion@cora.nwra.com> - 2.07-1
- Update to 2.07 (bug 1159526) fixes:
  CVE-2013-4440 (bug 1020222, 1020223)
  CVE-2013-4442 (bug 1020259, 1020261)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.06-3
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 James Bowes <jbowes@redhat.com> - 2.06-2
- Mark license as GPL+

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 2.06-1
- Update to 2.06

* Mon Sep 11 2006 James Bowes <jbowes@redhat.com> - 2.05-4
- EVR bumped for mass rebuild.

* Sat Mar 25 2006 James Bowes <jbowes@redhat.com> - 2.05-3
- Add dist tag to release.
- Don't strip binary, since rpmbuild will do it.

* Fri Mar 24 2006 James Bowes <jbowes@redhat.com> - 2.05-2
- Use url for Source0 in spec file.
- Use glob for man page extension.

* Sun Mar 12 2006 James Bowes <jbowes@redhat.com> - 2.05-1
- Initial Fedora packaging.
