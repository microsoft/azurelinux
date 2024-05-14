Summary:        Free GeoLite IP geolocation country database
Name:           GeoIP-GeoLite-data
# The geolite databases were traditionally updated on the first Tuesday of each month,
# hence we use a versioning scheme of YYYY.MM for the Fedora package.
#
# No further releases of IPv4 GeoLite Legacy databases will be made from April 2018.
Version:        2018.06
Release:        12%{?dist}
# License specified at https://dev.maxmind.com/geoip/legacy/geolite/#License
License:        CC-BY-SA
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://dev.maxmind.com/geoip/legacy/geolite/
Source0:        %{_distro_sources_url}/GeoIP.dat.gz
Source1:        %{_distro_sources_url}/GeoIPv6.dat.gz
Source2:        %{_distro_sources_url}/GeoLiteCity.dat.gz
Source3:        %{_distro_sources_url}/GeoLiteCityv6.dat.gz
Source4:        %{_distro_sources_url}/GeoIPASNum.dat.gz
Source5:        %{_distro_sources_url}/GeoIPASNumv6.dat.gz
# The data was unbundled from GeoIP at 1.6.4-3
Source6:        LICENSE
Conflicts:      GeoIP < 1.6.4-3
Obsoletes:      GeoIP-data < 1.6.4-10
Provides:       GeoIP-data = %{version}
Obsoletes:      geoip-geolite < %{version}
Provides:       geoip-geolite = %{version}
BuildArch:      noarch

%description
The GeoLite databases are free IP geolocation databases. This package contains
a database that maps IPv4 addresses to countries.

This product includes GeoLite data created by MaxMind, available from
https://www.maxmind.com/

%package extra
Summary:        Free GeoLite IP geolocation databases
Requires:       %{name} = %{version}-%{release}

%description extra
The GeoLite databases are free IP geolocation databases. This package contains
databases that map IPv6 addresses to countries, plus IPv4 and IPv6 addresses
to cities and autonomous system numbers.

This product includes GeoLite data created by MaxMind, available from
https://www.maxmind.com/

%prep
%setup -q -T -c

install -p -m 644 %{SOURCE0} GeoLiteCountry.dat.gz;	gunzip GeoLiteCountry.dat
install -p -m 644 %{SOURCE1} GeoIPv6.dat.gz;		gunzip GeoIPv6.dat
install -p -m 644 %{SOURCE2} GeoLiteCity.dat.gz;	gunzip GeoLiteCity.dat
install -p -m 644 %{SOURCE3} GeoLiteCityv6.dat.gz;	gunzip GeoLiteCityv6.dat
install -p -m 644 %{SOURCE4} GeoLiteASNum.dat.gz;	gunzip GeoLiteASNum.dat
install -p -m 644 %{SOURCE5} GeoIPASNumv6.dat.gz;	gunzip GeoIPASNumv6.dat

%build
# This section intentionally left empty

%install
mkdir -p %{buildroot}%{_datadir}/GeoIP/
for db in \
	GeoLiteCountry.dat \
	GeoIPv6.dat \
	GeoLiteCity.dat \
	GeoLiteCityv6.dat \
	GeoLiteASNum.dat \
	GeoIPASNumv6.dat
do
	install -p -m 644 $db %{buildroot}%{_datadir}/GeoIP/
done

# Add compat symlinks for GeoIPASNum.dat and GeoLiteASNumv6.dat
# ([upstream] database names used in the old geoip-geolite package)
ln -sf GeoLiteASNum.dat %{buildroot}%{_datadir}/GeoIP/GeoIPASNum.dat
ln -sf GeoIPASNumv6.dat %{buildroot}%{_datadir}/GeoIP/GeoLiteASNumv6.dat

# Symlinks for City databases to be where upstream expects them
# (geoiplookup -v ...)
ln -sf GeoLiteCity.dat %{buildroot}%{_datadir}/GeoIP/GeoIPCity.dat
ln -sf GeoLiteCityv6.dat %{buildroot}%{_datadir}/GeoIP/GeoIPCityv6.dat

install -m 644 %{SOURCE6} LICENSE

%preun
# If the package is being uninstalled (rather than upgraded), we remove
# the GeoIP.dat symlink, provided that it points to GeoLiteCountry.dat;
# rpm will then be able to remove the %%{_datadir}/GeoIP directory
if [ $1 = 0 ]; then
	if [ -h %{_datadir}/GeoIP/GeoIP.dat ]; then
		geoipdat=`readlink %{_datadir}/GeoIP/GeoIP.dat`
		if [ "$geoipdat" = "GeoLiteCountry.dat" ]; then
			rm -f %{_datadir}/GeoIP/GeoIP.dat
		fi
	fi
fi
exit 0

%posttrans
# Create the default GeoIP.dat as a symlink to GeoLiteCountry.dat
#
# This has to be done in %%posttrans rather than %%post because an old
# package's GeoIP.dat may still be present during %%post in an upgrade
#
# Don't do this if there is any existing GeoIP.dat, as we don't want to
# override what the user has put there
#
# Also, if there's an existing GeoIP.dat.rpmsave, we're probably doing
# an upgrade from an old version of GeoIP that packaged GeoIP.dat as
# %%config(noreplace), so rename GeoIP.dat.rpmsave back to GeoIP.dat
# instead of creating a new symlink
if [ ! -e %{_datadir}/GeoIP/GeoIP.dat ]; then
	if [ -e %{_datadir}/GeoIP/GeoIP.dat.rpmsave ]; then
		mv %{_datadir}/GeoIP/GeoIP.dat.rpmsave \
			%{_datadir}/GeoIP/GeoIP.dat
	else
		ln -sf GeoLiteCountry.dat %{_datadir}/GeoIP/GeoIP.dat
	fi
fi
exit 0

%files
%license LICENSE
%dir %{_datadir}/GeoIP/
# The databases are %%verify(not md5 size mtime) so that they can be updated
# via cron scripts and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCountry.dat

%files extra
# The databases are %%verify(not md5 size mtime) so that they can be updated
# via cron scripts and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCity.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCityv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteASNum.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPASNumv6.dat
# The compat symlinks are just regular files as they should never need to be
# changed
%{_datadir}/GeoIP/GeoIPASNum.dat
%{_datadir}/GeoIP/GeoIPCity.dat
%{_datadir}/GeoIP/GeoIPCityv6.dat
%{_datadir}/GeoIP/GeoLiteASNumv6.dat

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2018.06-12
- Updating naming for 3.0 version of Azure Linux.

* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 2018.06-11
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- license verified

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Paul Howarth <paul@city-fan.org> - 2018.06-1
- IPv6 databases are still seeing updates in June 2018
- IPv4 databases are unchanged from previous release

* Wed Apr  4 2018 Paul Howarth <paul@city-fan.org> - 2018.04-1
- Final update of GeoLite Legacy databases from Maxmind

* Wed Mar 21 2018 Paul Howarth <paul@city-fan.org> - 2018.03-1
- Update to March 2018 databases

* Fri Feb  2 2018 Paul Howarth <paul@city-fan.org> - 2018.02-1
- Update to February 2018 databases

* Mon Jan  8 2018 Paul Howarth <paul@city-fan.org> - 2018.01-1
- Update to January 2018 databases

* Thu Dec 21 2017 Paul Howarth <paul@city-fan.org> - 2017.12-1
- Update to December 2017 databases

* Mon Oct  9 2017 Paul Howarth <paul@city-fan.org> - 2017.10-1
- Update to October 2017 databases

* Mon Sep 11 2017 Paul Howarth <paul@city-fan.org> - 2017.09-1
- Update to September 2017 databases

* Wed Aug  9 2017 Paul Howarth <paul@city-fan.org> - 2017.08-1
- Update to August 2017 databases

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Paul Howarth <paul@city-fan.org> - 2017.07-1
- Update to July 2017 databases

* Tue Jun 13 2017 Paul Howarth <paul@city-fan.org> - 2017.06-1
- Update to June 2017 databases

* Tue May  9 2017 Paul Howarth <paul@city-fan.org> - 2017.05-1
- Update to May 2017 databases

* Wed Apr  5 2017 Paul Howarth <paul@city-fan.org> - 2017.04-1
- Update to April 2017 databases
- Drop EL-5 support as it's now EOL

* Fri Mar 10 2017 Paul Howarth <paul@city-fan.org> - 2017.03-1
- Update to March 2017 databases

* Thu Feb  9 2017 Paul Howarth <paul@city-fan.org> - 2017.02-1
- Update to February 2017 databases

* Tue Jan 17 2017 Paul Howarth <paul@city-fan.org> - 2017.01-1
- Update to January 2017 databases

* Tue Dec  6 2016 Paul Howarth <paul@city-fan.org> - 2016.12-1
- Update to December 2016 databases

* Fri Nov 25 2016 Paul Howarth <paul@city-fan.org> - 2016.11-1
- Update to November 2016 databases

* Thu Oct 13 2016 Paul Howarth <paul@city-fan.org> - 2016.10-1
- Update to October 2016 databases

* Tue Sep  6 2016 Paul Howarth <paul@city-fan.org> - 2016.09-1
- Update to September 2016 databases

* Fri Aug  5 2016 Paul Howarth <paul@city-fan.org> - 2016.08-1
- Update to August 2016 databases

* Mon Jul 11 2016 Paul Howarth <paul@city-fan.org> - 2016.07-1
- Update to July 2016 databases

* Tue Jun 21 2016 Paul Howarth <paul@city-fan.org> - 2016.06-1
- Update to June 2016 databases

* Mon May  9 2016 Paul Howarth <paul@city-fan.org> - 2016.05-1
- Update to May 2016 databases

* Wed Apr  6 2016 Paul Howarth <paul@city-fan.org> - 2016.04-1
- Update to April 2016 databases

* Tue Mar  8 2016 Paul Howarth <paul@city-fan.org> - 2016.03-1
- Update to March 2016 databases

* Tue Feb 23 2016 Paul Howarth <paul@city-fan.org> - 2016.02-1
- Update to February 2016 databases

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2016.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Paul Howarth <paul@city-fan.org> - 2016.01-1
- Update to January 2016 databases

* Fri Dec 11 2015 Paul Howarth <paul@city-fan.org> - 2015.12-1
- Update to December 2015 databases

* Mon Nov  9 2015 Paul Howarth <paul@city-fan.org> - 2015.11-1
- Update to November 2015 databases

* Wed Sep  9 2015 Paul Howarth <paul@city-fan.org> - 2015.09-1
- Update to September 2015 databases

* Tue Aug 18 2015 Paul Howarth <paul@city-fan.org> - 2015.08-1
- Update to August 2015 databases

* Wed Jul  8 2015 Paul Howarth <paul@city-fan.org> - 2015.07-1
- Update to July 2015 databases

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Paul Howarth <paul@city-fan.org> - 2015.06-1
- Update to June 2015 databases

* Tue May 12 2015 Paul Howarth <paul@city-fan.org> - 2015.05-1
- Update to May 2015 databases

* Mon Apr 27 2015 Paul Howarth <paul@city-fan.org> - 2015.04-2
- Add symlinks for City databases to be where upstream expects them
  (thanks to nucleo for the suggestion in #1194798)

* Sun Apr 12 2015 Paul Howarth <paul@city-fan.org> - 2015.04-1
- Update to April 2015 databases
- Add %%preun script to remove GeoIP.dat symlink if package is uninstalled

* Wed Apr  1 2015 Paul Howarth <paul@city-fan.org> - 2015.03-3
- Incorporate review feedback (#1194798)
  - Don't package GeoIP.dat symlink; create it in %%posttrans if it doesn't
    exist
  - Update IPASNum databases to current upstream
  - Wrap comments at 80 characters
  - Comment use of EPEL-5 idioms
  - Comment where upstream declares licensing

* Thu Mar  5 2015 Paul Howarth <paul@city-fan.org> - 2015.03-1
- Update to March 2015 databases

* Fri Feb 20 2015 Paul Howarth <paul@city-fan.org> - 2015.02-1
- Databases unbundled from GeoIP, like the old geoip-geolite package
