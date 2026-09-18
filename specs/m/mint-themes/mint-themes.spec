# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           mint-themes
Epoch:          1
Version:        2.2.2
Release:        3%{?dist}
Summary:        Mint themes

# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:        GPL-3.0-or-later
URL:            https://github.com/linuxmint/%{name}
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  fdupes
BuildRequires:  python3
BuildRequires:  python3-libsass

Recommends:     mint-x-icons

%description
A collection of mint themes.

%package -n     mint-y-theme
Summary:        The Mint-Y theme 
Recommends:     mint-y-icons

%description -n	mint-y-theme
The Mint-Y theme.  This theme is based on the Arc theme.

%package -n     mint-themes-gtk3
Summary:        Mint themes for GTK3
Recommends:     mint-themes = %{epoch}:%{version}
Recommends:     mint-y-theme = %{epoch}:%{version}


%description -n	mint-themes-gtk3
A collection of mint themes for GTK3.

%package -n     mint-themes-gtk4
Summary:        Mint themes for GTK4
Recommends:     mint-themes = %{epoch}:%{version}
Recommends:     mint-y-theme = %{epoch}:%{version}

%description -n	mint-themes-gtk4
A collection of mint themes for GTK4.

%package -n	cinnamon-themes
Summary:        Mint themes for GTK3 
Requires:       filesystem
Requires:       mint-themes-gtk3 = %{epoch}:%{version}
Requires:       mint-themes-gtk4 = %{epoch}:%{version}

%description -n	cinnamon-themes
Collection of the best themes available for Cinnamon


%prep
%autosetup -p1

%build
make

%install
%{__cp} -pr usr/ %{buildroot}
%fdupes -s %{buildroot}


%files
%license debian/copyright
%doc debian/changelog
%{_datadir}/themes/Mint-X*/
%exclude %{_datadir}/themes/Mint-X*/gtk-3.0/*
%exclude %{_datadir}/themes/Mint-X*/gtk-4.0/*
%exclude %{_datadir}/themes/Mint-X*/cinnamon/

%files -n mint-y-theme
%license debian/copyright
%doc debian/changelog
%{_datadir}/themes/Mint-Y*/
%exclude %{_datadir}/themes/Mint-Y*/gtk-3.0/*
%exclude %{_datadir}/themes/Mint-Y*/gtk-4.0/*
%exclude %{_datadir}/themes/Mint-Y*/cinnamon/

%files -n mint-themes-gtk3
%license debian/copyright
%doc debian/changelog
%{_datadir}/themes/Mint-X*/gtk-3.0/*
%{_datadir}/themes/Mint-Y*/gtk-3.0/*

%files -n mint-themes-gtk4
%license debian/copyright
%doc debian/changelog
%{_datadir}/themes/Mint-X*/gtk-4.0/*
%{_datadir}/themes/Mint-Y*/gtk-4.0/*

%files -n cinnamon-themes
%license debian/copyright
%doc debian/changelog
%{_datadir}/themes/Mint-X*/cinnamon/
%{_datadir}/themes/Mint-Y*/cinnamon/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Leigh Scott <leigh123linux@gmail.com> - 1:2.2.2-1
- Update to 2.2.2

* Fri Dec 06 2024 Leigh Scott <leigh123linux@gmail.com> - 1:2.2.1-1
- Update to 2.2.1

* Tue Nov 26 2024 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.9-1
- Update to 2.1.9

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 1:2.1.8-2
- convert license to SPDX

* Sat Jul 20 2024 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.8-1
- Update to 2.1.8

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 16 2024 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.7-1
-  Update to 2.1.7

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.6-2
- Use pysassc instead of sassc

* Thu Nov 30 2023 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.6-1
- New upstream release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 09 2023 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.5-1
- New upstream release

* Fri Jun 23 2023 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.2-1
- New upstream release

* Thu Jun 08 2023 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.1-1
- New upstream release

* Tue Jun 06 2023 Leigh Scott <leigh123linux@gmail.com> - 1:2.1.0-1
- New upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Leigh Scott <leigh123linux@gmail.com> - 1:2.0.8-1
- New upstream release

* Fri Nov 25 2022 Leigh Scott <leigh123linux@gmail.com> - 1:2.0.6-1
- New upstream release

* Sun Aug 21 2022 Leigh Scott <leigh123linux@gmail.com> - 1:2.0.5-1
- New upstream release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Leigh Scott <leigh123linux@gmail.com> - 1:2.0.3-1
- New upstream release

* Mon Jul 04 2022 Leigh Scott <leigh123linux@gmail.com> - 1:2.0.1-1
- New upstream release

* Tue Jun 14 2022 Leigh Scott <leigh123linux@gmail.com> - 1:1.9.9-1
- New upstream release

* Sat May 28 2022 Leigh Scott <leigh123linux@gmail.com> - 1:1.9.8-1
- New upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 01 2022 Leigh Scott <leigh123linux@gmail.com> - 1:1.9.6-1
- New upstream release

* Thu Dec 16 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.9.4-1
- New upstream release

* Thu Dec 09 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.9.3-1
- New upstream release

* Mon Dec 06 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.9.2-1
- New upstream release

* Fri Nov 26 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.9-1
- New upstream release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.8-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec  4 2020 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.7-1
- Update to 1.8.7

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 18 2020 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.6-1
- Update to 1.8.6

* Sat Jun 06 2020 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.5-1
- Update to 1.8.5

* Tue May 12 2020 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.4-1
- Update to 1.8.4

* Mon Apr 20 2020 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.4-0.1.20200415git2512422
- Update to git snapshot

* Wed Feb 26 2020 Leigh Scott <leigh123linux@googlemail.com> - 1:1.8.3-3
- Use sassc precompiled source 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:1.8.3-1
- Update to 1.8.3

* Mon Aug 12 2019 Leigh Scott <leigh123linux@gmail.com> - 1:1.8.2-1
- Update to 1.8.2
- Revert upstream Ubuntu font change

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:1.8.1-1
- Update to 1.8.1

* Fri Jul 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:1.8.0-1
- Update to 1.8.0

* Tue Jul 02 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.9-1
- Update to 1.7.9

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 15 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.7-1
- Update to 1.7.7

* Tue Nov 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.4-1
- Update to 1.7.4

* Wed Nov 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.4-0.2.20181112gitb94b890
- Update snapshot

* Mon Nov 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.4-0.1.20181103gitcc5ba69
- Update to git snapshot

* Sun Nov 04 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.3-1
- Update to 1.7.3

* Thu Aug 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.2-1
- Update to 1.7.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.7.1-1
- Update to 1.7.1

* Thu Jun 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.8-1
- Update to 1.6.8

* Sat Jun 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.7-1
- Update to 1.6.7

* Tue May 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.6-1
- Update to 1.6.6

* Mon May 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.5-1
- Update to 1.6.5

* Mon May 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.4-1
- Update to 1.6.4

* Sun May 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.3-1
- Update to 1.6.3

* Fri Apr 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.2-1
- Update to 1.6.2

* Sun Apr 08 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.2-0.5.20180408git0a7f930
- Update to git snapshot

* Fri Apr 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.2-0.4.20180405git295b819
- Update to git snapshot

* Tue Apr 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.2-0.3.20180403gitc402169
- Update to git snapshot

* Tue Apr 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.2-0.2.20180403git1e2c2db
- Update to git snapshot

* Mon Apr 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.2-0.1.20180402git2e06d4d
- Update to git snapshot
- Add build requires python3

* Wed Feb 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:1.6.1-1
- Update to 1.6.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 28 2017 Björn Esser <besser82@fedoraproject.org> - 1.5.0-1
- Initial import (#1529555)

* Thu Dec 28 2017 Björn Esser <besser82@fedoraproject.org> - 1.5.0-0.1
- Initial rpm release (#1529555)
