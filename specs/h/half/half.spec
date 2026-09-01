# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Copyright Fedora Project Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

# there is no debug package
%global debug_package %{nil}

Name:           half
Version:        2.2.0
Release:        10%{?dist}
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
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 2.2.0-9
- Add Fedora copyright

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
