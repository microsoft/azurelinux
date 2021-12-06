Summary:        Remove embedding limitations from TrueType fonts
Name:           ttembed
Version:        1.1
Release:        15%{?dist}
License:        Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/hisdeedsaredust/ttembed
Source0:        https://github.com/hisdeedsaredust/ttembed/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc

%description
Remove embedding limitations from TrueType fonts, by setting the fsType field
in the OS/2 table to zero. That's it; this program is a one-trick pony.

%prep
%autosetup

%build
CFLAGS="$CFLAGS %{optflags}" %make_build

%install
install -d %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1/
install -p -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*

%check
# smoke test - fail on not font file
result=0
echo 'not a font' > test
if [[ "$(./ttembed test 2>&1)" != "test: Not TTF/OTF" ]] ; then
    echo "TEST FAIL: not a font input test" 1>&2
    result=1
fi
rm test
[[ $result -eq 0 ]]

%changelog
* Mon Dec 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-15
- License verified.
- Removing 'exit' from the %%check section.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 2 2013 Petr Vobornik <pvoborni@redhat.com> - 1.1-1
- initial package
