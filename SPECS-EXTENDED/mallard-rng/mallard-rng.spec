Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:    mallard-rng
Version: 1.1.0
Release: 14%{?dist}
Summary: RELAX NG schemas for all Mallard versions

License: MIT
URL:     https://projectmallard.org/download/
Source0: https://projectmallard.org/download/%{name}-%{version}.tar.bz2

BuildArch:        noarch
BuildRequires:    make
Requires(post):   /usr/bin/xmlcatalog
Requires(post):   xml-common
Requires(postun): /usr/bin/xmlcatalog
Requires(postun): xml-common

%description
RELAX NG schemas for all Mallard versions and extensions that have been marked
final.


%prep
%autosetup


%build
%configure
%make_build


%install
%make_install


%post
xmlcatalog --noout --add 'nextCatalog' 'file://%{_sysconfdir}/xml/mallard/catalog' "" %{_sysconfdir}/xml/catalog &> /dev/null || :


%postun
xmlcatalog --noout --del 'file://%{_sysconfdir}/xml/mallard/catalog' %{_sysconfdir}/xml/catalog &> /dev/null || :


%files
%doc AUTHORS NEWS README
%license COPYING
%{_datadir}/xml/mallard
%{_datadir}/pkgconfig
%{_sysconfdir}/xml/mallard
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xml/mallard/catalog



%changelog
* Thu Jan 16 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.1.0-14
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 David King <amigadave@amigadave.com> - 1.1.0-1
- Update to 1.1.0 (#1671767)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 28 2017 David King <amigadave@amigadave.com> - 1.0.3-1
- Update to 1.0.3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 21 2016 David King <amigadave@amigadave.com> - 1.0.2-1
- Initial Fedora packaging (#1264945)
