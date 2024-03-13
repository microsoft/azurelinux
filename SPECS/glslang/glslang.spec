%global sdkver 1.3.275.0

Name:           glslang
Version:        14.0.0
Release:        1%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator

License:        BSD and GPLv3+ and Apache-2.0
URL:            https://github.com/KhronosGroup/%{name}
Source0:        %url/archive/vulkan-sdk-%{sdkver}.tar.gz#/%{name}-sdk-%{sdkver}.tar.gz
# Patch to build against system spirv-tools (rebased locally)
#Patch3:         https://patch-diff.githubusercontent.com/raw/KhronosGroup/glslang/pull/1722.patch#/0001-pkg-config-compatibility.patch
Patch3:         0001-pkg-config-compatibility.patch

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  spirv-tools-devel

%description
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1 -n %{name}-vulkan-sdk-%{sdkver}
# Fix rpmlint warning on debuginfo
find . -name '*.h' -or -name '*.cpp' -or -name '*.hpp'| xargs chmod a-x

%build
%cmake3 -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%{cmake_install}

# we don't want them in here
rm -rf %{buildroot}%{_includedir}/SPIRV

%ifnarch s390x ppc64
%check
pushd Test
./runtests localResults ../%{_vpath_builddir}/StandAlone/glslangValidator ../%{_vpath_builddir}/StandAlone/spirv-remap
popd
%endif

%files
%doc README.md README-spirv-remap.txt
%{_bindir}/glslang
%{_bindir}/glslangValidator
%{_bindir}/spirv-remap
%{_libdir}/libglslang-default-resource-limits.so
%{_libdir}/libglslang-default-resource-limits.so.14
%{_libdir}/libglslang-default-resource-limits.so.14.0.0
%{_libdir}/libglslang.so
%{_libdir}/libglslang.so.14
%{_libdir}/libglslang.so.14.0.0
%{_libdir}/libSPIRV.so
%{_libdir}/libSPIRV.so.14
%{_libdir}/libSPIRV.so.14.0.0
%{_libdir}/libSPVRemapper.so
%{_libdir}/libSPVRemapper.so.14
%{_libdir}/libSPVRemapper.so.14.0.0

%files devel
%{_includedir}/glslang/
%{_libdir}/pkgconfig/spirv.pc
%{_libdir}/cmake/*

%changelog
* Thu Feb 29 2024 Vince Perri <viperri@microsoft.com> - 14.0.0-1
- Initial Azure Linux import from Fedora 40 (license: MIT).
- License verified.
