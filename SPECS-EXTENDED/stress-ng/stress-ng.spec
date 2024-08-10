Name:		stress-ng
Version:	0.18.02
Release:    2%{?dist}	
Summary:	Stress test a computer system in various ways

License:	GPL-2.0-or-later
URL:		https://github.com/ColinIanKing/stress-ng
Source0:	https://github.com/ColinIanKing/stress-ng/archive/V%{version}/%{name}-%{version}.tar.gz
# darn is not supported in Power ISA < 3.0, while Fedora aims for Power ISA 2.07

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	glibc-devel
BuildRequires:	kernel-headers
BuildRequires:	keyutils-libs-devel
BuildRequires:	libaio-devel
BuildRequires:	libattr-devel
%if %{undefined rhel}
BuildRequires:	libbsd-devel
%endif
BuildRequires:	libcap-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	lksctp-tools-devel
BuildRequires:	libatomic
BuildRequires:	zlib-devel
BuildRequires:	Judy-devel

%description
Stress test a computer system in various ways. It was designed to exercise
various physical subsystems of a computer as well as the various operating
system kernel interfaces.

%prep
%autosetup -n %{name}-%{version}

%build
%make_build

%install
install -p -m 755 -D %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 644 -D %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
install -pm 644 bash-completion/%{name} \
    %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Sat Aug 10 2024 Chris Co <chrco@microsoft.com> - 0.18.02-2
- Drop powerpc patch since Azure Linux does not support powerpc
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Wed Jul 31 2024 Fabio Alessandro Locati <me@fale.io> - 0.18.02-1
- Update to 0.18.02

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Fabio Alessandro Locati <me@fale.io> - 0.18.01-1
- Update to 0.18.01. Fixes rhbz#2257061

* Tue Feb 06 2024 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.17.05-1
- Update to 0.17.05
- Fixes rhbz#2257061

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 17 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.17.03-1
- Update to 0.17.03
- Fixes rhbz#2253639

* Mon Dec 04 2023 John Kacur <jkacur@redhat.com> - 0.17.01-2
- Update the License field to the SPDX format using the tools
  license-fedora2spdx and verified by license-validate

* Sat Nov 11 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.17.01-1
- Update to 0.17.01
- Fixes rhbz#2242847

* Wed Oct 11 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.17.00-1
- Update to 0.17.00
- Fixes rhbz#2242847

* Sun Oct 01 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.16.05-1
- Update to 0.16.05
- Fixes rhbz#2237812

* Mon Aug 14 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.16.04-1
- Update to 0.16.04
- Fixes rhbz#2231634

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.16.02-1
- Update to 0.16.02
- Fixes rhbz#2222484

* Sat Jul 08 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.16.00-1
- Update to 0.16.00
- Fixes rhbz#2221348

* Sat Jun 17 2023 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.15.10-1
- Update to 0.15.10
- Fixes rhbz#2186552

* Mon Jun 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.15.06-2
- Disable libbsd dependency in RHEL builds

* Sat Mar 25 2023 Fabio Alessandro Locati <fale@fedoraproject.ora> - 0.15.06-1
- Update to 0.15.06
- Fixes rhbz#2179538

* Sat Mar 11 2023 Fabio Alessandro Locati <fale@fedoraproject.ora> - 0.15.05-1
- Update to 0.15.05
- Fixes rhbz#2130476

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Florian Weimer <fweimer@redhat.com> - 0.15.00-2
- Improve compatibility with strict(er) C99 compilers

* Wed Dec 07 2022 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.15.00-1
- Update to 0.15.00

* Sat Sep 17 2022 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.14.05-1
- Update to 0.14.05

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.14.02-1
- Update to 0.14.02

* Wed Feb 02 2022 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.13.11-1
- Update to 0.13.11
- move source to github since the author changed company
- clean the build process

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 31 2021 Chris Brown <chris.brown@redhat.com> - 0.13.00-1
- Update to 0.13.00

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Chris Brown <chris.brown@redhat.com> - 0.12.10-1
- Update to 0.12.10

* Mon Mar 1 2021 Chris Brown <chris.brown@redhat.com> - 0.12.04-1
- Update to 0.12.04

* Wed Feb 24 2021 Yaakov Selkowitz <yselkowi@redhat.com> - 0.12.03-2
- Enable ppc64le

* Mon Feb 15 2021 Chris Brown <chris.brown@redhat.com> - 0.12.03-1
- Update to 0.12.03

* Sun Feb 7 2021 Chris Brown <chris.brown@redhat.com> - 0.12.02-1
- Bump to 0.12.02

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 26 2020 Chris Brown <chris.brown@redhat.com> - 0.12.01-1
- Bump to 0.12.01

* Tue Dec 8 2020 Chris Brown <chris.brown@redhat.com> - 0.12.00-1
- Bump to 0.12.00

* Tue Dec 1 2020 Chris Brown <chris.brown@redhat.com> - 0.11.24-1
- Bump to 0.11.24

* Tue Nov 10 2020 Chris Brown <chris.brown@redhat.com> - 0.11.23-1
- Bump to 0.11.23
- Drop EPEL 8 Judy conditional

* Wed Sep 30 2020 Chris Brown <chris.brown@redhat.com> - 0.11.21-1
- Bump to 0.11.21

* Thu Sep 03 2020 Chris Brown <chris.brown@redhat.com> - 0.11.19-1
- Bump to 0.11.19

* Tue Aug 18 2020 Chris Brown <chris.brown@redhat.com> - 0.11.14-6
- Add Judy conditional for EPEL 8

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.14-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11.14-3
- Fix bash completion path

* Mon Jul 06 2020 Chris Brown <chris.brown@redhat.com> - 0.11.14-2
- Add bash completion
- Enable Judy, libatomic and libgcrypt
- Switch source and URL to https

* Fri Jul 03 2020 Chris Brown <chris.brown@redhat.com> - 0.11.14-1
- Bump to 0.11.14

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 0.07.29-8
- Rebuilt for libcrypt.so.2 (#1666033)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.07.29-5
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 18 2017 Fedora <sspreitz@redhat.com> - 0.07.29-2
- exclude ppc64 and ppc64le archs

* Tue Apr 18 2017 Fedora <sspreitz@redhat.com> - 0.07.29-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.07.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Sascha Spreitzer <sspreitz@redhat.com> - 0.07.05-3
- License is GPLv2+

* Sun Nov 20 2016 Sascha Spreitzer <sspreitz@redhat.com> - 0.07.05-2
- enhance building

* Sun Nov 20 2016 Sascha Spreitzer <sspreitz@redhat.com> - 0.07.05-1
- new version

* Mon Nov 14 2016 Sascha Spreitzer <sspreitz@redhat.com> - 0.07.04-1
- new version

* Mon Jun 13 2016 Sascha Spreitzer <sspreitz@redhat.com> - 0.06.06-1
- new version

* Fri Apr 29 2016 Sascha Spreitzer <sspreitz@redhat.com> - 0.05.25-1
- initial spec file
