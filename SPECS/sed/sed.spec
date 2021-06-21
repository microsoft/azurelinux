Summary:	Stream editor
Name:		sed
Version:	4.5
Release:        3%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/sed
Group:		Applications/Editors
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://ftp.gnu.org/gnu/sed/%{name}-%{version}.tar.xz
%define sha1 sed=6635c344956ef928cc33aca798ad20c6c1ea25f7
Conflicts:      toybox

%description
The Sed package contains a stream editor.

%package lang
Summary: Additional language files for sed
Group: System Environment/Programming
Requires: sed >= 4.5
%description lang
These are the additional language files of sed.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--htmldir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
sed -i 's|print_ver_ sed|Exit $fail|g' testsuite/panic-tests.sh
sed -i 's|compare exp-out out|#compare exp-out out|g' testsuite/subst-mb-incomplete.sh
make check

%files
%defattr(-,root,root)
%license COPYING
/bin/*
%{_mandir}/man1/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Sat May 09 00:21:19 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.5-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
* Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 4.5-1
- Updating to version 4.5
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4-3
- Added conflicts toybox
* Tue Aug 01 2017 Chang Lee <changlee@vmware.com> 4.4-2
- Skip panic-tests and subst-mb-incomplete from %check
* Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.4-1
- Update to version 4.4
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.2.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.2-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.2-1
- Initial build. First version
