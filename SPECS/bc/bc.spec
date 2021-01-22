Summary:        precision numeric processing language
Name:           bc
Version:        1.07.1
Release:        4%{?dist}
License:        GPLv2+
URL:            https://www.gnu.org/software/bc/
Group:          System Environment/base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/bc/%{name}-%{version}.tar.gz

BuildRequires:  ed

%description
The Bc package contains an arbitrary precision numeric processing language.

%prep
%setup -q

%build
%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_mandir}
rm -rf %{buildroot}%{_infodir}

%check
pushd Test
export OTHERBC=%{buildroot}%{_bindir}/bc
./timetest
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Jan 22 2021 Andrew Phelps <anphel@microsoft.com> 1.07.1-4
- Fix check test. Remove sha1. Change URL to GNU bc homepage.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.07.1-3
- Added %%license line automatically
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.07.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Mon Oct 1 2018 Sujay G <gsujay@vmware.com> 1.07.1-1
- Bump bc version to 1.07.1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.06.95-3
- GA - Bump release of all rpms
* Tue Aug 4 2015 Kumar Kaushik <kaushikk@vmware.com> 1.06.95-2
- Adding the post uninstall section.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.06.95-1
- initial version
