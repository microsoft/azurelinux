Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		console-setup
Version:	1.230
Release:	2%{?dist}
Summary:	Tools for configuring the console using X Window System key maps

# For a breakdown of the licensing, see COPYRIGHT, copyright, copyright.fonts and copyright.xkb
License:	GPL-2.0-or-later AND MIT AND LicenseRef-Fedora-Public-Domain
URL:		http://packages.debian.org/cs/sid/console-setup
Source0:	http://ftp.de.debian.org/debian/pool/main/c/%{name}/%{name}_%{version}.tar.xz

# Fixes installing paths to Fedora style
Patch0:		console-setup-1.76-paths.patch
# Fixes FSF address, sent to upstream
Patch1:		console-setup-1.76-fsf-address.patch
# Removes Caps_Lock to CtrlL_Lock substitution
Patch2:		console-setup-1.84-ctrll-lock.patch

Requires:	kbd
# require 'xkeyboard-config' to have X Window keyboard descriptions?

BuildRequires:	perl-generators
BuildRequires:	perl(encoding) perl(open)
BuildRequires:	make
BuildArch:	noarch

%description
This package provides the console with the same keyboard configuration
scheme that X Window System has. Besides the keyboard, the package configures
also the font on the console.  It includes a rich collection of fonts and
supports several languages that would be otherwise unsupported on the console
(such as Armenian, Georgian, Lao and Thai).


%package -n bdf2psf
Summary:	Generate console fonts from BDF source fonts

%description -n bdf2psf
This package provides a command-line converter that can be used in scripts
to build console fonts from BDF sources automatically. The converter comes
with a collection of font encodings that cover many of the world's
languages. The output font can use a different character encoding from the
input. When the source font does not define a glyph for a particular
symbol in the encoding table, that glyph position in the console font is
not wasted but used for another symbol.


%prep
%setup -q -n %{name}-%{version}
%autopatch -p1

cp -a --remove-destination debian/copyright COPYRIGHT
cp -a --remove-destination debian/changelog CHANGES

%build
make build-linux


%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT install-linux
# we don't want another set of keyboard descriptions, we want to use descriptions from
# xkeyboard-config (require it?), so removing it
# or maybe have these from tarball it in optional subpackage?
rm -rf $RPM_BUILD_ROOT/etc/console-setup

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -pm644 man/bdf2psf.1 $RPM_BUILD_ROOT%{_mandir}/man1/

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p Fonts/bdf2psf $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/bdf2psf
cp -a Fonts/fontsets Fonts/*.equivalents Fonts/*.set \
	$RPM_BUILD_ROOT%{_datadir}/bdf2psf/


%files
%doc README COPYRIGHT CHANGES copyright.fonts copyright.xkb Fonts/copyright
%{_bindir}/ckbcomp
%{_bindir}/setupcon
%config(noreplace) %{_sysconfdir}/default/console-setup
%config(noreplace) %{_sysconfdir}/default/keyboard
%{_datadir}/consolefonts
%{_datadir}/consoletrans
%{_mandir}/*/*


%files -n bdf2psf
%{_bindir}/bdf2psf
%{_mandir}/man1/bdf2psf.1*
%{_datadir}/bdf2psf
%license GPL-2


%changelog
* Tue Dec 17 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.230-2
- AzureLinux import from Fedora 41 
- License verified

* Wed Jul 17 2024 Packit <hello@packit.dev> - 1.230-1
- Update to latest upstream version

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Packit <hello@packit.dev> - 1.228-1
- Update to latest upstream version

* Sun Jan 28 2024 Packit <hello@packit.dev> - 1.224-1
- Update to latest upstream version

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.223-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.223-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Packit <hello@packit.dev> - 1.223-1
- Update to latest upstream version

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.222-1
- Update to latest upstream version
  Resolves: #2216578

* Thu May 25 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.221-1
- Update to latest upstream version
  Resolves: #2208916

* Tue May 16 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.220-1
- Update to latest upstream version
  Resolves: #2196018

* Thu Apr 27 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.219-1
- Update to latest upstream version
  Resolves: #2189733

* Tue Mar 28 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.218-2
- SPDX migration

* Fri Mar 17 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.218-1
- Update to latest upstream version
  Resolves: #2178377

* Thu Feb 16 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.217-1
- Update to latest upstream version
  Resolves: #2170210

* Fri Feb 03 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.216-1
- Update to latest upstream version
  Resolves: #2166117

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.215-1
- Update to latest upstream version
  Resolves: #2156436

* Fri Dec 16 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.212-1
- Update to latest upstream version
  Resolves: #2152910

* Wed Oct 19 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.211-1
- Update to latest upstream version
  Resolves: #2135993

* Thu Sep 15 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.210-1
- Update to latest upstream version
  Resolves: #2120120

* Thu Jul 21 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.209-1
- Update to latest upstream version
  Resolves: #2108201

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.208-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.208-1
- Update to latest upstream version
  Resolves: #2090948

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 09 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.207-1
- Update to latest upstream version
  Resolves: #2018840

* Tue Aug 31 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.205-1
- Update to latest upstream version
  Resolves: #1985584

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.204-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.204-1
- Update to latest upstream version
  Resolves: #1980566

* Thu Jun 03 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.203-1
- Update to latest upstream version
  Resolves: #1965868

* Tue May 11 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.202-2
- Use the "base" XKB files, not "xorg" (patch by Peter Hutterer)
  Resolves: #1951453

* Wed Mar 24 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.202-1
- Update to latest upstream version
  Resolves: #1941247

* Wed Mar 10 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.201-1
- Update to latest upstream version
  Resolves: #1930510

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.200-1
- Update to latest upstream version
  Resolves: #1911871

* Mon Dec 07 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.199-1
- Update to latest upstream version
  Resolves: #1902975

* Mon Nov 09 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.198-1
- Update to latest upstream version
  Resolves: #1893002

* Tue Sep 22 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.197-1
- Update to latest upstream version
  Resolves: #1881276

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.196-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.196-1
- Update to latest upstream version
  Resolves: #1856118

* Mon Mar 30 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.195-1
- Update to latest upstream version
  Resolves: #1817552

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.194-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.194-1
- Update to latest upstream version
  Resolves: #1773413

* Wed Sep 04 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.193-1
- Update to latest upstream version
  Resolves: #1742489

* Tue Jul 30 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.192-1
- Update to latest upstream version
  Resolves: #1727182

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.191-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.191-1
- Update to latest upstream version
  Resolves: #1692077

* Tue Mar 19 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.190-1
- Update to latest upstream version
  Resolves: #1685067

* Fri Mar 08 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.189-2
- Package bdf2psf as well

* Tue Feb 12 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.189-1
- Update to latest upstream version
  Resolves: #1674091

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.186-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 04 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.186-1
- Update to latest upstream version
  Resolves: 1632056

* Mon Aug 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.185-1
- Update to latest upstream version
  Resolves: #1616114

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.184-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.184-2
- Remove Caps Lock to CtrlL_Lock substitution
  Resolves: #1586149

* Thu Apr 19 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.184-1
- Update to latest upstream version
  Resolves: #1562605

* Wed Mar 28 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.181-1
- Update to latest upstream version
  Resolves: #1556587

* Wed Mar 14 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.179-1
- Remove Group tag
- Update to latest upstream version
  Resolves: #1545959

* Wed Feb 07 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.177-1
- Update to latest upstream version
  Resolves: #1536894

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.175-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.175-1
- Update to latest upstream version
  Resolves: #1534075

* Wed Jan 03 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.174-1
- Update to latest upstream version
  Resolves: #1528872

* Thu Dec 14 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.173-1
- Update to latest upstream version
  Resolves: #1524079

* Thu Nov 23 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.170-1
- Update to latest upstream version
  Resolves: #1508170

* Wed Oct 25 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.169-1
- Update to latest upstream version
  Resolves: #1503366

* Tue Sep 19 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.167-1
- Update to latest upstream version
  Resolves: #1467455

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.165-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.165-1
- Update to latest upstream version
  Resolves: #1465190

* Thu Apr 20 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.164-1
- Update to latest upstream version
  Resolves: #1428812

* Thu Mar 02 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.162-1
- Update to latest upstream version
  Resolves: #1421122

* Wed Feb 08 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.158-1
- Update to latest upstream version
  Resolves: #1414397

* Mon Jan 16 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.157-1
- Update to latest upstream version
  Resolves: #1410956

* Mon Dec 19 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.155-1
- Update to latest upstream version
  Resolves: #1404057

* Thu Nov 24 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.154-1
- Update to latest upstream version
  Resolves: #1394588

* Mon Oct 24 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.152-1
- Update to latest upstream version
  Resolves: #1378257

* Wed Sep 21 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.149-1
- Update to latest upstream version
  Resolves: #1377144

* Thu Aug 04 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.148-1
- Update to latest upstream version
  Resolves: #1361821

* Mon Jul 25 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.147-1
- Update to latest upstream version
  Resolves: #1357700

* Mon Jun 06 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.146-1
- Update to latest upstream version
  Resolves: #1343049

* Wed Jun 01 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.145-1
- Update to latest upstream version
  Resolves: #1341357

* Tue May 24 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.143-1
- Update to latest upstream version
  Resolves: #1338765

* Mon Apr 25 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.142-1
- Update to latest upstream version
  Resolves: #1323370

* Tue Mar 29 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.140-1
- Update to latest upstream version
  Resolves: #1314573

* Mon Feb 29 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.137-1
- Update to latest upstream version
  Resolves: #1310912

* Thu Feb 04 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.131-2
- Update to latest upstream version
  Resolves: #1303783

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.135-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.135-1
- Update to latest upstream version
  Resolves: #1303365

* Wed Nov 25 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.134-1
- Update to latest upstream version
  Resolves: #1275853

* Mon Oct 19 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.133-1
- Update to latest upstream version
  Resolves: #1246800, #1266276

* Thu Aug 27 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.132-1
- Update to latest upstream version
  Resolves: #1246800, #1256135

* Wed Jul 15 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.130-1
- Update to latest upstream version
  Resolves: #1236429

* Tue Jun 23 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.128-1
- Update to latest upstream version
  Resolves: #1222723

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.126-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.126-1
- Update to latest upstream version
  Resolves: #1221402

* Mon May 04 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.124-1
- Update to latest upstream version
  Resolves: #1217018

* Wed Apr 22 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.123-1
- Update to latest upstream version
  Resolves: #1212233

* Tue Apr 14 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.121-1
- Update to latest upstream version
  Resolves: #1210953

* Tue Mar 31 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.120-1
- Update to latest upstream version
  Resolves: #1206848

* Thu Mar 05 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.118-1
- Update to latest upstream version
  Resolves: #1199059

* Mon Feb 23 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.117-1
- Update to latest upstream version
  Resolves: #1195090

* Mon Dec 08 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.116-1
- Update to latest upstream version
  Resolves: #1170951

* Wed Nov 12 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.115-1
- Update to latest upstream version
  Resolves: #1163117

* Thu Oct 30 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.114-1
- Update to latest upstream version
  Resolves: #1157435

* Wed Oct 01 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.113-1
- Update to latest upstream version
  Resolves: #1138997

* Mon Sep 01 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.111-1
- Update to latest upstream version
  Resolves: #1129030

* Mon Aug 04 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.110-1
- Update to latest upstream version
  Resolves: #1124031

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.108-1
- Update to latest upstream version
  Resolves: #1096045

* Thu Apr 10 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.107-1
- Update to latest upstream version
  Resolves: #1084949

* Thu Mar 20 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.106-1
- Update to latest upstream version
  Resolves: #1078695

* Thu Jan 02 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.104-1
- Update to latest upstream version
  Resolves: #1040384

* Wed Nov 06 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.102-1
- Update to latest upstream version
  Resolves: #1026672
- Fix bogus date in %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.87-3
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.87-1
- Update to latest upstream version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.80-1
- Update to latest upstream version
- Fix files listed twice build warning

* Tue Jun 26 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.76-2
- Fix License field
- Do not own /etc/default directory
- Fix FSF address in ckbcomp utility
- Fix paths in manpages

* Wed Jun 20 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.76-1
- Initial support
