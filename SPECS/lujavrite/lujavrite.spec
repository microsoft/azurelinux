Name:           lujavrite
Version:        1.0.2
Release:        5%{?dist}
Summary:        Lua library for calling Java code
License:        Apache-2.0
URL:            https://github.com/mizdebsk/lujavrite

Source0:        https://github.com/mizdebsk/lujavrite/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  lua-devel
BuildRequires:  java-devel >= 1.8

%description
LuJavRite is a rock-solid Lua library that allows calling Java code
from Lua code.  It does so by launching embedded Java Virtual Machine
and using JNI interface to invoke Java methods.

%prep
%setup -q

%build
export JAVA_HOME=$(find %{_libdir}/jvm -name "msopenjdk*")

./build.sh

%install
install -D -p -m 0755 lujavrite.so %{buildroot}%{lua_libdir}/%{name}.so

%check
lua test.lua

%files
%{lua_libdir}/*
%license LICENSE NOTICE
%doc README.md

%changelog
* Thu Apr 04 2024 Mitch Zhu <mitchzhu@microsoft.com> - 1.0.2-5
- Initial Azure Linux import from Fedora 40 (license: MIT).
- License verified.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.2-1
- Update to upstream version 1.0.2

* Wed Mar 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.1-1
- Initial packaging
