Summary:        Feature-rich header-only C++ testing framework
Name:           doctest
Version:        2.4.10
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/doctest/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
%global debug_package %{nil}
BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  git
%undefine __cmake3_in_source_build

%description
A fast (both in compile times and runtime) C++ testing framework, with the
ability to write tests directly along production source (or in their own
source, if you prefer).

%package devel
Summary:        Development files for %{name}
Requires:       libstdc++-devel%{?_isa}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1

%build
%{cmake3} \
  -DCMAKE_BUILD_TYPE=Release \
  -DDOCTEST_WITH_MAIN_IN_STATIC_LIB:BOOL=OFF \
  -DDOCTEST_WITH_TESTS:BOOL=ON \
  %{nil}
%{cmake3_build}

%check
%{ctest3}

%install
%{cmake3_install}

%files devel
%doc README.md CHANGELOG.md CONTRIBUTING.md
%license LICENSE.txt
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/

%changelog
* Fri Mar 10 2023 nick black <niblack@microsoft.com> - 2.4.10-1
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- Verified license
