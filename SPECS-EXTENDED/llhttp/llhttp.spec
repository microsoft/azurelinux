# This package is rather exotic. The compiled library is a typical shared
# library with a C API. However, it has only a tiny bit of C source code. Most
# of the library is written in TypeScript, which is transpiled to C, via LLVM
# IR, using llparse (https://github.com/nodejs/llparse)—all of which happens
# within the NodeJS ecosystem.
#
# The package therefore “builds like” a NodeJS package, and to the extent they
# are relevant we apply the NodeJS packaging guidelines. However, the result of
# the build “installs like” a traditional C library package and has no NodeJS
# dependencies, including bundled ones.
#
# Furthermore, the package is registered with npm as “llhttp”, but current
# releases are not published there, so we use the GitHub archive as the
# canonical source and use a custom bundler script based on
# nodejs-packaging-bundler to fetch NodeJS build dependencies.
#
# Overall, we cherry-pick from the standard and NodeJS packaging guidelines as
# each seems to best apply, understanding that this package does not fit well
# into any of the usual patterns or templates.
#
# Note that there is now a “release” tarball, e.g.
# https://github.com/nodejs/llhttp/archive/refs/tags/release/v%%{version}tar.gz,
# that allows this package to be built without the NodeJS/TypeScript machinery.
# However, the release archive lacks the original TypeScript source code for
# the generated C code, which we would need to include in the source RPM as an
# additional source even if we do not do the re-generation ourselves.

Name:           llhttp
Version:        9.2.1
%global so_version 9.2
Release:        3%{?dist}
Summary:        Port of http_parser to llparse
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# License of llhttp is (SPDX) MIT; nothing from the NodeJS dependency bundle is
# installed, so its contents do not contribute to the license of the binary
# RPMs, and we do not need a file llhttp-%%{version}-bundled-licenses.txt.
License:        MIT
URL:            https://github.com/nodejs/llhttp
Source0:        %{url}/archive/v%{version}/llhttp-%{version}.tar.gz

# Based closely on nodejs-packaging-bundler, except:
#
# - The GitHub source tarball specified in this spec file is used since the
#   current version is not typically published on npm
# - No production dependency bundle is generated, since none is needed—and
#   therefore, no bundled licenses text file is generated either
Source1:        llhttp-packaging-bundler
# Created with llhttp-packaging-bundler (Source1):
Source2:        llhttp-%{version}-nm-dev.tar.zst

# While nothing in the dev bundle is installed, we still choose to audit for
# null licenses at build time and to keep manually-approved exceptions in a
# file.
Source3:        check-null-licenses
Source4:        audited-null-licenses.toml

# The compiled RPM does not depend on NodeJS at all, but we cannot *build* it
# on architectures without NodeJS.
ExclusiveArch:  %{nodejs_arches}

# For generating the C source “release” from TypeScript:
BuildRequires:  nodejs-devel
BuildRequires:  make

# For compiling the C library
BuildRequires:  cmake
BuildRequires:  gcc

# For tests
BuildRequires:  gcc-c++

# For check-null-licenses
BuildRequires:  python3-devel

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
%autosetup

# Remove build flags specifying ISA extensions not in the architectural
# baseline from the test fixture setup.
sed -r -i 's@([[:blank:]]*)(.*-m(sse4))@\1// \2@' test/fixtures/index.ts

# We build the library that we install via release/CMakeLists.txt, but the
# tests are built via Makefile targets. Don’t apply non-default optimization or
# debug flags to the test executables.
sed -r -i 's@ -[Og].\b@@g' Makefile

# Set up bundled (dev) node modules required to generate the C sources from the
# TypeScript sources.
tar --zstd --extract --file='%{SOURCE2}'
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_dev/* .
ln -s ../node_modules_dev/.bin .
popd

# We run ts-node out of node_modules/.bin rather than using npx (which we will
# not have available).
sed -r -i 's@\bnpx[[:blank:]](ts-node)\b@node_modules/.bin/\1@' Makefile


%build
# Generate the C source “release” from TypeScript using the “node_modules_dev”
# bundle.
%make_build release RELEASE='%{version}'

# To help prove that nothing from the bundled NodeJS dev dependencies is
# included in the binary packages, remove the “node_modules” symlinks.
rm -rvf node_modules

cd release
%cmake
%cmake_build


%install
cd release
%cmake_install


%check
# Symlink the NodeJS bundle again so that we can test with Mocha
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_dev/* .
ln -s ../node_modules_dev/.bin .
popd

# Verify that no bundled dev dependency has a null license field, unless we
# already audited it by hand. This reduces the chance of accidentally including
# code with license problems in the source RPM.
%{python3} '%{SOURCE3}' --exceptions '%{SOURCE4}' --with dev node_modules_dev

%if !0%{?rhel}
# Ensure we have checked all of the licenses in the dev dependency bundle for
# allowability.
pattern="${pattern-}${pattern+|}UNKNOWN|(Apache|Python) License 2\\.0"
pattern="${pattern-}${pattern+|}(MIT|ISC|BSD [023]-Clause) License"
pattern="${pattern-}${pattern+|}BSD 2-Clause with views sentence"
pattern="${pattern-}${pattern+|}MIT License and/or X11 License"
pattern="${pattern-}${pattern+|}GNU General Public License"
# The CC0-1.0 license is *not allowed* in Fedora for code, but the
# binary-search dev dependency falls under the following blanket exception:
#
#   Existing uses of CC0-1.0 on code files in Fedora packages prior to
#   2022-08-01, and subsequent upstream versions of those files in those
#   packages, continue to be allowed. We encourage Fedora package maintainers
#   to ask upstreams to relicense such files.
#
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/91#note_1151947383
#
# This can be verified by checking out commit
# f460573ec4dc41968e600a96aaaf03a167b236bf (2021-12-16) from dist-git for this
# package, obtaining the source llhttp-6.0.6-nm-dev.tgz, and observing that
# llhttp-6.0.6/node_modules_dev/binary-search/package.json shows the CC0-1.0
# license.
pattern="${pattern-}${pattern+|}binary-search/package.json: (\*No copyright\* )?Creative Commons CC0 1\.0"
# The license BSD-3-Clause-Clear appears in sprintf-js/bower.json. This license
# is on the not-allowed list, but it is not real: sprintf-js/package.json and
# sprintf-js/LICENSE have the correct (and allowed) BSD-3-Clause license, and
# upstream confirmed in “Licensing Question”
# https://github.com/alexei/sprintf.js/issues/211 that the appearance of
# BSD-3-Clause-Clear in this file was a mere typo.
pattern="${pattern-}${pattern+|}sprintf-js/bower.json: (\*No copyright\* )?BSD 3-Clause Clear License"

if licensecheck -r node_modules_dev |
    grep -vE "(${pattern})( \\[generated file\\])?\$" ||
  ! askalono crawl node_modules_dev | awk '
      $1 == "License:" { license = $0; next }
      $1 == "Score:" {
        if ( \
          license ~ /: (MIT|ISC) \(/ || \
          license ~ /: (0BSD|BSD-2-Clause(-Views)?|BSD-3-Clause) \(/ || \
          license ~ /: (Apache-2\.0|Python-2\.0\.1) \(/ \
        ) {
          next # license is OK
        }
        # license needs auditing
        problem = 1
        print file; print license; print $0
        next
      }
      { file = $0 }
      END { exit problem }'

then
  cat 1>&2 <<'EOF'
=================================================================
Possible new license(s) found in dev dependency bundle!

While these do not contribute to License, they must appear in:
https://docs.fedoraproject.org/en-US/legal/allowed-licenses/

Please audit them and modify the patterns representing expected
licenses in the spec file!
=================================================================
EOF
  exit 1
fi
%endif

# http-loose-request.c:7205:20: error: invalid conversion from 'void*' to
#     'const unsigned char*' [-fpermissive]
#  7205 |     start = state->_span_pos0;
#       |             ~~~~~~~^~~~~~~~~~
#       |                    |
#       |                    void*
export CXXFLAGS="${CXXFLAGS-} -fpermissive"
export CFLAGS="${CFLAGS-} -fpermissive"
export CLANG=gcc
# See scripts.test in package.json:


%files
%license release/LICENSE-MIT
%{_libdir}/libllhttp.so.%{so_version}{,.*}


%files devel
%doc release/README.md
%{_includedir}/llhttp.h
%{_libdir}/libllhttp.so
%{_libdir}/pkgconfig/libllhttp.pc
%{_libdir}/cmake/llhttp/


%changelog
* Mon May 12 2025 Archana Shettigar <v-shettigara@microsoft.com> - 9.2.1-3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

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
