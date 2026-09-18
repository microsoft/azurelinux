# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global common_description %{expand:
GeoLite2 databases are free IP geolocation databases comparable to, but less
accurate than, MaxMind's GeoIP2 databases.  This product includes GeoLite2 data
created by MaxMind, available from http://www.maxmind.com.}


Name:           geolite2
# Upstream changed their license on 2019-12-30.  This is the last version
# released under CC-BY-SA.
# https://bugzilla.redhat.com/show_bug.cgi?id=1786211
Version:        20191217
Release:        15%{?dist}
Summary:        Free IP geolocation databases
# This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License
# This database incorporates GeoNames geographical data, which is made available under the Creative Commons Attribution 3.0 License
License:        CC-BY-SA-4.0 AND CC-BY-3.0
URL:            https://dev.maxmind.com/geoip/geoip2/geolite2/
Source0:        https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN_%{version}.tar.gz
Source1:        https://geolite.maxmind.com/download/geoip/database/GeoLite2-City_%{version}.tar.gz
Source2:        https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country_%{version}.tar.gz
BuildArch:      noarch


%description %{common_description}


%package asn
Summary:        Free IP geolocation ASN database


%description asn %{common_description}


%package city
Summary:        Free IP geolocation city database


%description city %{common_description}


%package country
Summary:        Free IP geolocation country database


%description country %{common_description}


%prep
%setup -q -T -c -a 0 -a 1 -a 2


%install
for db in GeoLite2-{ASN,City,Country}; do
    install -D -p -m 0644 ${db}_%{version}/$db.mmdb %{buildroot}%{_datadir}/GeoIP/$db.mmdb
done


%files asn
%license GeoLite2-ASN_%{version}/COPYRIGHT.txt GeoLite2-ASN_%{version}/LICENSE.txt
%dir %{_datadir}/GeoIP
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLite2-ASN.mmdb


%files city
%license GeoLite2-City_%{version}/COPYRIGHT.txt GeoLite2-City_%{version}/LICENSE.txt
%dir %{_datadir}/GeoIP
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLite2-City.mmdb


%files country
%license GeoLite2-Country_%{version}/COPYRIGHT.txt GeoLite2-Country_%{version}/LICENSE.txt
%dir %{_datadir}/GeoIP
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLite2-Country.mmdb


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar  3 2023 Paul Howarth <paul@city-fan.org> - 20191217-9
- Use SPDX-format license tag

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191217-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Carl George <carl@george.computer> - 20191217-1
- Latest upstream

* Tue Oct 08 2019 Carl George <carl@george.computer> - 20191008-1
- Latest upstream

* Tue Aug 13 2019 Carl George <carl@george.computer> - 20190806-1
- Latest upstream
- Add ASN subpackage

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190618-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Carl George <carl@george.computer> - 20190618-1
- Latest upstream

* Thu Apr 11 2019 Carl George <carl@george.computer> - 20190409-1
- Latest upstream

* Wed Feb 06 2019 Carl George <carl@george.computer> - 20190205-1
- Latest upstream

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181204-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Carl George <carl@george.computer> - 20181204-1
- Latest upstream

* Thu Oct 04 2018 Carl George <carl@george.computer> - 20181002-1
- Latest upstream

* Mon Aug 13 2018 Carl George <carl@george.computer> - 20180807-1
- Latest upstream

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180605-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Carl George <carl@george.computer> - 20180605-1
- Latest upstream

* Tue Apr 24 2018 Carl George <carl@george.computer> - 20180403-1
- Initial package
