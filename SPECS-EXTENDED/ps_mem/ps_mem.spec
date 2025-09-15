Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           ps_mem
Version:        3.14
Release:        9%{?dist}
Summary:        Memory profiling tool
License:        LGPL-2.1-only
URL:            https://github.com/pixelb/ps_mem

Source0:        https://raw.githubusercontent.com/pixelb/ps_mem/c80287d/ps_mem.py
Source1:        http://www.gnu.org/licenses/lgpl-2.1.txt
Source2:        ps_mem.1

BuildArch:      noarch

BuildRequires:  python3-devel

%description
The ps_mem tool reports how much core memory is used per program
(not per process). In detail it reports:
sum(private RAM for program processes) + sum(Shared RAM for program processes)
The shared RAM is problematic to calculate, and the tool automatically
selects the most accurate method available for the running kernel.


%prep
%setup -q -T -c %{name}-%{version}

cp -p %{SOURCE0} %{name}
cp -p %{SOURCE1} LICENSE
cp -p %{SOURCE2} %{name}.1

# use python3
sed -i "s|/usr/bin/env python|%{__python3}|" %{name}
touch -r %{SOURCE0} %{name}


%install
install -Dpm755 %{name}   %{buildroot}%{_bindir}/%{name}
install -Dpm644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1


%files
%doc LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 3.14-9
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 Lukáš Zaoral <lzaoral@redhat.com> - 3.14-4
- migrate to SPDX license format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Pádraig Brady <P@draigBrady.com> - 3.14-1
- Latest upstream

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6-7
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.6-3
- Rebuild for Python 3.6

* Mon Jul 11 2016 Lumir Balhar <lbalhar@redhat.com> - 3.6-2
- Fixed missing BuildRequire

* Wed Jun 08 2016 Lumir Balhar <lbalhar@redhat.com> - 3.6-1
- Latest upstream release
- Package ported to Python3 with dependencies

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 16 2015 Pádraig Brady <pbrady@redhat.com> - 3.5-1
- Latest upstream
- Depend on default python implementation

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jaromir Capik <jcapik@redhat.com> - 3.1-4
- RH man page scan (#989490)

* Thu Jul 25 2013 Jaromir Capik <jcapik@redhat.com> - 3.1-3
- Patching shebang to force python3 (#987036)

* Thu May 30 2013 Jaromir Capik <jcapik@redhat.com> - 3.1-2
- Preserving file timestamps

* Wed May 29 2013 Jaromir Capik <jcapik@redhat.com> - 3.1-1
- Initial package
