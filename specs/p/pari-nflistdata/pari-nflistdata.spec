# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pari-nflistdata
Version:        20220729
Release: 9%{?dist}
Summary:        PARI/GP Computer Algebra System nflist extensions
License:        GPL-2.0-or-later
URL:            https://pari.math.u-bordeaux.fr/packages.html
Source0:        https://pari.math.u-bordeaux.fr/pub/pari/packages/nflistdata.tgz
Source1:        https://pari.math.u-bordeaux.fr/pub/pari/packages/nflistdata.tgz.asc
# Public key 0x4522e387, Bill Allombert <Bill.Allombert@math.u-bordeaux.fr>
Source2:        gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg

BuildArch:      noarch

BuildRequires:	gnupg2

%description
This package is needed by nflist to list fields of small discriminant
(currently needed by the single Galois group A5) or to list most regular
extensions of Q(T) in degree larger than 7.

%prep
# Verify the source file
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}

%autosetup -n data

# We'll ship the README as %%doc
mv nflistdata/README .

%build
# Nothing to do

%install
mkdir -p %{buildroot}%{_datadir}/pari
cp -a nflistdata %{buildroot}%{_datadir}/pari

%files
%doc README
%{_datadir}/pari/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220729-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Jerry James <loganjerry@gmail.com> - 20220729-1
- Version 20220729
- Check PGP signature on the source tarball

* Mon Dec 12 2022 Jerry James <loganjerry@gmail.com> - 20220326-2
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220326-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 28 2022 Jerry James <loganjerry@gmail.com> - 20220326-1
- Version 20220326

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210527-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 11 2021 Jerry James <loganjerry@gmail.com> - 20210527-1
- Initial RPM
