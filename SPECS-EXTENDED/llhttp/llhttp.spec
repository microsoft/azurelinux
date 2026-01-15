# This package is rather exotic. The compiled library is a typical shared
# library with a C API. However, it has only a tiny bit of C source code. Most
# of the library is written in TypeScript, which is transpiled to C, via LLVM
# IR, using llparse (https://github.com/nodejs/llparse)—all of which happens
# within the NodeJS ecosystem.
#
# Historically, this package “built like” a NodeJS package, with a
# dev-dependency bundle from NPM that we used to transpile the original
# TypeScript sources to C downstream. Since 9.3.0, it is no longer practical to
# re-generate the C sources from Typescript without using pre-compiled esbuild
# executables from NPM, so we use the upstream “release” tarball with
# pre-generated C source and header files included.
#
# That allows this package to be built without running the NodeJS/Typescript
# machinery in the build (via a large “dev” dependency bundle. However, this
# release archive lacks the original TypeScript source code for the generated C
# code, so we need to include this in an additional source. For details, see:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/what-can-be-packaged/#pregenerated-code

# This package is a dependency of libgit2 which in turn is one of rpmautospec.
# When upgrading to a version with a new soname, this package needs to provide
# both in order to bootstrap itself and libgit2. Set %%bootstrap and
# %%previous_so_version for this (and unset and rebuild later).
#
%bcond  bootstrap 0
%global so_version 9.3
%global previous_so_version 9.2

Name:           llhttp
Version:        9.3.0
Release:        6%{?dist}
Summary:        Port of http_parser to llparse
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# SPDX
License:        MIT
URL:            https://github.com/nodejs/llhttp
Source0:        %{url}/archive/refs/tags/release/v%{version}/llhttp-release-v%{version}.tar.gz
# Contains the original TypeScript sources, which we must include in the source
# RPM per packaging guidelines.
Source1:        %{url}/archive/v%{version}/llhttp-%{version}.tar.gz

# For compiling the C library
BuildRequires:  cmake
BuildRequires:  gcc
# There is no C++ involved, but CMake searches for a C++ compiler.
BuildRequires:  gcc-c++

%if %{with bootstrap}
%if "%{_lib}" == "lib64"
BuildRequires:  libllhttp.so.%{previous_so_version}()(64bit)
%else
BuildRequires:  libllhttp.so.%{previous_so_version}
%endif
%endif

%description
This project is a port of http_parser to TypeScript. llparse is used to
generate the output C source file, which could be compiled and linked with the
embedder's program (like Node.js).

%package devel
Summary:        Development files for llhttp
Requires:       llhttp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The llhttp-devel package contains libraries and header files for
developing applications that use llhttp.

%prep
%autosetup -n llhttp-release-v%{version}

%conf
%cmake

%build
%cmake_build

%install
%cmake_install

%if %{with bootstrap}
cp -vp %{_libdir}/libllhttp.so.%{previous_so_version}{,.*} \
    %{buildroot}%{_libdir}
%endif

# The same obstacles that prevent us from re-generating the C sources from
# TypeScript also prevent us from running the tests, which rely on NodeJS.

%files
# Files LICENSE and LICENSE-MIT are duplicates.
%license LICENSE
%doc README.md
%{_libdir}/libllhttp.so.%{so_version}{,.*}
%if %{with bootstrap}
%{_libdir}/libllhttp.so.%{previous_so_version}{,.*}
%endif

%files devel
%{_includedir}/llhttp.h
%{_libdir}/libllhttp.so
%{_libdir}/pkgconfig/libllhttp.pc
%{_libdir}/cmake/llhttp/

%changelog
* Tue Dec 23 2025 Aditya Singh <v-aditysing@microsoft.com> - 9.3.0-6
- Initial Azure Linux import from Fedora 44 (license: MIT).
- License verified.

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 9.3.0-4
- Non-bootstrap build

* Mon May 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 9.3.0-3
- Minor style tweaks to bootstrapping machinery

* Mon May 19 2025 Nils Philippsen <nils@redhat.com> - 9.3.0-2
- Make package bootstrappable for rpmautospec

* Sun May 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 9.3.0-1
- Update to 9.3.0 (close RHBZ#2363919)

* Tue Apr 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 9.2.1-6
- Correct a term in the SourceLicense

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.2.1-4
- Omit build-time license auditing on i686
- This keeps llhttp from blocking licensecheck’s dependencies or askalono-
  cli from dropping i686 support.

* Fri Dec 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.2.1-3
- Add a SourceLicense field
- Re-generate the dev-dependencies bundle

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.2.1-1
- Update to 9.2.1 (close RHBZ#2273352, fix CVE-2024-27982)
- Switch from xz to zstd compression for the “dev” bundle archive

* Thu Mar 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.2.0-4
- Format check-null-licenses with “ruff format”

* Wed Feb 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.2.0-1
- Update to 9.2.0 (close RHBZ#2263250)

* Wed Feb 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1.3-6
- Compress the dev dependency bundle with xz instead of gzip

* Sun Feb 11 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 9.1.3-5
- Avoid licensecheck dependency in RHEL builds

* Thu Feb 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1.3-4
- Better audit (and document auditing of) dev dependency licenses

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1.3-1
- Update to 9.1.3 (close RHBZ#2242220)

* Tue Oct 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1.2-1
- Update to 9.1.2

* Thu Sep 14 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1.1-1
- Update to 9.1.1

* Thu Sep 14 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 9.1.0-1
- Update to 9.1.0

* Mon Aug 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 9.0.1-1
- Update to 9.0.1 (close RHBZ#2228290)

* Tue Aug 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 9.0.0-1
- Update to 9.0.0

* Sat Jul 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 8.1.1-1
- Update to 8.1.1 (close RHBZ#2216591)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 8.1.0-5
- Remove explicit %%set_build_flags, not needed since F36

* Wed Feb 15 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 8.1.0-4
- Fix test compiling/execution

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 8.1.0-2
- Indicate dirs. in files list with trailing slashes

* Sat Oct 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 8.1.0-1
- Update to 8.1.0 (close RHBZ#2131175)

* Sat Oct 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 8.0.0-1
- Update to 8.0.0 (close RHBZ#2131175)

* Sat Oct 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.10-2
- Drop workarounds for Python 3.10 and older

* Thu Sep 29 2022 Stephen Gallagher <sgallagh@redhat.com> - 6.0.10-1
- Update to v6.0.10

* Thu Aug 25 2022 Miro Hrončok <miro@hroncok.cz> - 6.0.9-2
- Use tomllib/python-tomli instead of dead upstream python-toml

* Thu Aug 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.9-1
- Update to 6.0.9 (close RHBZ#2116231)
- Bumped .so version from downstream 0.1 to upstream 6.0
- Better upstream support for building and installing a shared library
- The -devel package now contains a .pc file
- Tests are now built with gcc and fully respect distro flags

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.6-7
- Drop “forge” macros, which aren’t really doing much here

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.6-5
- Add a note about LLHTTP_STRICT_MODE to the package description

* Fri Dec 24 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.6-4
- Revert "Build with LLHTTP_STRICT_MODE enabled"

* Wed Dec 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.6-3
- Build with LLHTTP_STRICT_MODE enabled

* Tue Dec 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.6-2
- Dep. on cmake-filesystem is now auto-generated

* Mon Dec 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 6.0.6-1
- Initial package (close RHBZ#2029461)
## END: Generated by rpmautospec
