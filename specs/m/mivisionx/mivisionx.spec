# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname MIVisionX
%global rocm_release 6.4
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//' )

# For testing
# Use the VX conformace tests, openvx_1.3 branch
# https://github.com/KhronosGroup/OpenVX-cts
# Results on gfx1103
#
# [ ALL DONE ] 5820 test(s) from 69 test case(s) ran
# [ PASSED   ] 5817 test(s)
# [ FAILED   ] 3 test(s), listed below:
# [ FAILED   ] SmokeTestBase.vxReleaseReferenceBase
# [ FAILED   ] SmokeTestBase.vxLoadKernels
# [ FAILED   ] SmokeTestBase.vxUnloadKernels
# [ DISABLED ] 8190 test(s)

Name:           mivisionx
Version:        %{rocm_version}
Release: 5%{?dist}
Summary:        AMD's computer vision toolkit
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT AND Apache-2.0 AND MIT-Khronos-old AND GPL-3.0-or-later
# MIT is the main license
# Apache-2.0 is used for the includes
#  amd_openvx/openvx/include/VX/vx*.h
# MIT-Khronos-old covers a couple of files
#  amd_openvx/openvx/api/vx_nodes.cpp
#  amd_openvx/openvx/api/vxu.cpp
# GPL 3 or later for a couple of files
#  apps/cloud_inference/client_app/qcustomplot.*

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?fedora} || 0%{?suse_version}
BuildRequires:  fdupes
%endif
BuildRequires:  half-devel
BuildRequires:  hipcc
# Problem with ffmpeg
# /MIVisionX-rocm-6.3.1/amd_openvx_extensions/amd_media/kernels.cpp:98:5: error: use of undeclared identifier 'av_register_all'
#   98 |     av_register_all();
#      |     ^
# BuildRequires:  ffmpeg-free-devel
BuildRequires:  libavcodec-free-devel
BuildRequires:  libavformat-free-devel
%if 0%{?fedora}
BuildRequires:  mesa-va-drivers
%endif
BuildRequires:  miopen-devel
BuildRequires:  opencv-devel
BuildRequires:  rocblas-devel
BuildRequires:  rocm-cmake
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-omp-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpp-devel
BuildRequires:  rocm-runtime-devel

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
MIVisionX toolkit is a set of comprehensive computer vision
and machine intelligence libraries, utilities, and applications
bundled into a single toolkit. AMD MIVisionX delivers highly
optimized conformant open-source implementation of the Khronos
OpenVX™ and OpenVX™ Extensions along with Convolution Neural
Net Model Compiler & Optimizer supporting ONNX, and Khronos
NNEF™ exchange formats. The toolkit allows for rapid prototyping
and deployment of optimized computer vision and machine learning
inference workloads on a wide range of computer hardware,
including small embedded x86 CPUs, APUs, discrete GPUs, and
heterogeneous servers.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# Remove some cruft
find . -type f -name '.gitignore' -delete
find . -type f -name '.DS_Store' -delete

# #include <half/half.hpp> -> <half.hpp>
for f in `find . -type f -name '*.hpp' -o -name '*.h' -o -name '*.cpp' `; do
    sed -i -e 's@#include <half/half.hpp>@#include <half.hpp>@' $f
done

# Fixup default ROCM_PATH
sed -i -e 's@/opt/rocm@%{_prefix}@' CMakeLists.txt

%build

%cmake \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/clang++ \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DMIGRAPHX=OFF \
    -DNEURAL_NET=OFF \
    -DHIP_PLATFORM=amd

%cmake_build

%install
%cmake_install

#Clean up dupes:
%if 0%{?fedora} || 0%{?suse_version}
%fdupes %{buildroot}%{_prefix}
%endif

# ERROR   0020: file '/usr/lib64/libvx_amd_custom.so.1.0.1' contains a runpath referencing '..' of an absolute path [:/usr/lib64/rocm/llvm/bin/../lib]
chrpath -r %{rocmllvm_libdir} %{buildroot}%{_libdir}/libvx_amd_custom.so.1.*.*

if [ -f %{buildroot}%{_prefix}/share/doc/%{name}/LICENSE.txt ]; then
    rm %{buildroot}%{_prefix}/share/doc/%{name}/LICENSE.txt
fi
if [ -f %{buildroot}%{_prefix}/share/doc/%{name}-asan/LICENSE.txt ]; then
    rm %{buildroot}%{_prefix}/share/doc/%{name}-asan/LICENSE.txt
fi
rm -rf %{buildroot}%{_datadir}/%{name}/apps
rm -rf %{buildroot}%{_datadir}/%{name}/samples
rm -rf %{buildroot}%{_datadir}/%{name}/test


%files
%license LICENSE.txt
%{_bindir}/runvx
%{_libdir}/libopenvx.so.1{,.*}
%{_libdir}/libvx_amd_custom.so.1{,.*}
%{_libdir}/libvx_opencv.so.1{,.*}
%{_libdir}/libvx_rpp.so.1{,.*}
%{_libdir}/libvxu.so.1{,.*}

%files devel
%doc README.md
%{_datadir}/%{name}/
%{_includedir}/%{name}/
%{_libdir}/libopenvx.so
%{_libdir}/libvx_amd_custom.so
%{_libdir}/libvx_opencv.so
%{_libdir}/libvx_rpp.so
%{_libdir}/libvxu.so

%changelog
* Mon Aug 11 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- mesa-va-drivers are not on RHEL

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Remove -mtls-dialect cflag

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Apr 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Sat Feb 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-1
- Initial package

