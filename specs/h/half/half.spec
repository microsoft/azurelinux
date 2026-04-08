# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# there is no debug package
%global debug_package %{nil}

Name:           half
Version:        2.2.0
Release:        8%{?dist}
Summary:        A C++ half-precision floating point type
License:        MIT

URL:            http://sourceforge.net/projects/half
Source0:        %{url}/files/%{name}/%{version}/%{name}-%{version}.zip
BuildArch:      noarch

BuildRequires:  unzip

%description
This is a C++ header-only library to provide an IEEE-754 conformant
half-precision floating point type along with corresponding arithmetic
operators, type conversions and common mathematical functions. It aims
for both efficiency and ease of use, trying to accurately mimic the
behaviour of the builtin floating point types at the best performance
possible. It automatically uses and provides C++11 features when
possible, but stays completely C++98-compatible when neccessary.

%package devel
Summary:        A C++ half-precision floating point type
Provides:       %{name}-static = %{version}-%{release}

%description devel
This is a C++ header-only library to provide an IEEE-754 conformant
half-precision floating point type along with corresponding arithmetic
operators, type conversions and common mathematical functions. It aims
for both efficiency and ease of use, trying to accurately mimic the
behaviour of the builtin floating point types at the best performance
possible. It automatically uses and provides C++11 features when
possible, but stays completely C++98-compatible when neccessary.

%prep
rm -rf %{name}-%{version}
unzip -d %{name}-%{version} %{SOURCE0}
cd %{name}-%{version}
# change dos endings to unix
sed -i "s|\r||g" include/half.hpp
sed -i "s|\r||g" LICENSE.txt
sed -i "s|\r||g" README.txt

%install
cd %{name}-%{version}
mkdir -p %{buildroot}%{_includedir}
install -m 644 include/half.hpp %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE.txt %{buildroot}%{_docdir}/%{name}/
install -m 644 README.txt %{buildroot}%{_docdir}/%{name}/

%files devel
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.txt
%license %{_docdir}/%{name}/LICENSE.txt
%{_includedir}/half.hpp

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 2 2024 Tom Rix <Tom.Rix@amd.com> - 2.2.0-6
- Fix docdir dir ownship

* Mon Dec 2 2024 Tom Rix <Tom.Rix@amd.com> - 2.2.0-5
- TW needs to explicitly BuildRequires unzip

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 9 2023 Tom Rix <trix@redhat.com> - 2.2.0-1
- Initial package
