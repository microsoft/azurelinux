Summary:        Program for modifying or creating files
Name:           patch
Version:        2.7.6
Release:        8%{?dist}
License:        GPLv3+
URL:            https://www.gnu.org/software/patch/
Source0:        https://ftp.gnu.org/gnu/patch/%{name}-%{version}.tar.gz
Patch0:         CVE-2018-6951.patch
Patch1:         CVE-2018-1000156.patch
Patch2:         CVE-2018-6952.patch
# https://git.savannah.gnu.org/cgit/patch.git/patch/?id=3fcd042d26d70856e826a42b5f93dc4854d80bf0 
Patch3:         CVE-2018-20969.patch
# This vulnerability is fixed with patch3.
Patch4:         CVE-2019-13638.nopatch
Patch5:         CVE-2019-13636.patch
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Conflicts:      toybox

%description
Program for modifying or creating files by applying a patch
file typically created by the diff program.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
sed -i "s/ulimit -n 32/ulimit -n 1024/g" tests/deep-directories
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.7.6-8
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

*   Tue Jun 02 2020 Nick Samson <nisamson@microsoft.com> - 2.7.6-7
-   Fixed CVE-2019-13636
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7.6-6
-   Added %%license line automatically
*   Mon Apr 20 2020 Emre Girgin <mrgirgin@microsoft.com> 2.7.6-5
-   Fixed CVE-2018-20969.
-   Fixed CVE-2019-13638.
-   Update URL and Source0.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7.6-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Nov 19 2018 Siju Maliakkal <smaliakkal@vmware.com> 2.7.6-3
-   Add patches for CVE-2018-6951,CVE-2018-1000156,CVE-2018-6952
*   Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 2.7.6-2
-   Add conflicts toybox.
*   Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.7.6-1
-   Upgrade to 2.7.6.
*   Fri Apr 28 2017 Divya Thaluru <dthaluru@vmware.com> 2.7.5-4
-   Fixed ulimit in test script.
*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 2.7.5-3
-   Modified %%check.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.5-2
-   GA - Bump release of all rpms.
*   Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 2.7.5-1
-   Updating to 2.7.5 version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.7.1-1
-   Initial build First version.
