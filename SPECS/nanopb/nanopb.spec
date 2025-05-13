%bcond_without check

%global forgeurl https://github.com/nanopb/nanopb
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Version:        0.4.9
%global tag %{version}
%forgemeta

Name:           nanopb
Release:        2%{?dist}
Summary:        A small code-size Protocol Buffers implementation in ansi C
License:        Zlib
URL:            https://jpa.kapsi.fi/nanopb/
Source0:        %{forgesource}

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  protobuf-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-poetry
BuildRequires:  pkgconfig
# for testing
%if %{with check}
BuildRequires:  scons
%endif

%description
Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is
especially suitable for use in microcontrollers, but fits any memory restricted
system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        python3
Summary:        Small code-size Protocol Buffers implementation in Python
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    python3
The %{name}-python3 package contains Small code-size Protocol Buffers
implementation in Python. It includes the protoc-based generator, which converts
.proto files to .pb.h files for inclusion in a project.

%prep
%forgeautosetup -p1

# remove unneeded files
rm generator/{nanopb_generator.py2,protoc-gen-nanopb-py2}
rm generator/*.bat

# https://github.com/nanopb/nanopb/blob/master/extra/poetry/poetry_build.sh
cp extra/poetry/pyproject.toml .
mkdir -p nanopb
cp -r generator nanopb
touch nanopb/__init__.py nanopb/generator/__init__.py
make -C nanopb/generator/proto

%generate_buildrequires
%pyproject_buildrequires

%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_STATIC_LIBS=OFF \
    -Dnanopb_BUILD_GENERATOR=OFF \
    -Dnanopb_BUILD_PKGCONFIG=ON

%cmake_build

%pyproject_wheel

%install
%cmake_install

%pyproject_install
%pyproject_save_files nanopb

%if %{with check}
%check
pushd tests
    scons
popd
%endif

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/libprotobuf-nanopb.so.0

%files devel
%{_libdir}/libprotobuf-nanopb.so
%{_includedir}/nanopb/
%dir %{_libdir}/cmake/nanopb
%{_libdir}/cmake/nanopb/*.cmake

%files python3 -f %{pyproject_files}
%{_bindir}/nanopb_generator
%{_bindir}/protoc-gen-nanopb

%changelog
* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Packit <hello@packit.dev> - 0.4.9-1
- Update to 0.4.9 upstream release
- Resolves: rhbz#2313698

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.4.8-4
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Nov 18 2023 topazus <topazus@outlook.com> - 0.4.8-1
- update to 0.4.8

* Tue Oct 24 2023 topazus <topazus@outlook.com> - 0.4.7-4
- remove python2 related files

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Python Maint <python-maint@redhat.com> - 0.4.7-2
- Rebuilt for Python 3.12

* Sun Jun 25 2023 topazus <topazus@outlook.com> - 0.4.7-1
- initial import; rhbz#2216595
