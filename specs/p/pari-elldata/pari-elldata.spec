# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		pari-elldata
Version:	20210301
Release: 12%{?dist}
Summary:	PARI/GP Computer Algebra System elliptic curves
License:	GPL-2.0-or-later
URL:		https://pari.math.u-bordeaux.fr/packages.html
Source0:	https://pari.math.u-bordeaux.fr/pub/pari/packages/elldata.tgz
Source1:	https://pari.math.u-bordeaux.fr/pub/pari/packages/elldata.tgz.asc
# Public key 0x4522e387, Bill Allombert <Bill.Allombert@math.u-bordeaux.fr>
Source2:	gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg

BuildArch:	noarch

BuildRequires:	gnupg2
BuildRequires:	parallel

%description
This package contains the optional PARI package elldata, which provides the
Elliptic Curve Database of J. E. Cremona Elliptic, which can be queried by
ellsearch and ellidentify.

%prep
# Verify the source file
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}

%autosetup -c

# We'll ship the README as %%doc
mv data/elldata/README .

%build
# Pari can read compressed data files, so save space
parallel %{?_smp_mflags} --no-notice gzip --best ::: data/elldata/ell*

%install
mkdir -p %{buildroot}%{_datadir}/pari/
cp -a data/elldata %{buildroot}%{_datadir}/pari/
%{_fixperms} -c %{buildroot}%{_datadir}/pari/

%files
%doc README
%{_datadir}/pari/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Jerry James <loganjerry@gmail.com> - 20210301-4
- Verify the source archive before unpacking it

* Mon Dec 12 2022 Jerry James <loganjerry@gmail.com> - 20210301-4
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210301-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul  1 2021 Jerry James <loganjerry@gmail.com> - 20210301-1
- Version 20210301

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20190912-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190912-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190912-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 13 2019 Jerry James <loganjerry@gmail.com> - 20190912-1
- Update to upstream release from September 12th 2019

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20161017-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Jerry James <loganjerry@gmail.com> - 20161017-5
- Verify PGP signature on the source file
- Compress the data files

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20161017-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20161017-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20161017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Paul Howarth <paul@city-fan.org> - 20161017-1
- Update to upstream release from October 17th 2016

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160215-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 21 2016 Paul Howarth <paul@city-fan.org> - 20160215-1
- Update to upstream release from February 15th 2016

* Fri Feb  5 2016 Paul Howarth <paul@city-fan.org> - 20150519-1
- Update to upstream release from May 19th 2015

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20140113-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140113-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Paul Howarth <paul@city-fan.org> - 20140113-1
- Update to upstream release from January 13th 2014

* Fri Oct  4 2013 Paul Howarth <paul@city-fan.org> - 20121022-1
- Update to upstream release from October 12th 2012

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120415-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120415-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120415-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Paul Howarth <paul@city-fan.org> - 20120415-5
- Drop conflict with old versions of pari, which cannot use this package but
  aren't broken by it either

* Wed May 23 2012 Paul Howarth <paul@city-fan.org> - 20120415-4
- Conflict with old pari packages rather than pari-gp packages

* Tue May 22 2012 Paul Howarth <paul@city-fan.org> - 20120415-3
- Add dist tag
- Use %%{_fixperms} to ensure packaged files have sane permissions
- At least version 2.2.11 of pari-gp is required to use this data, so
  conflict with older versions; can't use a versioned require here as it
  would lead to circular build dependencies with pari itself

* Mon May 21 2012 Paul Howarth <paul@city-fan.org> - 20120415-2
- Ship the README as %%doc (#822896)

* Fri May 18 2012 Paul Howarth <paul@city-fan.org> - 20120415-1
- Initial RPM package
