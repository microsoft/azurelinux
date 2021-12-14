%define luaver 5.2
%define luapkgdir %{_datadir}/lua/%{luaver}

Name:           lua-lunit
Version:        0.5
Release:        18%{?dist}
Summary:        Unit testing framework for Lua

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/mrothNET/lunit
# Source0:      https://github.com/mrothNET/lunit/archive/refs/tags/v0.5.tar.gz
Source0:        https://github.com/mrothNET/lunit/archive/refs/tags/lunit-%{version}.tar.gz

# for running tests
BuildRequires:  lua >= %{luaver}
Requires:       lua >= %{luaver}

BuildArch:      noarch

%description
Lunit is a unit testing framework for lua, written in lua.

Lunit provides 26 assert functions, and a few misc functions for usage
in an easy unit testing framework.

Lunit comes with a test suite to test itself. The testsuite consists
of approximately 710 assertions.


%prep
%setup -q -n lunit-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p lunit $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{luapkgdir}
cp -pr lunit{,-console}.lua $RPM_BUILD_ROOT%{luapkgdir}


%check
./lunit lunit-tests.lua | tee testlog.txt
grep -q "0 failed, 0 errors" testlog.txt



%files
%doc LICENSE ANNOUNCE CHANGES DOCUMENTATION README* example.lua
%{_bindir}/lunit
%{luapkgdir}/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 0.5-6
- rebuild for lua 5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov  5 2009 Michel Salim <salimma@fedoraproject.org> - 0.5-1
- Update to 0.5

* Mon Oct 19 2009 Michel Salim <salimma@fedoraproject.org> - 0.4-2
- Patch out the use of non-existent myerror fn

* Thu Sep 10 2009 Michel Salim <salimma@fedoraproject.org> - 0.4-1
- Initial package
