# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		pari-seadata
Version:	20090618
Release: 30%{?dist}
Summary:	PARI/GP Computer Algebra System modular polynomials
License:	GPL-2.0-or-later
URL:		https://pari.math.u-bordeaux.fr/packages.html
Source0:	https://pari.math.u-bordeaux.fr/pub/pari/packages/seadata.tgz
Source1:	https://pari.math.u-bordeaux.fr/pub/pari/packages/seadata.tgz.asc
Source2:	https://pari.math.u-bordeaux.fr/pub/pari/packages/seadata-big.tar
Source3:	https://pari.math.u-bordeaux.fr/pub/pari/packages/seadata-big.tar.asc
# Public key 0xb5444815, owned by Bill Allombert <allomber@math.u-bordeaux.fr>
Source4:	gpgkey-4940AE28C5F8E8A35E4D8D287833ECF1B5444815.gpg
# Public key 0x4522e387, Bill Allombert <Bill.Allombert@math.u-bordeaux.fr>
Source5:	gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg
BuildArch:	noarch

BuildRequires:	gnupg2
BuildRequires:	parallel

%description
This package contains the optional PARI package seadata, which provides the
modular polynomials for prime level up to 500 needed by the GP functions
ellap and ellsea.  This is suitable for finite fields of cardinality q up
to 750 bits.

These polynomials were extracted from the ECHIDNA databases available at
<http://echidna.maths.usyd.edu.au/kohel/dbs/> and computed by David R. Kohel
at the University of Sydney.

%package	big
Summary:	PARI/GP Computer Algebra System big modular polynomials
Requires:	%{name} = %{version}-%{release}

%description	big
This package contains extra modular polynomials of prime level between
500 and 800.  This is suitable for finite fields of cardinality q up to
1100 bits.

%prep
# Verify the source files
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE4}
%{gpgverify} --data=%{SOURCE2} --signature=%{SOURCE3} --keyring=%{SOURCE5}

%autosetup -c -a 2
mv data/seadata/README* .

%build
# Pari can read compressed data files, so save space
# First, decompress the compressed files so we can recompress with --best
gunzip data/seadata/*.gz
parallel %{?_smp_mflags} --no-notice gzip --best ::: data/seadata/sea*

%install
mkdir -p %{buildroot}%{_datadir}/pari/
cp -a data/seadata %{buildroot}%{_datadir}/pari/
%{_fixperms} %{buildroot}%{_datadir}/pari/

%files
%doc README
%dir %{_datadir}/pari/
%dir %{_datadir}/pari/seadata/
%{_datadir}/pari/seadata/sea0*
%{_datadir}/pari/seadata/sea2*
%{_datadir}/pari/seadata/sea3*
%{_datadir}/pari/seadata/sea4*

%files		big
%doc README.big
%{_datadir}/pari/seadata/sea5*
%{_datadir}/pari/seadata/sea6*
%{_datadir}/pari/seadata/sea7*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Jerry James <loganjerry@gmail.com> - 20090618-22
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Jerry James <loganjerry@gmail.com> - 20090618-15
- Add -big subpackage
- Verify PGP signatures on the source files
- Compress the data files

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20090618-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090618-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090618-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090618-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090618-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090618-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  1 2012 Paul Howarth <paul@city-fan.org> - 20090618-3
- Drop conflict with old versions of pari, which cannot use this package but
  aren't broken by it either

* Wed May 23 2012 Paul Howarth <paul@city-fan.org> - 20090618-2
- Add dist tag
- Use %%{_fixperms} to ensure packaged files have sane permissions
- At least version 2.4.3 of pari is required to use this data, so conflict
  with older versions; can't use a versioned require here as it would lead to
  circular build dependencies with pari itself

* Fri May 18 2012 Paul Howarth <paul@city-fan.org> - 20090618-1
- Initial RPM package
