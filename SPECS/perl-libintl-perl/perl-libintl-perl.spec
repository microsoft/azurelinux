# Got the intial spec from Fedora and modified it
Summary:	Internationalization library for Perl, compatible with gettext
Name:		perl-libintl-perl
Version:	1.29
Release:        4%{?dist}
License:	LGPLv2+
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/libintl-perl/
Source: 	https://cpan.metacpan.org/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
Requires: 	perl >= 5.28.0
BuildRequires: 	perl >= 5.28.0

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.


%prep
%setup -q -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
			-name '*.bs' -size 0 \) -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%license COPYING
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.29-4
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.29-3
-   Renaming perl-libintl to perl-libintl-perl
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.29-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.29-1
-   Update to version 1.29
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 1.26-1
-   upgrade for 2.0
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.24-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.24-1
-   Upgraded to version 1.24
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.23-1
-   Initial version.
