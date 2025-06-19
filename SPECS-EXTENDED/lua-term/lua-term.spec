Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global luaminver 5.2

#global commit 76d7c992a22d4481969a977ad36d6d35d3b2ca6f
#global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           lua-term
Version:        0.08
Release:        5%{?dist}
Summary:        Terminal functions for Lua

License:        MIT
URL:            https://github.com/hoelzro/%{name}
Source0:        https://github.com/hoelzro/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  lua-devel >= %{luaminver}
Requires:       lua(abi) = %{lua_version}
Requires:       lua >= %{lua_version}

%description
Lua module for manipulating a terminal.

%prep
# Lua is no longer installed by default. Grab Lua version for use in
# determining install locations.
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}
# for arch-independent modules
%global luapkgdir %{_datadir}/lua/%{luaver}

%setup -q

%build
%{__cc} %{optflags} -fPIC -c core.c -o core.o
%{__cc} %{__global_ldflags} -shared -o core.so core.o
chmod 755 core.so

%install
mkdir -p %{buildroot}%{luapkgdir}
cp -rp term  %{buildroot}%{luapkgdir}/
mkdir -p %{buildroot}%{lualibdir}/term
cp -p core.so %{buildroot}%{lualibdir}/term/

%files
%license COPYING
%doc CHANGES README.md
%{lualibdir}/term/
%{luapkgdir}/term/

%changelog
* Tue Apr 08 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.08-5
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 01 2024 Orion Poplawski <orion@nwra.com> - 0.08-1
- Update to 0.08

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Björn Esser <besser82@fedoraproject.org> - 0.07-11
- Rebuilt for Lua 5.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Jeff Backus <jeff.backus@gmail.com> - 0.07-6
- Fixed FTBFS issues related Fedora 28 Mass Rebuild (#1583364)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Apr 10 2016 Orion Poplawski <orion@cora.nwra.com> - 0.07-1
- Update to 0.07

* Tue Apr 5 2016 Orion Poplawski <orion@cora.nwra.com> - 0.06-1
- Update to 0.06

* Mon Apr 4 2016 Orion Poplawski <orion@cora.nwra.com> - 0.05-1
- Update to 0.05

* Sun Mar 6 2016 Orion Poplawski <orion@cora.nwra.com> - 0.04-1
- Update to 0.04
- Use %%{__global_ldflags}
- Use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Tom Callaway <spot@fedoraproject.org> - 0.03-6
- rebuild for lua 5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 2 2014 Orion Poplawski <orion@cora.nwra.com> - 0.03-3
- Fix EL6 lua requires

* Fri May 2 2014 Orion Poplawski <orion@cora.nwra.com> - 0.03-2
- Use git hash for source
- Fix .so permissions

* Thu May 1 2014 Orion Poplawski <orion@cora.nwra.com> - 0.03-1
- Update to 0.03
- Cleanup spec
- Support EL6

* Wed Oct 09 2013 Jiri Machala <george.machala@gmail.com> - 0.02-1
- Initial version

