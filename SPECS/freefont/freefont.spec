%global _fontdir /usr/share/fonts
Summary:        GNU Free fonts
Name:           freefont
Version:        20120503
Release:        3%{?dist}
License:        GPLv3
URL:            https://ftp.gnu.org/pub/gnu/freefont/
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/pub/gnu/%{name}/%{name}-ttf-%{version}.zip

# BUG in Mariner RPMbuilder not providing zip
BuildRequires: fontconfig
BuildRequires: unzip

%description
The GNU FreeFont project aims to provide a useful set of free scalable
(i.e., OpenType) fonts covering as much as possible of the ISO 10646/Unicode
UCS (Universal Character Set).

%prep
%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_fontdir}
mv *.ttf %{buildroot}%{_fontdir}/
fc-cache

%files
%defattr(-,root,root)
%license COPYING
%{_fontdir}/*.ttf

%changelog
* Tue Jun 20 2023 Osama Esmail <osamaesmail@microsoft.com> - 20120503-3
- Added `BuildRequires: fontconfig`
- Run `fc-cache` after install

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 20120503-2
- Added %%license line automatically

* Wed Apr 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 20120503-1
- Original version for CBL-Mariner.
