# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


Name:           zig-srpm-macros
Version:        1
Release: 6%{?dist}
Summary:        SRPM macros required for Zig packages

License:        MIT

Source0:        macros.zig-srpm
Source100:      LICENSE

BuildArch:      noarch

Requires:       rpm

%description
%{summary}

%prep
%autosetup -c -T
cp -a %{sources} .

%install
mkdir -p %{buildroot}%{rpmmacrodir}
install -pm 644 macros.* %{buildroot}%{rpmmacrodir}/

%files
%license LICENSE
%{rpmmacrodir}/macros.zig-srpm

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Jan Drögehoff <sentrycraft123@gmail.com> - 1-1
- Initial spec
