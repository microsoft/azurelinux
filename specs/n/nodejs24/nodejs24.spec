## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This should be moved to rpm-redhat-config or similar as soon as feasible
# NOTE: %%SOURCE macros are not yet defined, so explicit path is needed
%{load:%{_sourcedir}/nodejs.srpm.macros}

# === Versions of any software shipped in the main nodejs tarball
%nodejs_define_version node 1:24.13.1-%{autorelease} -p

# Special release for sub-packages with their own version string.
# The complex release string ensures that the subpackage release is always increasing,
# even in the event that the main package version changes
# while the sub-package version stays the same.
%global nodejs_subpackage_release %{node_epoch}.%{node_version}.%{node_release}

# The following ones are generated via script;
# expect anything between the markers to be overwritten on any update.

# BEGIN automatic-version-macros  # DO NOT REMOVE THIS LINE!
# Version from node-v24.13.1/src/node_version.h
%global node_soversion 137

# Version from node-v24.13.1/deps/ada/ada.h
%nodejs_define_version ada 3.4.2
# Version from node-v24.13.1/deps/brotli/c/common/version.h
%nodejs_define_version brotli 1.2.0
# Version from node-v24.13.1/deps/cares/include/ares_version.h
%nodejs_define_version c_ares 1.34.6
# Version from node-v24.13.1/deps/histogram/include/hdr/hdr_histogram_version.h
%nodejs_define_version histogram 0.11.9
# Version from node-v24.13.1/tools/icu/current_ver.dep
%nodejs_define_version icu 78.2 -p
# Version from node-v24.13.1/deps/uv/include/uv/version.h
%nodejs_define_version libuv 1.51.0
# Version from node-v24.13.1/deps/llhttp/include/llhttp.h
%nodejs_define_version llhttp 9.3.0
# Version from node-v24.13.1/deps/nghttp2/lib/includes/nghttp2/nghttp2ver.h
%nodejs_define_version nghttp2 1.68.0
# Version from node-v24.13.1/deps/ngtcp2/nghttp3/lib/includes/nghttp3/version.h
%nodejs_define_version nghttp3 1.6.0
# Version from node-v24.13.1/deps/ngtcp2/ngtcp2/lib/includes/ngtcp2/version.h
%nodejs_define_version ngtcp2 1.11.0
# Version from node-v24.13.1/deps/cjs-module-lexer/src/package.json
%nodejs_define_version nodejs-cjs-module-lexer 2.2.0
# Version from node-v24.13.1/lib/punycode.js
%nodejs_define_version nodejs-punycode 2.1.0
# Version from node-v24.13.1/deps/undici/src/package.json
%nodejs_define_version nodejs-undici 7.18.2
# Version from node-v24.13.1/deps/npm/package.json
%nodejs_define_version npm 1:11.8.0-%{nodejs_subpackage_release}
# Version from node-v24.13.1/deps/sqlite/sqlite3.h
%nodejs_define_version sqlite 3.51.2
# Version from node-v24.13.1/deps/uvwasi/include/uvwasi.h
%nodejs_define_version uvwasi 0.0.23
# Version from node-v24.13.1/deps/v8/include/v8-version.h
%nodejs_define_version v8 3:13.6.233.17-%{nodejs_subpackage_release} -p
# Version from node-v24.13.1/deps/zlib/zlib.h
%nodejs_define_version zlib 1.3.1
# END automatic-version-macros  # DO NOT REMOVE THIS LINE!

# === Conditional build – global options
# Use all vendored dependencies when bootstrapping
%bcond all_deps_bundled %{with bootstrap}

# === Distro-wide build configuration adjustments ===
# v8 cannot be built with LTO enabled;
# the rest of the build should be LTO enabled via the configure script
%global _lto_cflags %{nil}

# === Additional definitions ===
# Architecture-dependent suffix for requiring/providing .so names
%if 0%{?__isa_bits} == 64
%global _so_arch_suffix ()(64bit)
%endif
# place for data files
%global nodejs_datadir  %{_datarootdir}/node-%{node_version_major}
# place for (npm) packages used by multiple streams and/or that are stream-agnostic (do not care)
%global nodejs_common_sitelib %{_prefix}/lib/node_modules
# place for (npm) packages specific to this stream
%global nodejs_private_sitelib %{_prefix}/lib/node_modules_%{node_version_major}

Name:           nodejs%{node_version_major}
Epoch:          %{node_epoch}
Version:        %{node_version}
Release:        %{node_release}

Summary:        JavaScript runtime
License:        Apache-2.0 AND Artistic-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BlueOak-1.0.0 AND CC-BY-3.0 AND CC0-1.0 AND ISC AND MIT
URL:            https://nodejs.org

ExclusiveArch:  %{nodejs_arches}
# v8 does not build on i686 any more
ExcludeArch:    %{ix86}

# SPEC tools – additiona macros, dependency generators, and utilities
BuildRequires:  chrpath
BuildRequires:  git-core
BuildRequires:  jq
BuildRequires:  nodejs-packaging
# Build system and supporting tools
BuildRequires:  gcc >= 10.0, gcc-c++ >= 10.0, pkgconf, ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  %{py3_dist setuptools jinja2}
# Additional libraries, either system or vendored ones
BuildRequires:  pkgconfig(openssl) >= 3.0.2
%nodejs_declare_bundled -a  ada
%nodejs_declare_bundled -a  brotli      -plibbrotlidec,libbrotlienc
%nodejs_declare_bundled -a  c-ares      -plibcares
%nodejs_declare_bundled -a  histogram
%nodejs_declare_bundled -a  icu
%nodejs_declare_bundled -a  libuv       -p
%nodejs_declare_bundled -a  llhttp
%nodejs_declare_bundled -a  nghttp2
%nodejs_declare_bundled -a  nghttp3
%nodejs_declare_bundled -a  ngtcp2
%nodejs_declare_bundled -a  nodejs-cjs-module-lexer
%nodejs_declare_bundled -a  nodejs-punycode -npunycode
%nodejs_declare_bundled -a  nodejs-undici
%nodejs_declare_bundled -a  sqlite      -psqlite3
%nodejs_declare_bundled -a  uvwasi
%nodejs_declare_bundled -a  v8
%nodejs_declare_bundled -a  zlib        -p
# Run-time dependencies of the main package
Requires:   ca-certificates
# Required and/or recommended sub-packages
Requires:   %{name}-libs%{?_isa}      = %{node_evr}
Recommends: %{name}-docs              = %{node_evr}
Recommends: %{name}-full-i18n%{?_isa} = %{node_evr}
Recommends: %{name}-npm              >= %{npm_evr}
# Virtual provides
Provides:   nodejs(abi) = %{node_soversion}, nodejs(abi%{node_version_major}) = %{node_soversion}
Provides:   nodejs(engine) = %{node_version}

# Main source tarball; see packaging/make-nodejs-tarball.sh on how it is created
Source:         node-v%{node_version}-stripped.tar.gz
# Sources 001-099: reserved for additional sources to be installed
# - Full ICU database data
Source001:      https://github.com/unicode-org/icu/releases/download/release-%{icu_version_major}.%{icu_version_minor}/icu4c-%{icu_version_major}.%{icu_version_minor}-data-bin-b.zip
Source002:      https://github.com/unicode-org/icu/releases/download/release-%{icu_version_major}.%{icu_version_minor}/icu4c-%{icu_version_major}.%{icu_version_minor}-data-bin-l.zip
# - Downstream/distribution configuration files
Source003:      nodejs.pc.in
Source004:      v8.pc.in
Source005:      npmrc.in
Source006:      nodejs_abi.attr.in
Source007:      nodejs_abi.req.in
# - Check section tests
Source010:      test-runner.sh
Source011:      test-should-pass.txt
Source020:      i18n-btest402.js
# Source 100+: Packaging support files that won't be installed
# - Packaging supports scripts and Makefile, used to semi-automate RPM updates. See the Makefile in the tarball on how this is created.
Source100:      packaging-scripts.tar.gz
# - Additional SRPM macros
Source101:      nodejs.srpm.macros

%patchlist
0001-Remove-unused-OpenSSL-config.patch
0005-v8-highway-Fix-for-GCC-15-compiler-error-on-PPC8-PPC.patch
0001-fips-disable-options.patch

%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

%package        devel
Summary:        JavaScript runtime – development headers
Requires:       nodejs%{node_version_major}%{?_isa} = %{node_evr}
Requires:       nodejs%{node_version_major}-libs%{?_isa} = %{node_evr}
Requires:       nodejs-packaging
Requires:       openssl-devel%{?_isa}
%{!?with_bundled_brotli:Requires: brotli-devel%{?_isa}}
%{!?with_bundled_libuv:Requires: libuv-devel%{?_isa}}
%{!?with_bundled_zlib:Requires: zlib-devel%{?_isa}}
# Note: -devel sub-packages of the various streams conflict with each other,
# as the headers cannot be easily namespaced (would break at lease node-gyp search path).
# Hence the Provides: in place of metapackage.
Provides:       nodejs-devel = %{node_evr}

Provides: alternative-for(nodejs-devel) = %{node_evr}
Conflicts: alternative-for(nodejs-devel)
Conflicts: nodejs-devel-pkg
 # previously VP used for the same reason as alternative-for() above


%description    devel
Development headers for the Node.js JavaScript runtime.

%package -n     v8-%{v8_version_major}.%{v8_version_minor}-devel
Summary:        v8 – development headers
Epoch:          %{v8_epoch}
Version:        %{v8_version}
Release:        %{v8_release}

Requires:       nodejs%{node_version_major}-devel%{?_isa} = %{node_evr}
Requires:       nodejs%{node_version_major}-libs%{?_isa}  = %{node_evr}
Provides:       v8-devel = %{v8_evr}
Obsoletes:      v8-devel <= 2:10.2.154, v8-314-devel <= 2:3.14

%description -n v8-%{v8_version_major}.%{v8_version_minor}-devel
Development headers for the v8 runtime.

%package        libs
Summary:        Node.js and v8 libraries
# v8 used to be a separate package; keep providing it virtually
Provides:       v8 = %{v8_evr}
Provides:       v8%{?_isa} = %{v8_evr}
Obsoletes:      v8 < 1:6.7.17-10
Provides:       libv8.so.%{v8_version_major}%{?_so_arch_suffix} = %{v8_epoch}:%{v8_version}
Provides:       libv8_libbase.so.%{v8_version_major}%{?_so_arch_suffix} = %{v8_epoch}:%{v8_version}
Provides:       libv8_libplatform.so.%{v8_version_major}%{?_so_arch_suffix} = %{v8_epoch}:%{v8_version}

%description    libs
Libraries to support Node.js and provide stable v8 interfaces.

%package        full-i18n
Summary:        Non-English locale data for Node.js
Requires:       nodejs%{node_version_major}%{?_isa} = %{node_evr}

%description    full-i18n
Optional data files to provide full ICU support for Node.js.
Remove this package to save space if non-English locales are not needed.

%package        docs
Summary:        Node.js API documentation
BuildArch:      noarch
Requires(meta): nodejs%{node_version_major} = %{node_evr}

%description    docs
The API documentation for the Node.js JavaScript runtime.

%package        npm
Summary:        Node.js Package Manager
Epoch:          %{npm_epoch}
Version:        %{npm_version}
Release:        %{npm_release}

BuildArch:      noarch
Requires:       nodejs%{node_version_major}         = %{node_evr}
Recommends:     nodejs%{node_version_major}-docs    = %{node_evr}
Provides:       npm(npm) = %{npm_version}

%description    npm
npm is a package manager for node.js. You can use it to install and publish
your node programs. It manages dependencies and does other cool stuff.


%prep
%autosetup -n node-v%{node_version} -S git_am
# clean the archive of the de-vendored dependencies, ensuring they are not used
readonly -a devendored_paths=(
    deps/v8/third_party/jinja2 tools/inspector_protocol/jinja2
    %{?!with_bundled_brotli:deps/brotli}
    %{?!with_bundled_c_ares:deps/cares}
    %{?!with_bundled_libuv:deps/uv}
    %{?!with_bundled_nodejs_cjs_module_lexer:deps/cjs-module-lexer}
    %{?!with_bundled_nodejs_undici:deps/undici}
    %{?!with_bundled_sqlite:deps/sqlite}
    %{?!with_bundled_zlib:deps/zlib}
)
rm -rf "${devendored_paths[@]}"

# use system python throughout the whole sources
readonly -a potential_python_scripts=(
    $(grep --recursive --files-with-matches --max-count=1 python)
)
%py3_shebang_fix "${potential_python_scripts[@]}"

%build
# additional build flags
readonly -a extra_cflags=(
    # Decrease debuginfo verbosity; otherwise,
    # the linker will run out of memory when linking v8
    -g1
    # For i686 compatibility, build with defines from libuv (rhbz#892601)
    -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64
    # Do not use OpenSSL Engine API (RHEL-33743)
    -DOPENSSL_NO_ENGINE
    # 2022-07-14: There's a bug in either torque or gcc that causes a
    # segmentation fault on ppc64le and s390x if compiled with -O2. Things
    # run fine on -O1 and -O3, so we'll just go with -O3 (like upstream)
    # while this gets sorted out.
    -O3
    # v8 segfaults when Identical Code Folding is enabled
    # - https://github.com/nodejs/node/issues/47865
    -fno-ipa-icf
)
# configuration flags
readonly -a configure_flags=(
    # Basic build options
    --verbose --ninja
    # Use FHS and build separate libnode.so
    --prefix=%{_prefix} --shared --libdir=%{_lib}
    # Use system OpenSSL
    --shared-openssl
    --openssl-is-fips
    --openssl-conf-name=openssl_conf
    --openssl-use-def-ca-store
    # Link with system libraries where appropriate
    %{?!with_bundled_brotli:--shared-brotli}
    %{?!with_bundled_c_ares:--shared-cares}
    %{?!with_bundled_libuv:--shared-libuv}
    %{?!with_bundled_sqlite:--shared-sqlite}
    %{?!with_bundled_zlib:--shared-zlib}
%if %{without bundled_nodejs_cjs_module_lexer}
    --shared-builtin-cjs_module_lexer/lexer-path=%{nodejs_common_sitelib}/cjs-module-lexer/lexer.js
    --shared-builtin-cjs_module_lexer/dist/lexer-path=%{nodejs_common_sitelib}/cjs-module-lexer/dist/lexer.js
%endif
%if %{without bundled_nodejs_undici}
    --shared-builtin-undici/undici-path=%{nodejs_common_sitelib}/undici/loader.js
%endif
    # Enable LTO where possible
    --enable-lto
    # Compile with small icu, extendable via full-i18n subpackage
    --with-intl=small-icu --with-icu-default-data-dir=%{nodejs_datadir}/icudata
    # Do not ship corepack
    --without-corepack
    # Use local headers for native addons when available
    --use-prefix-to-find-headers
)

export CFLAGS="${CFLAGS} ${extra_cflags[*]}" CXXFLAGS="${CXXFLAGS} ${extra_cflags[*]}"
%python3 configure.py "${configure_flags[@]}"
%ninja_build -C out/Release

%install
# Fill in values in configuration file templates
# usage: mkconfig [additional sed options] <template.in >config_file
mkconfig() {
    local -ra replace_opts=(
        -e 's;@INCLUDEDIR@;%{_includedir};g'
        -e 's;@LIBDIR@;%{_libdir};g'
        -e 's;@NODEJS_VERSION@;%{node_version};g'
        -e 's;@PREFIX@;%{_prefix};g'
        -e 's;@PYTHON3@;%{python3};g'
        -e 's;@SYSCONFDIR@;%{_sysconfdir};g'
        -e 's;@V8_VERSION@;%{v8_version};g'
    )

    sed --regexp-extended "${replace_opts[@]}" "$@"
}

# === Base installation
%{python3} tools/install.py install --dest-dir="${RPM_BUILD_ROOT}" --prefix="%{_prefix}"

# Correct the main binary permissions and remove RPATH
chmod 0755       "${RPM_BUILD_ROOT}%{_bindir}/node"
chrpath --delete "${RPM_BUILD_ROOT}%{_bindir}/node"

# Provide library symlinks
pushd "${RPM_BUILD_ROOT}%{_libdir}"
# - devel symlink for libnode.so
ln -srf libnode.so.%{node_soversion} libnode.so
# - compatibility symlinks for libv8
for soname in libv8{,_libbase,_libplatform}; do
    ln -srf libnode.so.%{node_soversion} "${soname}.so.%{v8_version_major}.%{v8_version_minor}"
    ln -srf libnode.so.%{node_soversion} "${soname}.so"
done
popd  # from ${RPM_BUILD_ROOT}%%{_libdir}

# Massage includedir
pushd "${RPM_BUILD_ROOT}%{_includedir}"
# - provide compatibility symlinks for libv8
for header in node/libplatform node/v8*.h node/cppgc; do
    ln -srf "${header}" "$(basename "${header}")"
done
# - config.gypi is platform-dependent and would conflict between arches
mv node/config.gypi node/config-%{_arch}.gypi
popd  # ${RPM_BUILD_ROOT}%%{_includedir}

# Install node-gyp configuration files
install -p -Dt "${RPM_BUILD_ROOT}%{nodejs_datadir}" common.gypi

# Create pkg-config files
readonly PKGCONFDIR="${RPM_BUILD_ROOT}%{_libdir}/pkgconfig"
mkdir -p "${PKGCONFDIR}"
mkconfig -e 's;@PKGCONFNAME@;nodejs-%{node_version_major};g' \
    <%{SOURCE3} >"${PKGCONFDIR}/nodejs-%{node_version_major}.pc"
mkconfig -e 's;@PKGCONFNAME@;v8-%{v8_version_major}.%{v8_version_minor};g' \
    <%{SOURCE4} >"${PKGCONFDIR}/v8-%{v8_version_major}.%{v8_version_minor}.pc"

# Create automatic RPM requires generator for this stream
mkdir -p "${RPM_BUILD_ROOT}%{_rpmconfigdir}/fileattrs"
sed -e 's;@NODEJS_VERSION_MAJOR@;%{node_version_major};g' \
    <%{SOURCE6} >"${RPM_BUILD_ROOT}%{_rpmconfigdir}/fileattrs/nodejs%{node_version_major}_abi.attr"
sed -e 's;@NODEJS_VERSION_MAJOR@;%{node_version_major};g' \
    <%{SOURCE7} >"${RPM_BUILD_ROOT}%{_rpmconfigdir}/nodejs%{node_version_major}_abi.req"

# Install documentation
mkdir -p "${RPM_BUILD_ROOT}%{_pkgdocdir}/html"
cp -pr doc/* "${RPM_BUILD_ROOT}%{_pkgdocdir}/html"
rm -f "${RPM_BUILD_ROOT}%{_pkgdocdir}/html/node.1"

# Some debugger support files from v8 are provided as documentation from upstream;
# move them to the correct directory (according to us).
pushd "${RPM_BUILD_ROOT}%{_defaultdocdir}"
mv -t "${RPM_BUILD_ROOT}%{_pkgdocdir}" node/gdbinit node/lldb_commands.py
popd  # from ${RPM_BUILD_ROOT}%%{_defaultdocdir}

# === Full ICU data installation
# Unzip the data themselves, and make the appropriate documentation available for %%doc
if test "$(%{python3} -Ic 'import sys; print(sys.byteorder)')" = "little"; then
readonly icu_source='%{SOURCE2}' icu_data_file='icudt%{icu_version_major}l.dat'
else
readonly icu_source='%{SOURCE1}' icu_data_file='icudt%{icu_version_major}b.dat'
fi
readonly icu_data_dir="${RPM_BUILD_ROOT}%{nodejs_datadir}/icudata"
readonly icu_doc_dir="full-icu"

unzip -od "${icu_data_dir}" "${icu_source}" "${icu_data_file}"
unzip -od "${icu_doc_dir}"  "${icu_source}" -x "${icu_data_file}"

# === NPM installation and tweaks
# Correct permissions in provided scripts
# - There are executable scripts for Windows PowerShell; RPM would try to pull it as a dependency
# - Not all executable bits should be removed; the -not -path lines are the ones that will be kept untouched
declare NPM_DIR="${RPM_BUILD_ROOT}%{nodejs_common_sitelib}/npm"
find "${NPM_DIR}" \
    -not -path "${NPM_DIR}/bin/*" \
    -not -path "${NPM_DIR}/node_modules/node-gyp/bin/node-gyp.js" \
    -not -path "${NPM_DIR}/node_modules/@npmcli/run-script/lib/node-gyp-bin/node-gyp" \
    -type f -executable \
    -execdir chmod -x '{}' +

# Remove (empty) project-specific .npmrc from npm itself,
# to avoid confusion with the distro-wide configuration below
rm -f "${NPM_DIR}/.npmrc"
# Create distribution-wide configuration file
mkconfig <%{SOURCE5} >"${NPM_DIR}/npmrc"

# Install HTML documentation to %%_pkgdocdir
mkdir -p "${RPM_BUILD_ROOT}%{_pkgdocdir}/npm/"
cp -prt  "${RPM_BUILD_ROOT}%{_pkgdocdir}/npm/" deps/npm/docs
# - replace the docs in $NPM_DIR with symlink to the doc dir
rm -rf  "${NPM_DIR}/docs"
ln -srf "${RPM_BUILD_ROOT}%{_pkgdocdir}/npm/docs" "${NPM_DIR}/docs"
# Install man pages to %%_mandir
mkdir -p "${RPM_BUILD_ROOT}%{_mandir}"
cp -prt  "${RPM_BUILD_ROOT}%{_mandir}" deps/npm/man/*
# – replace man pages in $NPM_DIR with symlinks to the man dir
rm -rf  "${NPM_DIR}/man"
ln -srf "${RPM_BUILD_ROOT}%{_mandir}" "${NPM_DIR}/man"

# === Adjustments to avoid conflict between parallel streams
# Note: some of the actions here make some of the previous ones redundant
# (for example, replacing a symlink made few lines above).
# This is by design; it should allow us to drop this entire section if we want
# to approach the problem in a different way
# (for example, backporting the changes to modular packages in EL9).

# Rename the main binary
readonly NODE_BIN='%{_bindir}/node-%{node_version_major}'
mv "${RPM_BUILD_ROOT}%{_bindir}/node" "${RPM_BUILD_ROOT}%{_bindir}/node-%{node_version_major}"

# Make the sitelib into a private one; but keep providing (empty) common one
mv "${RPM_BUILD_ROOT}%{nodejs_common_sitelib}" "${RPM_BUILD_ROOT}%{nodejs_private_sitelib}"
# 2025-05-20 FIXME: Turning a symlink into a directory needs to be coordinated across all the active streams.
# In order to not block this new packaging approach on the WASM unbundling effort,
# do not provide the common sitelib for now.
#mkdir "${RPM_BUILD_ROOT}%%{nodejs_common_sitelib}"
declare NPM_DIR="${RPM_BUILD_ROOT}%{nodejs_private_sitelib}/npm"

# Adjust npm scripts to use the renamed interpreter
readonly SHEBANG_ERE='^#!/usr/bin/(env\s+)?node\b'
readonly SHEBANG_FIX='#!%{_bindir}/node-%{node_version_major}'
readonly -a npm_bin_dirs=("${NPM_DIR}/bin" "${NPM_DIR}/node_modules")

find "${npm_bin_dirs[@]}" -type f \
| xargs grep --extended-regexp --files-with-matches "${SHEBANG_ERE}" \
| xargs sed --regexp-extended --in-place "s;${SHEBANG_ERE};${SHEBANG_FIX};"

# Fix shell scripts that call 'node' as command
readonly -a known_shell_scripts=(
    "${NPM_DIR}/bin/node-gyp-bin/node-gyp"
    "${NPM_DIR}/node_modules/@npmcli/run-script/lib/node-gyp-bin/node-gyp"
)
sed --regexp-extended --in-place 's;\bnode(\s);%{_bindir}/node-%{node_version_major}\1;' "${known_shell_scripts[@]}"

# Replace npm %%{_bindir} symlinks with properly versioned ones
# usage: relink_bin <basename> <source>
relink_bin() {
    local -r basename="${1?No link basename provided!}"
    local -r source="${2?No link source provided!}"

    ln -srf "${source}" "${RPM_BUILD_ROOT}%{_bindir}/${basename}-%{node_version_major}"
    rm -f   "${RPM_BUILD_ROOT}%{_bindir}/${basename}"
}
relink_bin npm "${NPM_DIR}/bin/npm-cli.js"
relink_bin npx "${NPM_DIR}/bin/npx-cli.js"

# Move manpages to versioned directories
readonly VERSIONED_MANDIR="${RPM_BUILD_ROOT}%{nodejs_datadir}/man"
mkdir -p "${VERSIONED_MANDIR}"
mv    -t "${VERSIONED_MANDIR}" "${RPM_BUILD_ROOT}%{_mandir}"/man?
# - compress the man-pages manually so that rpm will (re-)create valid symlinks
# FIXME: This should probably be replaced with ading /usr/share/node-*/man dir to /usr/lib/rpm/brp-compress
readonly MAN_INFO_COMPRESS="%{?_man_info_compress}%{!?_man_info_compress:gzip -9 -n}"
find "${VERSIONED_MANDIR}" -type f -name '*.[123456789]' -execdir ${MAN_INFO_COMPRESS} '{}' +
# – update npm man symlink
ln -srfn "${VERSIONED_MANDIR}" "${NPM_DIR}/man"
# - create symlinks for the versioned binaries
mkdir -p "${RPM_BUILD_ROOT}%{_mandir}/man1"
ln -srf  "${VERSIONED_MANDIR}/man1/node.1.gz" "${RPM_BUILD_ROOT}%{_mandir}/man1/node-%{node_version_major}.1.gz"
ln -srf  "${VERSIONED_MANDIR}/man1/npm.1.gz" "${RPM_BUILD_ROOT}%{_mandir}/man1/npm-%{node_version_major}.1.gz"
ln -srf  "${VERSIONED_MANDIR}/man1/npx.1.gz" "${RPM_BUILD_ROOT}%{_mandir}/man1/npx-%{node_version_major}.1.gz"


%check
# === Common test environment
export LD_LIBRARY_PATH="${RPM_BUILD_ROOT}%{_libdir}:${LD_LIBRARY_PATH}"

# "aliases" to the just-build binaries
node() {
    "${RPM_BUILD_ROOT}%{_bindir}/node-%{node_version_major}" \
        --icu-data-dir="${RPM_BUILD_ROOT}%{nodejs_datadir}/icudata" \
    "$@"
}
npm() {
    node "${RPM_BUILD_ROOT}%{_bindir}/npm-%{node_version_major}" "$@"
}

# === Sanity check for important versions
node -e 'require("assert").equal(process.versions.node, "%{node_version}")'
node -e 'require("assert").equal(process.versions.v8.replace(/-node\.\d+$/, ""), "%{v8_version}")'
%if %{with bundled_c_ares}
node -e 'require("assert").equal(process.versions.ares.replace(/-DEV$/, ""), "%{c_ares_version}")'
%endif
%if %{with bundled_punycode}
node --no-deprecation -e 'require("assert").equal(require("punycode").version, "%{nodejs_punycode_version}")'
%endif

npm version --json | jq --exit-status '.npm == "%{npm_version}"'

# === Custom and/or devendored parts sanity checks
# - full i18n support is available
node '%{SOURCE20}'
# - npm update notifier is disabled
npm config list --json | jq --exit-status '.["update-notifier"] == false'

# === Upstream test suite
bash '%{SOURCE10}' "${RPM_BUILD_ROOT}%{_bindir}/node-%{node_version_major}" test/ '%{SOURCE11}'


%files
%doc        README.md CHANGELOG.md GOVERNANCE.md onboarding.md
%license    LICENSE
%dir        %{nodejs_datadir}/
%dir        %{nodejs_datadir}/man/
%dir        %{nodejs_datadir}/man/man1/
#%%dir        %%{nodejs_common_sitelib}/
%dir        %{nodejs_private_sitelib}/
%{_bindir}/node-%{node_version_major}
%{nodejs_datadir}/man/man1/node.1*
%{_mandir}/man1/node-%{node_version_major}.1*

%files      libs
%license    LICENSE
%{_libdir}/libnode.so.%{node_soversion}
%{_libdir}/libv8.so.%{v8_version_major}.%{v8_version_minor}
%{_libdir}/libv8_libbase.so.%{v8_version_major}.%{v8_version_minor}
%{_libdir}/libv8_libplatform.so.%{v8_version_major}.%{v8_version_minor}

%files      devel
%license    LICENSE
%dir        %{nodejs_datadir}/
%{_includedir}/node/
%{_libdir}/libnode.so
%{_libdir}/pkgconfig/nodejs-%{node_version_major}.pc
%{_pkgdocdir}/gdbinit
%{_pkgdocdir}/lldb_commands.py
%{_rpmconfigdir}/fileattrs/nodejs%{node_version_major}_abi.attr
%{_rpmconfigdir}/nodejs%{node_version_major}_abi.req
%{nodejs_datadir}/common.gypi

%files -n   v8-%{v8_version_major}.%{v8_version_minor}-devel
%license    LICENSE
%{_includedir}/cppgc
%{_includedir}/libplatform
%{_includedir}/v8*.h
%{_libdir}/libv8.so
%{_libdir}/libv8_libbase.so
%{_libdir}/libv8_libplatform.so
%{_libdir}/pkgconfig/v8-%{v8_version_major}.%{v8_version_minor}.pc

%files      full-i18n
%doc        full-icu/icu4c-%{icu_version_major}.%{icu_version_minor}-data-bin-?-README.md
%license    full-icu/LICENSE
%dir        %{nodejs_datadir}/
%{nodejs_datadir}/icudata/

%files      npm
%doc        deps/npm/README.md
%license    deps/npm/LICENSE
%dir        %{nodejs_datadir}/
%dir        %{nodejs_private_sitelib}/
%{_bindir}/npm-%{node_version_major}
%{_bindir}/npx-%{node_version_major}
%{_mandir}/man1/npm-%{node_version_major}.1*
%{_mandir}/man1/npx-%{node_version_major}.1*
%{nodejs_datadir}/man
%{nodejs_private_sitelib}/npm/
%exclude    %{nodejs_datadir}/man/man1/node*.1*

%files      docs
%doc        doc/README.md
%license    LICENSE
%dir        %{_pkgdocdir}
%{_pkgdocdir}/html/
%{_pkgdocdir}/npm/

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1:24.13.1-2
- test: add initial lock files

* Thu Feb 19 2026 tjuhasz <tjuhasz@redhat.com> - 1:24.13.1-1
- Update to version 24.13.1 (rhbz#2438455)

* Thu Jan 22 2026 tjuhasz <tjuhasz@redhat.com> - 1:24.13.0-4
- Replace usage of man_info_compress to be funcional across all branches.

* Thu Jan 22 2026 Andrei Radchenko <aradchen@redhat.com> - 1:24.13.0-3
- build: expose libplatform symbols in shared libnode

* Mon Jan 19 2026 Jan Staněk <jstanek@redhat.com> - 1:24.13.0-2
- Diverge from rawhide

* Tue Jan 13 2026 tjuhasz <tjuhasz@redhat.com> - 1:24.13.0-1
- Update to version 24.13.0 (rhbz#2421027)

* Mon Jan 12 2026 Jan Staněk <jstanek@redhat.com> - 1:24.11.1-3
- Run version checks only on bundled components

* Tue Dec 02 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.11.1-2
- Fix name collision of the COMPRESS variable in spec file.

* Wed Nov 12 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.11.1-1
- Update to version 24.11.1 (rhbz#2414318)

* Wed Nov 12 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.11.0-2
- Rebuild for nodejs-packaging

* Wed Oct 29 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.11.0-1
- Update to version 24.11.0 (rhbz#2402617)

* Wed Oct 01 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.9.0-1
- Update to version 24.9.0 (rhbz#2399683)

* Thu Sep 11 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.8.0-1
- Update to version 24.8.0 (rhbz#2394460)

* Mon Sep 01 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.7.0-1
- Update to version 24.7.0 (rhbz#2391378)

* Mon Sep 01 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.6.0-5
- Adjust test-runner to prevent race-condition failures

* Wed Aug 27 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.6.0-4
- Add back fips prevention patch (rhbz#2389184)

* Mon Aug 25 2025 Jan Staněk <jstanek@redhat.com> - 1:24.6.0-3
- Import nodejs_abi requirement generator from packaging

* Mon Aug 18 2025 Andrei Radchenko <aradchen@redhat.com> - 1:24.6.0-2
- test-suite: add public test plan and gating file

* Fri Aug 15 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.6.0-1
- Update to version 24.6.0 (rhbz#2388711)

* Tue Aug 12 2025 Andrei Radchenko <aradchen@redhat.com> - 1:24.5.0-2
- spec: fix node binary calls to use versioned node-24 binary

* Fri Aug 01 2025 Andrei Radchenko <aradchen@redhat.com> - 1:24.5.0-1
- Update to version 24.5.0 (rhbz#2385880)

* Wed Jul 30 2025 Andrei Radchenko <aradchen@redhat.com> - 1:24.4.1-6
- spec: devel packages explicitly conflicts

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:24.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.4.1-3
- Remove tests from list which are not present in nodejs24

* Thu Jul 17 2025 Jan Staněk <jstanek@redhat.com> - 1:24.4.1-2
- Use local headers for building native addons when available

* Thu Jul 17 2025 tjuhasz <tjuhasz@redhat.com> - 1:24.4.1-1
- Update to version 24.4.1

* Wed Jul 16 2025 Jan Staněk <jstanek@redhat.com> - 1:24.4.0-3
- Remove arch-specific dependency from npm

* Mon Jul 14 2025 Jan Staněk <jstanek@redhat.com> - 1:24.4.0-1
- Update to version 24.4.0

* Thu Jul 10 2025 Jan Staněk <jstanek@redhat.com> - 1:24.0.1-1
- Initial package import (rhbz#2369466)
## END: Generated by rpmautospec
