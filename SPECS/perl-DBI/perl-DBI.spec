# Got the intial spec from Fedora and modified it
# Filter unwanted dependencies
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(RPC::\\)

# According to documentation, module using Coro is just:
# A PROOF-OF-CONCEPT IMPLEMENTATION FOR EXPERIMENTATION.
# Omit Coro support on bootsrap bacause perl-DBI is pulled in by core
# perl-CPANPLUS.
%bcond_without coro

Summary:        A database access API for perl
Name:           perl-DBI
Version:        1.641
Release:        3%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
# The source tarball must be repackaged to remove the DBI/FAQ.pm, since the
# license is not a FSF free license.
Source0:        https://cpan.metacpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
#Source0:        DBI-%{version}_repackaged.tar.gz
%define sha1 DBI=d14c34fac2dd058905b0b8237a4ca8b86eed6f5d
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  perl >= 5.28.0
Requires:	perl >= 5.28.0

%description
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.

%prep
%setup -q -n DBI-%{version}
for F in lib/DBD/Gofer.pm; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.utf8"
    touch -r "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done
chmod 644 ex/*
chmod 744 dbixs_rev.pl
# Fix shell bangs
for F in dbixs_rev.pl ex/corogofer.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done

rm lib/DBD/Gofer/Transport/corostream.pm
sed -i -e '/^lib\/DBD\/Gofer\/Transport\/corostream.pm$/d' MANIFEST

# Remove RPC::Pl* reverse dependencies due to security concerns,
# CVE-2013-7284, bug #1051110
for F in lib/Bundle/DBI.pm lib/DBD/Proxy.pm lib/DBI/ProxyServer.pm \
        dbiproxy.PL t/80proxy.t; do
    rm "$F"
    sed -i -e '\|^'"$F"'|d' MANIFEST
done
sed -i -e 's/"dbiproxy$ext_pl",//' Makefile.PL
# Remove Win32 specific files to avoid unwanted dependencies
for F in lib/DBI/W32ODBC.pm lib/Win32/DBIODBC.pm; do
    rm "$F"
    sed -i -e '\|^'"$F"'|d' MANIFEST
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} '%{buildroot}'/*

%check
make test

%files
%license LICENSE
%{_bindir}/dbipro*
%{_bindir}/dbilogstrip
%{perl_vendorarch}/*.p*
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/DBI/
%{perl_vendorarch}/auto/DBI/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Sat May 09 00:21:23 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.641-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.641-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.641-1
-   Update to version 1.641
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.636-1
-   Upgraded to 1.636
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.634-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.634-1
-   Upgrade version
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.633-1
-   Initial version.
