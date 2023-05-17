%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)
# Filter dependencies on private modules. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)

Summary:        Practical Extraction and Report Language
Name:           perl
Version:        5.30.3
Release:        3%{?dist}
License:        GPL+ or Artistic
URL:            https://www.perl.org/
Group:          Development/Languages
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.cpan.org/src/5.0/%{name}-%{version}.tar.gz
Patch0:         CVE-2023-31484.patch
Provides:       perl >= 0:5.003000
Provides:       perl(getopts.pl)
Provides:       perl(s)
Provides:       /bin/perl
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  gdbm-devel
Requires:       zlib
Requires:       gdbm
Requires:       glibc
Requires:       libgcc


%description
The Perl package contains the Practical Extraction and
Report Language.
%prep
%setup -q
pushd cpan/CPAN
%patch0 -p1
popd
sed -i 's/-fstack-protector/&-all/' Configure

%build
export BUILD_ZLIB=False
export BUILD_BZIP2=0
CFLAGS="%{_optflags}"

sh Configure -des \
    -Dprefix=%{_prefix} \
    -Dvendorprefix=%{_prefix} \
    -Dman1dir=%{_mandir}/man1 \
    -Dman3dir=%{_mandir}/man3 \
    -Dman3ext=3pm \
    -Dpager=%{_bindir}"/less -isR" \
    -Duseshrplib \
    -Dusethreads \
        -DPERL_RANDOM_DEVICE="/dev/erandom"

make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
unset BUILD_ZLIB BUILD_BZIP2
%check
sed -i '/02zlib.t/d' MANIFEST
sed -i '/cz-03zlib-v1.t/d' MANIFEST
sed -i '/cz-06gzsetp.t/d' MANIFEST
sed -i '/porting\/podcheck.t/d' MANIFEST
make test TEST_SKIP_VERSION_CHECK=1
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%license Copying
%{_bindir}/*
%dir %{_libdir}/perl5
%dir %{_libdir}/perl5/%{version}
%{_libdir}/perl5/%{version}/*
%{_mandir}/*/*

%changelog

* Wed May 17 2023 Ahmed Badawi <ahmedbadawi@microsoft.com> 5.30.3-3
- Added patch for a CVE-2023-31484

* Mon Apr 24 2023 Sam Meluch <sammeluch@microsoft.com> 5.30.3-2
- Add -Dman3ext to Configure script in order to avoid manual page name conflicts on installs

*   Tue Jun 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 5.30.3-1
-   Updating to newer version to fix CVE-2020-10878 and CVE-2020-12723.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 5.28.1-4
-   Added %%license line automatically
*   Fri May 8 2020 Nicolas Guibourge <nicolasg@microsoft.com> 5.28.1-3
-   Undo caretx.c patch
*   Wed Apr 29 2020 Nicolas Guibourge <nicolasg@microsoft.com> 5.28.1-2
-   Patch caretx.c so perl works from chroot inside Doccker container
*   Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.com> 5.28.1-1
-   Upgrade to 5.28.1.
-   Fix CVE-2018-18311.
-   Fix CVE-2018-18312.
-   Update license, Source0 and URL.
-   License verified
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5.28.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Oct 24 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.28.0-2
-   Add provides perl(s)
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 5.28.0-1
-   Upgrade to version 5.28.0
*   Tue Oct 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.24.1-4
-   CVE-2017-12837 and CVE-2017-12883 patch from
-   https://perl5.git.perl.org/perl.git/commitdiff/2be4edede4ae226e2eebd4eff28cedd2041f300f#patch1
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 5.24.1-3
-   Rebuild perl after adding gdbm-devel package.
*   Thu Jun 15 2017 Chang Lee <changlee@vmware.com> 5.24.1-2
-   Updated %check
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 5.24.1-1
-   Update to 5.24.1.
*   Thu Oct 20 2016 Xiaolin Li <xiaolinl@vmware.com> 5.22.1-5
-   CVE-2016-1238 patch from http://perl5.git.perl.org/perl.git/commit/cee96d52c39b1e7b36e1c62d38bcd8d86e9a41ab.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 5.22.1-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.22.1-3
-   GA - Bump release of all rpms
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-2
-   Enable threads
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-1
-   Update version
*   Thu Jun 4 2015 Touseef Liaqat <tliaqat@vmware.com> 5.18.2-2
-   Provide /bin/perl.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.18.2-1
-   Initial build. First version
