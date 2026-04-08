# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define             fontdir %{_datadir}/fonts/%{name}
%define             catalogue %{_sysconfdir}/X11/fontpath.d

Name:               zvbi
Version:            0.2.44
Release:            2%{?dist}
Summary:            Raw VBI, Teletext and Closed Caption decoding library
License:            GPL-2.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-2-Clause AND MIT
URL:                https://github.com/zapping-vbi/zvbi
Source0:            https://github.com/zapping-vbi/zvbi/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:             %{name}-0.2.24-tvfonts.patch
Patch1:             %{name}-0.2.25-openfix.patch

BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      bdftopcf
BuildRequires:      doxygen
BuildRequires:      fontconfig
BuildRequires:      gcc-c++
BuildRequires:      gettext-devel
BuildRequires:      libICE-devel
BuildRequires:      libpng-devel
BuildRequires:      libtool
BuildRequires:      make
BuildRequires:      mkfontdir
BuildRequires:      systemd-units
BuildRequires:      tzdata


%description
ZVBI provides functions to capture and decode VBI data. The vertical blanking
interval (VBI) is an interval in a television signal that temporarily suspends
transmission of the signal for the electron gun to move back up to the first
line of the television screen to trace the next screen field. The vertical
blanking interval can be used to carry data, since anything sent during the VBI
would naturally not be displayed; various test signals, closed captioning, and
other digital data can be sent during this time period.


%package devel
Summary:            Development files for zvbi
Requires:           %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for zvbi


%package fonts
Summary:            Fonts from zvbi converted to X11
BuildArch:          noarch
Obsoletes:          xawtv-tv-fonts < 3.95
Provides:           xawtv-tv-fonts >= 3.95

%description fonts
Fonts from zvbi converted for use with X11


%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

# systemd service file
cat >zvbid.service <<EOF
[Unit]
Description=Proxy Sharing V4L VBI Device Between Applications
After=syslog.target

[Service]
Type=forking
ExecStart=%{_sbindir}/zvbid

[Install]
WantedBy=multi-user.target

EOF


%build
./autogen.sh
# Note: We don't do --enable-static=no because static libs are needed to build
# x11font during compile time to convert zvbi fonts into x11 fonts. x11font
# is thrown away and not installed as it's not useful for anything else
%configure --disable-rpath --enable-v4l --enable-dvb --enable-proxy

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

# Generate fonts, fonts.alias and fonts.dir
pushd contrib
./x11font
for font in *.bdf
do
    bdftopcf $font | gzip -9 -c > ${font%.bdf}.pcf.gz
done
mkfontdir -x .bdf .
cat >fonts.alias <<EOF
teletext   -ets-teletext-medium-r-normal--*-200-75-75-c-120-iso10646-1
EOF
popd


%install
mkdir -p %{buildroot}%{fontdir}
%make_install

%find_lang %{name}

mkdir -p %{buildroot}%{_unitdir}
install -m644 zvbid.service %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_initrddir}

install -pm0644 contrib/*.pcf.gz %{buildroot}%{fontdir}
install -pm0644 contrib/fonts.* %{buildroot}%{fontdir}
touch %{buildroot}%{fontdir}/fonts.cache-1

mkdir -p %{buildroot}%{catalogue}
ln -sf %{fontdir} %{buildroot}%{catalogue}/%{name}

find %{buildroot}%{_libdir} -name '*.a' -delete


%check
cd test
make check


%post
%systemd_post zvbid.service


%preun
%systemd_preun zvbid.service


%postun
%systemd_postun_with_restart zvbid.service


%files -f %{name}.lang
%license COPYING.md
%doc AUTHORS BUGS ChangeLog NEWS README.md TODO
%{_bindir}/%{name}*
%if ! (0%{?fedora} >= 42)
%{_sbindir}/zvbid
%endif
%{_unitdir}/zvbid.service
%{_libdir}/libzvbi.so.0*
%{_libdir}/libzvbi-chains.so.0*
%{_mandir}/man1/zvbi*1*


%files devel
%{_includedir}/libzvbi.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-0.2.pc


%files fonts
%dir %{_datadir}/fonts/%{name}
%{fontdir}/*.gz
%{fontdir}/fonts.dir
%{fontdir}/fonts.alias
%{catalogue}/%{name}
%ghost %{fontdir}/fonts.cache-1


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 14 2025 Xavier Bachelot <xavier@bachelot.org> - 0.2.44-1
- Update to 0.2.44 (RHBZ#2351225)
- Acknowledge for bin/sbin merge in F42+

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Xavier Bachelot <xavier@bachelot.org> - 0.2.43-1
- Update to 0.2.43 (RHBZ#2330170)

* Fri Sep 13 2024 Xavier Bachelot <xavier@bachelot.org> - 0.2.42-1
- Update to 0.2.42

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 17 2023 David Cantrell <dcantrell@redhat.com> - 0.2.35-20
- Update License tag to use SPDX identifiers
- Change deprecated %%patchN macros to %%patch -P N

* Sun Feb 05 2023 Kalev Lember <klember@redhat.com> - 0.2.35-19
- Avoid requiring systemd for systemd rpm scriptlets

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
- avoid rpath in binaries

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.35-14
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar  1 2021 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.35-13
- Fix BuildRequires (#1933652)

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.35-8
- Remove obsolete scriptlets

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Feb 14 2016 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.35-1
- Update to 0.2.35

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.33-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 24 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-14
- new systemd-rpm macros (#850382)
- drop sysv triggerun migration

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Hans de Goede <hdegoede@redhat.com> - 0.2.33-11
- Fix build with libpng-1.5

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.33-10
- Rebuild for new libpng

* Fri Sep 23 2011 Tom Callaway <spot@fedoraproject.org> - 0.2.33-9
- add missing triggerun for systemd migration

* Tue Sep  6 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-8
- Drop chkconfig stuff completely

* Wed Aug 17 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-7
- Migration from SysV to Systemd init system (#730154)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 21 2010 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-5
- add patch to fix compiling under rawhide (#564991)
- make fonts subpackage arch independent

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 25 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-3
- Rebuilt for #491975

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 14 2008 Subhodip Biswas <subhodip@fedoraproject.org > - 0.2.33-1
- Package update .
* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.2.30-2
- Fix Patch0:/%%patch mismatch.

* Wed Mar 05 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.30-1
- Update to 0.2.30
- Updated license field due to license change GPLv2+ -> LGPLv2+
- Dropped encoding fixes for ChangeLog. No longer needed.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.26-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.26-2
- Release bump

* Sun Jan 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.26-1
- Upgrade to 0.2.26

* Wed Aug 22 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.25-2
- Release bump for F8 mass rebuild
- License change due to new guidelines
- Use fontpath.d for F8+
- Added patch to fix compilation with open() macro on F8+

* Sun May 27 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.25-1
- Upgrade to 0.2.25

* Tue Mar 13 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.24-1
- Upgrade to 0.2.24
- Convert README and ChangeLog to UTF-8
- Added patch for x11font to generate more font sizes useful for other
  applications such as xawtv (courtesy of Dmitry Butskoy)
- Fonts sub-rpm now obsoletes and provides xawtv-tv-fonts
- Split font generation and font installation into separate sections
- Various other minor changes to the spec
- Added xfs support for the fonts

* Fri Sep 01 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.22-2
- Minor spec cleanups

* Tue Aug 29 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.22-1
- Initial release
