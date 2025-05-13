Distribution:   Azure Linux
Name:           nanomsg
Vendor:         Microsoft Corporation
Version:        1.2.1
Release:        2%{?dist}
Summary:        Socket library that provides several common communication patterns

License:        MIT
URL:            https://nanomsg.org/
Source0:        https://github.com/nanomsg/nanomsg/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake3
BuildRequires:  gcc
# For docs only, can be skipped
BuildRequires:  rubygem-asciidoctor

%description
The nanomsg library is a simple high-performance implementation of several
"scalability protocols". These scalability protocols are light-weight messaging
protocols which can be used to solve a number of very common messaging patterns,
such as request/reply, publish/subscribe, surveyor/respondent, and so forth.
These protocols can run over a variety of transports such as TCP, UNIX sockets,
and even WebSocket.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%autosetup -p1


%build
%cmake3 \
  -DTHREADSAFE=ON \
  %{nil}
%cmake3_build


%install
%cmake3_install


%check
%ctest3


%files
%license COPYING
%{_bindir}/nanocat
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/nanocat.1*

%files devel
%doc tests
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}-%{version}/
%{_includedir}/%{name}/
%{_defaultdocdir}/%{name}/
%{_mandir}/man3/nn_*.3*
%{_mandir}/man7/nn_*.7*
%{_mandir}/man7/%{name}.7*

%files doc
%doc AUTHORS doc README.md RELEASING SUPPORT


%changelog
* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Scott K Logan <logans@cottsay.net> - 1.2.1-1
- Update to 1.2.1 (rhbz#2262607)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 24 2020 Scott K Logan <logans@cottsay.net> - 1.1.5-6
- Fix FTBFS (rhbz#1864185)
- Use EPEL 7 compatible CMake macros
- Add an rpmlintrc to suppress spelling suggestions

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 18 2019 Troy Dawson <tdawson@redhat.com> - 1.1.5-1
- Initial package
