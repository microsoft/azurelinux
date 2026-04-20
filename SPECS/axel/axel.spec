Summary:        Light command line download accelerator for Linux and Unix
Name:           axel
Version:        2.17.14
Release:        4%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/axel-download-accelerator/axel
Source0:        https://github.com/axel-download-accelerator/axel/archive/v%{version}/axel-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  txt2man

%description
Axel tries to accelerate HTTP/FTP downloading process by using
multiple connections for one file. It can use multiple mirrors for a
download. Axel has no dependencies and is lightweight, so it might
be useful as a wget clone on byte-critical systems.

%prep
%autosetup -p1

%build
autoreconf -vfi
%{configure}
%make_build


%install
%make_install \

mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 -p -T doc/axelrc.example %{buildroot}%{_sysconfdir}/axelrc

%find_lang %{name}


%files -f %{name}.lang
%{_bindir}/%{name}
%doc ChangeLog README.md doc/API
%license COPYING
%config(noreplace) %{_sysconfdir}/axelrc
%{_mandir}/man1/axel.1*


%changelog
* Sun Apr 20 2026 Zhichun Wan <zhichunwan@microsoft.com> - 2.17.14-4
- Initial Azure Linux import from Fedora 42 (license: GPL-2.0-or-later).
- License verified.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 Packit <hello@packit.dev> - 2.17.14-1
- Update to 2.17.14 upstream release
- Resolves: rhbz#2274014

* Wed Feb 07 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.17.13-1
- feat: update to 2.17.13 (fixes rh#2261961)

* Wed Feb 07 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.17.11-8
- chore: add packit

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 09 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.17.11-2
- chore: bump for branch

* Tue Feb 08 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.17.11-1
- feat: update to 2.17.11 (fixes rhbz#2034429)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.17.10-3
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.17.10-1
- Updated to axel-2.17.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 10 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.16-1
- Update to latest upstream release
- Add gcc g++ to BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.15-1
- Update to latest release
- Update upstream location

* Sun Sep 10 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.13.1-2
- Spec update

* Sun Sep 10 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.13.1-1
- Update to latest upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.5-1
- Update to new release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Apr 17 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.4-4
- rebuilt to fix 583210

* Mon Feb 15 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.4-3
- rebuilt to fix 564650

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.4-1
- initial rpm build
