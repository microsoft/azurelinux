Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# All package versioning is found here:
# the actual version is composed from these below
#   bzrmajor:  main bzr version
#   Version: bzr version, add subrelease version here
%global brzmajor 3.3
%global brzminor .17
 
Name:           breezy
Version:        %{brzmajor}%{?brzminor}
Release:        2%{?dist}
Summary:        Friendly distributed version control system
# breezy is GPL-2.0-or-later, but it has Rust dependencies
# see packaged LICENSE.dependencies for details
License:        GPL-2.0-or-later AND (MIT OR Apache-2.0) AND Unicode-DFS-2016 AND MIT AND (Unlicense OR MIT)
URL:            http://www.breezy-vcs.org/
Source0:        https://github.com/breezy-team/breezy/archive/brz-%{version}%{?brzrc}.tar.gz
Source1:        brz-icon-64.png
Source50:        lib-rio-vendor.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools-rust
BuildRequires:  cargo-rpm-macros >= 21
BuildRequires:  cargo2rpm
BuildRequires:  zlib-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  python3-setuptools-gettext
BuildRequires:  python3-wheel
BuildRequires:  python3-semantic_version
BuildRequires:  python3-configobj
BuildRequires:  python3-yaml
BuildRequires:  python3-fastbencode
BuildRequires:  python3-dulwich
BuildRequires:  python3-patiencediff
BuildRequires:  make
BuildRequires:  netavark
BuildRequires:  python3-sphinx

# This is the name of the command, note that it is brz, not bzr
Provides:       brz = %{version}-%{release}

# breezy is a fork of bzr and replaces it
Provides:       bzr = %{version}-%{release}
Obsoletes:      bzr < 3
Provides:       git-remote-bzr = %{version}-%{release}
Obsoletes:      git-remote-bzr < 3

# This is needed for launchpad support
Recommends:     python3-launchpadlib

%description
Breezy (brz) is a decentralized revision control system, designed to be easy
for developers and end users alike.

By default, Breezy provides support for both the Bazaar and Git file formats.


%prep
%autosetup -p1 -n %{name}-brz-%{version}%{?brzrc}

# Unpack vendored Rust deps for lib-rio (offline build)
tar -xzf %{SOURCE50} -C lib-rio

# Place workspace lockfile at repo root where cargo expects it
cp -f lib-rio/Cargo.lock .

ln -snf lib-rio/vendor vendor

%{__sed} -i -E 's|^license[[:space:]]*=[[:space:]]*"GPL-2\.0(-or-later)?"|license = { text = "GPL-2.0-or-later" }|' pyproject.toml

%cargo_prep
# Fix invalid TOML caused by unquoted RPM macros in Cargo config
if [ -f .cargo/config.toml ]; then
  %{__sed} -i -E 's|^([[:space:]]*opt-level[[:space:]]*=[[:space:]]*)([^"#][^#[:space:]]*)|\1"\2"|' .cargo/config.toml
  %{__sed} -i -E 's|^([[:space:]]*codegen-units[[:space:]]*=[[:space:]]*)([^"#][^#[:space:]]*)|\1"\2"|' .cargo/config.toml
  %{__sed} -i -E 's|^([[:space:]]*lto[[:space:]]*=[[:space:]]*)([^"#][^#[:space:]]*)|\1"\2"|' .cargo/config.toml
  %{__sed} -i -E 's|^([[:space:]]*debug[[:space:]]*=[[:space:]]*)([^"#][^#[:space:]]*)|\1"\2"|' .cargo/config.toml
fi
# Remove unused shebangs
sed -i '1{/#![[:space:]]*\/usr\/bin\/\(python\|env\)/d}' \
    breezy/__main__.py \
    breezy/git/git_remote_helper.py \
    breezy/git/tests/test_git_remote_helper.py \
    breezy/plugins/bash_completion/bashcomp.py \
    breezy/plugins/zsh_completion/zshcomp.py \
    breezy/tests/ssl_certs/create_ssls.py \
    contrib/brz_access
# Remove Cython generated .c files
find . -name '*_pyx.c' -exec rm \{\} \;
sed -i 's/Strip.All/Strip.No/' setup.py

mkdir -p .cargo
cat > .cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

[build]
rustc = "/usr/bin/rustc"
rustdoc = "/usr/bin/rustdoc"

[target.x86_64-unknown-linux-gnu]
linker = "/usr/bin/cc"
EOF

%build
export RUSTC=/usr/bin/rustc
export CARGO=/usr/bin/cargo
export RUSTDOC=/usr/bin/rustdoc
export CARGO_NET_OFFLINE=true

%pyproject_wheel

chmod a-x contrib/bash/brzbashprompt.sh

# Generate man pages
%{__python3} tools/generate_docs.py man

# Add Rust licenses
 %{cargo_license_summary}
 %{cargo_license} > LICENSE.dependencies

%install
%pyproject_install
%pyproject_save_files breezy
chmod -R a+rX contrib
chmod 0644 contrib/debian/init.d
chmod 0644 contrib/bzr_ssh_path_limiter  # note the bzr here
chmod 0644 contrib/brz_access
find %{buildroot}%{python3_sitearch}/%{name}/ -name '*.so' -exec chmod 0755 {} \;

install -Dpm 0644 contrib/bash/brz %{buildroot}%{_sysconfdir}/bash_completion.d/brz
rm contrib/bash/brz

install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/brz.png

# Install man pages manually
install -d %{buildroot}%{_mandir}/man1
[ -f brz.1 ] && install -m 0644 brz.1 %{buildroot}%{_mandir}/man1/
[ -f breezy/git/git-remote-bzr.1 ] && install -m 0644 breezy/git/git-remote-bzr.1 %{buildroot}%{_mandir}/man1/

# move git-remote-bzr to avoid conflict
mv %{buildroot}%{_bindir}/git-remote-bzr %{buildroot}%{_bindir}/git-remote-brz
mv %{buildroot}%{_mandir}/man1/git-remote-bzr.1 %{buildroot}%{_mandir}/man1/git-remote-brz.1

# backwards compatible symbolic links
ln -s brz %{buildroot}%{_bindir}/bzr
ln -s git-remote-brz %{buildroot}%{_bindir}/git-remote-bzr
echo ".so man1/brz.1" > %{buildroot}%{_mandir}/man1/bzr.1
echo ".so man1/git-remote-brz.1" > %{buildroot}%{_mandir}/man1/git-remote-bzr.1

# With older versions of setuptools-gettext, locales are generated to a weird
# directory; move them to datadir.
if [ -d %{buildroot}%{buildroot}%{_datadir}/locale ]
then
  mv %{buildroot}%{buildroot}%{_datadir}/locale %{buildroot}%{_datadir}
fi
%find_lang %{name}
cat %{name}.lang >> %{pyproject_files}
 
%check
# for now, at least run a basic smoke test to prevent undetected major breakages
# like https://bugzilla.redhat.com/2366194
export %{py3_test_envvars}
brz init-repo testrepo

%files -f %{pyproject_files}
# %license LICENSE.dependencies
%doc NEWS README.rst TODO contrib/
%{_bindir}/brz
%{_bindir}/bzr-*-pack
%{_bindir}/git-remote-brz
%{_bindir}/bzr
%{_bindir}/git-remote-bzr
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/brz
%{_datadir}/pixmaps/brz.png

%changelog
* Sat Dec 20 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 3.3.17-1
- Upgrade to version 3.3.17 (license: MIT).
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 01 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Thu Oct 24 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.1-4
- On Fedora 32+, replace bazaar with breezy
  https://fedoraproject.org/wiki/Changes/ReplaceBazaarWithBreezy

* Thu Oct 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.1-3
- Reenable all extension modules

* Thu Oct 10 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.1-2
- Disable the _static_tuple_c extension module to workaround Python 3.8 problems (#1760260)
- Other disabled modules depending on the above:
  _chk_map_pyx, _dirstate_helpers_pyx, _bencode_pyx, _btree_serializer_pyx

* Wed Sep 04 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.1-1
- Package breezy
