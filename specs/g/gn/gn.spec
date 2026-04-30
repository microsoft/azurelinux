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

# Build HTML docs from markdown using pandoc?
%bcond html_docs 1

Name:           gn
# Upstream uses the number of commits in the git history as the version number.
# See gn --version, which outputs something like “1874 (2b683eff)”. The commit
# position and short commit hash in this string come from “git describe HEAD
# --match initial-commit”; see build/gen.py. This means that a complete git
# checkout is required to establish the version number; the information is not
# in the tarball! This is terribly inconvenient. See
# https://bugs.chromium.org/p/gn/issues/detail?id=3.
#
# As a result, it is necessary to use our custom update-version script,
# supplying the new full commit hash as the sole argument or providing no
# arguments to select the latest commit. This will:
#  1. Clone the git repository from the Internet (a substantial download)
#  2. Run build/gen.py to generate last_commit_position.h, the header with
#     version information, and copy it into the same directory as the script
#  3. Modify the commit and access macros and the Version field in this spec
#     file.
#  4. Download the source tarball (spectool -g)
#  5. Update the sources (fedpkg new-sources %%{commit}.tar.gz)
#  6. Stage all changes in git
#  7. Commit the changes
#
# See https://gn.googlesource.com/gn/+log for the latest changes.
%global commit 304bbef6c7e9a86630c12986b99c8654eb7fe648
%global access 20260205
%global shortcommit %{sub %{commit} 1 12}
%global position 2324
Version:        %{position}^%{access}.%{shortcommit}
Release:        %autorelease
Summary:        Meta-build system that generates build files for Ninja

# The entire source is BSD-3-Clause, except:
#   - src/base/third_party/icu/ is (Unicode-DFS-2016 AND ICU); see
#     src/base/third_party/icu/LICENSE and also the header comment in
#     src/base/third_party/icu/icu_utf.h.
#
# Note that src/util/test/gn_test.cc, which is licensed Apache-2.0, does not
# contribute to the binary RPMs, only to the gn_unittests executable, which is
# not installed; you may verify this with:
#   gdb -ex 'set pagination off' -ex 'info sources' gn | grep -F gn_test.cc
License:        BSD-3-Clause AND Unicode-DFS-2016 AND ICU
SourceLicense:  %{license} AND Apache-2.0
URL:            https://gn.googlesource.com/gn
Source0:        %{url}/+archive/%{commit}.tar.gz#/gn-%{shortcommit}.tar.gz
# Generated using script update-version:
Source1:        last_commit_position.h
Source2:        update-version

# Downstream-only: do not override optimization flags
#
# Stop overriding optimization flags; not sent upstream because this is
# intentional on their part.
#
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_flags
Patch:          0001-Downstream-only-do-not-override-optimization-flags.patch
# Downstream-only: do not build with -Wno-format
#
# This conflicts with -Werror=format-security.
Patch:          0002-Downstream-only-do-not-build-with-Wno-format.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  python3-devel
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

# For RPM macros:
BuildRequires:  emacs-common

%if %{with html_docs}
BuildRequires:  pandoc
BuildRequires:  parallel
%endif
BuildRequires:  help2man

Requires:       vim-filesystem
Requires:       python3
Provides:       vim-gn = %{version}-%{release}

Requires:       emacs-filesystem >= %{_emacs_version}
Provides:       emacs-gn = %{version}-%{release}

# src/base/third_party/icu/icu_utf.h:
#
#   This file has the relevant components from ICU copied to handle basic
#   UTF8/16/32 conversions. Components are copied from umachine.h, utf.h,
#   utf8.h, and utf16.h into icu_utf.h.
#
# The forked, bundled ICU components are copied from Chromium. Because of the
# downstream changes (primarily, changing namespaces and symbol prefixes),
# there is no clear path to unbundling.
#
# See src/base/third_party/icu/README.chromium, from which the version number
# is taken.
Provides:       bundled(icu) = 60

%description
GN is a meta-build system that generates build files for Ninja.


%package doc
Summary:        Documentation for GN
BuildArch:      noarch

%description doc
The gn-doc package contains detailed documentation for GN.


%prep
%autosetup -c -n gn-%{commit} -p1

# Use pre-generated last_commit_position.h.
mkdir -p ./out
cp -vp '%{SOURCE1}' ./out

# Copy and rename vim extensions readme for use in the main documentation
# directory.
cp -vp misc/vim/README.md README-vim.md

# Fix shebangs in examples and such.
%py3_shebang_fix .


%conf
AR='gcc-ar'; export AR
# Treating warnings as errors is too strict for downstream builds.
#
# Both --use-icf and --use-lto add compiler flags that only work with clang++,
# not with g++. We do get LTO on Fedora anyway, since we respect the
# distribution’s build flags.
%{python3} build/gen.py \
    --allow-warnings \
    --no-last-commit-position \
    --no-strip \
    --no-static-libstdc++


%build
ninja -j %{_smp_build_ncpus} -C out -v

%if %{with html_docs}
# There is a script, misc/help_as_html.py, that generates some HTML help, but
# pandoc does a better job and we can cover more Markdown sources.
find . -type f -name '*.md' | parallel -v pandoc -o '{.}.html' '{}'
%endif

help2man \
    --name='%{summary}' \
    --version-string="gn $(./out/gn --version)" \
    --no-info \
    ./out/gn |
  # Clean up a couple of stray binary bytes in the help output
  tr -d '\302\240' |
  # Format the entries within the sections as tagged paragraphs, and italicise
  # [placeholders in square brackets].
  sed -r -e 's/(^[[:alnum:]_]+:)/.TP\n.B \1\n/' \
      -e 's/\[([^]]+)\]/\\fI[\1]\\fR/g' > out/gn.1


%install
install -t '%{buildroot}%{_bindir}' -D -p out/gn

install -d '%{buildroot}%{_datadir}/vim/vimfiles'
cp -vrp misc/vim/* '%{buildroot}%{_datadir}/vim/vimfiles'
find '%{buildroot}%{_datadir}/vim/vimfiles' \
    -type f -name 'README.*' -print -delete
%py_byte_compile %{python3} '%{buildroot}%{_datadir}/vim/vimfiles/gn-format.py'

install -t '%{buildroot}%{_emacs_sitestartdir}' -D -p -m 0644 misc/emacs/*.el

install -t '%{buildroot}%{_mandir}/man1' -D -m 0644 -p out/gn.1


%check
out/gn_unittests

# Verify consistency of the version header with the spec file
grep -E '^#define[[:blank:]]+LAST_COMMIT_POSITION_NUM[[:blank:]]+'\
'%{position}[[:blank:]]*' \
    'out/last_commit_position.h' >/dev/null
grep -E '^#define[[:blank:]]+LAST_COMMIT_POSITION[[:blank:]]+'\
'"%{position} \(%{shortcommit}\)"[[:blank:]]*' \
    'out/last_commit_position.h' >/dev/null


%files
%license LICENSE
%{_bindir}/gn

%{_mandir}/man1/gn.1*

%{_datadir}/vim/vimfiles/gn-format.py
%{_datadir}/vim/vimfiles/autoload/gn.vim
%{_datadir}/vim/vimfiles/ftdetect/gnfiletype.vim
%{_datadir}/vim/vimfiles/ftplugin/gn.vim
%{_datadir}/vim/vimfiles/syntax/gn.vim

%{_emacs_sitestartdir}/gn-mode.el


%files doc
%license LICENSE src/base/third_party/icu/README.chromium
%doc AUTHORS
%doc OWNERS
%doc README*.md
%if %{with html_docs}
%doc README*.html
%endif
%doc docs/
%doc examples/
%doc infra/
%doc tools/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2324^20260205.304bbef6c7e9-2
- test: add initial lock files

* Thu Feb 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2324^20260205.304bbef6c7e9-1
- Update to version 2324

* Thu Feb 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2322^20260205.7498ca2e5e24-1
- Update to version 2322

* Sun Jan 18 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2318^20260118.103f8b437f5e-1
- Update to version 2318

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2316^20260111.9673115bc14c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Jan 11 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2316^20260111.9673115bc14c-1
- Update to version 2316

* Wed Jan 07 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2315^20260107.5550ba0f4053-1
- Update to version 2315

* Wed Dec 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2311^20251224.64d35867ca0a-1
- Update to version 2311

* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2308^20251209.5964f4997670-1
- Update to version 2308

* Thu Nov 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2295^20251120.c5a0003bcc2a-1
- Update to version 2295
- In the version number, change the style of the snapshot information

* Tue Nov 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2291^20251111gite7f3202128bd-1
- Update to version 2291

* Tue Nov 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2288^20251104git092f4f0d612e-1
- Update to version 2288

* Thu Oct 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2287^20251009git07d3c6f4dc29-1
- Update to version 2287

* Wed Sep 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2285^20250924git81b24e01531e-1
- Update to version 2285

* Sat Sep 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2281^20250913gitaa3ecaecac29-1
- Update to version 2281

* Sun Aug 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2279^20250831git5d0a4153b0bc-1
- Update to version 2279

* Tue Aug 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2276^20250812gitc15bfa41e526-1
- Update to version 2276

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2256^20250710git635a71e20e99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2256^20250710git635a71e20e99-1
- Update to version 2256

* Sat Jun 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2251^20250614git54169531ed6d-1
- Update to version 2251

* Fri May 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2239^20250530gitafd24ed11bc5-1
- Update to version 2239

* Sun May 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2237^20250525gitebc8f16ca7b0-1
- Update to version 2237

* Wed May 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2236^20250521gitcad8f67e2dd0-1
- Update to version 2236

* Fri May 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2235^20250516git0c25d1bbde6e-1
- Update to version 2235

* Fri May 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2234^20250502git487f8353f154-1
- Update to version 2234

* Fri Apr 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2232^20250425git90478db6b59b-1
- Update to version 2232

* Thu Apr 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2223^20250403git6e8e0d6d4a15-1
- Update to version 2223

* Sun Mar 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2222^20250316git18602f6cf116-1
- Update to version 2222

* Sat Mar 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2221^20250308git7a8aa3a08a13-1
- Update to version 2221

* Mon Mar 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2214^20250303git3d0d3445f67d-1
- Update to version 2214

* Mon Mar 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2213^20250303git4a8016dc3915-1
- Update to version 2213

* Wed Jan 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2209^20250129gitab638bd7cbb9-1
- Update to version 2209

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2207^20250116gited1abc107815-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2207^20250116gited1abc107815-1
- Update to version 2207

* Fri Dec 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2206^20241227gitc97a86a72105-1
- Update to version 2206

* Thu Dec 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2204^20241129git468c6128db7f-2
- Add a SourceLicense field

* Fri Nov 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2204^20241129git468c6128db7f-1
- Update to version 2204

* Fri Nov 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2201^20241017gitfeafd1012a32-2
- Invoke build/gen.py in %%conf rather than in %%build

* Thu Oct 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2201^20241017gitfeafd1012a32-1
- Update to version 2201

* Wed Sep 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2200^20240925git95b0f8fe31a9-1
- Update to version 2200

* Thu Sep 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2198^20240912git20806f79c6b4-1
- Update to version 2198

* Sat Aug 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2190^20240824git225e90c5025b-1
- Update to version 2190

* Wed Aug 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2188^20240821gitd010e218ca70-1
- Update to version 2188

* Mon Aug 19 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2187^20240819git32f63e70484f-1
- Update to version 2187

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2185^20240815git54f5b539df8c-1
- Update to version 2185

* Mon Aug 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2180^20240812git449f3e4dfb45-1
- Update to version 2180

* Wed Aug 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2179^20240807git05eed8f6252e-1
- Update to version 2179

* Tue Aug 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2178^20240806git8f2193f70793-1
- Update to version 2178

* Wed Jul 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2177^20240731git0ee833e823f2-1
- Update to version 2177

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2175^20240611gitb2afae122eeb-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2175^20240611gitb2afae122eeb-1
- Update to version 2175

* Fri Jun 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2174^20240607gitb3a0bff47dd8-1
- Update to version 2174

* Fri May 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2171^20240530gitd010969ecc31-2
- Correct SPDX License expression

* Thu May 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2171^20240530gitd010969ecc31-1
- Update to version 2171

* Thu May 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2168^20240514gitdf98b86690c8-2
- Use git to generate downstream patches

* Tue May 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2168^20240514gitdf98b86690c8-1
- Update to version 2168

* Thu May 09 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2166^20240509gitb0c2742896b6-1
- Update to version 2166

* Fri Apr 19 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2164^20240419git155c53952ec2-1
- Update to version 2164

* Wed Apr 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2163^20240410gitd823fd85da3f-1
- Update to version 2163

* Wed Apr 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2161^20240403git415b3b19e094-1
- Update to version 2161

* Fri Mar 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2160^20240329git93ee9b91423c-1
- Update to version 2160

* Wed Mar 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2159^20240327gitcfddfffb7913-1
- Update to version 2159

* Fri Mar 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2157^20240315git22581fb46c0c-1
- Update to version 2157

* Fri Mar 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2155^20240308gitdd0927eb34bb-1
- Update to version 2155

* Mon Mar 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2154^20240301git88e8054aff7b-2
- Bump release to upgrade F38

* Fri Mar 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2154^20240301git88e8054aff7b-1
- Update to version 2154

* Fri Mar 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2150^20240226git5787e994aa4c-3
- Respect %%_smp_build_ncpus

* Mon Feb 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2150^20240226git5787e994aa4c-1
- Update to version 2150

* Thu Feb 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2149^20240222git03d10f1657b4-1
- Update to version 2149

* Fri Feb 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2146^20240216git0a2b8eac80f1-1
- Update to version 2146

* Thu Feb 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2145^20240215git8b973aa51d02-1
- Update to version 2145

* Wed Feb 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2144^20240214gita3dcd7a7ad86-1
- Update to version 2144

* Sat Jan 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2143^20240127gita2e2717ea670-1
- Update to version 2143

* Tue Jan 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2140^20240123gitf99e015ac35f-1
- Update to version 2140

* Sat Jan 20 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2139^20240120gitb5adfe5f574d-1
- Update to version 2139

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2136^20240116git5d76868385b8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2136^20240116git5d76868385b8-1
- Update to version 2136

* Mon Jan 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2135^20240115gitb8562a4abd95-1
- Update to version 2135

* Sat Jan 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2134^20240113git5fd939de8a66-1
- Update to version 2134

* Tue Dec 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2131^20231219git85944ebc24a9-1
- Update to version 2131

* Tue Nov 28 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2130^20231128git7367b0df0a0a-1
- Update to version 2130

* Thu Nov 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2129^20231123git92e63272dc04-1
- Update to version 2129

* Mon Nov 20 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2128^20231120gitc7b223bfb225-1
- Update to version 2128

* Wed Nov 15 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2127^20231115gitbc5744174d9e-1
- Update to version 2127

* Mon Nov 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2125^20231113git85bd0a62938b-1
- Update to version 2125

* Tue Oct 24 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2124^20231024gite4702d740906-1
- Update to version 2124

* Fri Oct 20 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2123^20231020git5d8727f3fbf4-1
- Update to version 2123

* Thu Oct 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2122^20231012git182a6eb05d15-1
- Update to version 2122

* Thu Oct 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2121^20230913git991530ce394e-3
- Drop gn-5e19d2fb166f-redundant-move.patch
- This isn’t needed since we tolerate warnings

* Thu Oct 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2121^20230913git991530ce394e-2
- Drop the “werror” bcond
- Always allow warnings

* Wed Sep 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2121^20230913git991530ce394e-1
- Update to version 2121

* Thu Aug 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2119^20230810gitcc56a0f98bb3-1
- Update to version 2119

* Thu Aug 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2118^20230803git811d332bd905-1
- Update to version 2118

* Thu Jul 27 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2117^20230727git3fccef9033b9-1
- Update to version 2117

* Wed Jul 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2115^20230726git1029a3b50873-1
- Update to version 2115

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2114^20230712gitfae280eabe5d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2114^20230712gitfae280eabe5d-1
- Update to version 2114

* Tue Jul 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2113^20230711git11e12b0ef870-1
- Update to version 2113

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2109^20230618git4bd1a77e6795-1
- Update to version 2109

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2106^20230529gite3978de3e8da-3
- Use new (rpm 4.17.1+) bcond style

* Sat Jun 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2106^20230529gite3978de3e8da-2
- Remove explicit %%set_build_flags, not needed since F36

* Mon May 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2106^20230529gite3978de3e8da-1
- Update to version 2106

* Sun May 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2105^20230521gite9e83d9095d3-1
- Update to version 2105

* Thu May 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2104^20230518git6975103d9f59-1
- Update to version 2104

* Wed May 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2092^20230510git26aa46c283e4-1
- Update to version 2092

* Wed Apr 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2088^20230419git5a004f9427a0-2
- Remove gn-5e19d2fb166f-stdint.patch since it is now upstream

* Wed Apr 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2088^20230419git5a004f9427a0-1
- Update to version 2088

* Sat Apr 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2087^20230408gitffeea1b1fd07-1
- Update to version 2087

* Thu Apr 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2086^20230406git61da8bdce622-1
- Update to version 2086

* Sun Mar 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2084^20230319git41fef642de70-1
- Update to version 2084

* Sun Mar 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2082^20220714gitfe330c0ae1ec-2
- Fix updating access time in snapshot info

* Sun Feb 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2082^20220714gitfe330c0ae1ec-1
- Update to version 2082

* Mon Feb 20 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2081^20220714gitb25a2f8c2d33-1
- Update to version 2081

* Thu Feb 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2080^20220714gitedf6ef4b06b4-1
- Update to version 2080

* Tue Jan 31 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2079^20220714git84c8431f3e03-1
- Update to version 2079

* Mon Jan 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2077^20220714git5e19d2fb166f-7
- Updated comment on redundant move patch

* Thu Jan 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2077^20220714git5e19d2fb166f-6
- Add two patches for GCC 13

* Thu Jan 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2077^20220714git5e19d2fb166f-5
- Build without -Werror

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2077^20220714git5e19d2fb166f-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2077^20220714git5e19d2fb166f-3
- Leaf package: remove i686 support

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2077^20220714git5e19d2fb166f-2
- Indicate dirs. in files list with trailing slashes

* Wed Dec 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2077^20220714git5e19d2fb166f-1
- Update to version 2077

* Fri Dec 02 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2073^20220714git70d6c60823c0-1
- Update to version 2073

* Sun Nov 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2072^20220714git1c4151ff5c1d-1
- Update to version 2072

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2071^20220714gita4d67be044b4-1
- Update to version 2071

* Sat Oct 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2067^20220714git27b90626701a-1
- Update to version 2067

* Wed Oct 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2066^20220714git57c352b2b034-1
- Update to version 2066

* Sat Oct 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2065^20220714gitb9c6c19be95a-1
- Update to version 2065

* Tue Sep 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2064^20220714gitcc28efe62ef0-1
- Update to version 2064

* Sun Sep 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2059^20220714gitb4851eb2062f-1
- Update to version 2059

* Tue Sep 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2058^20220714git00b741b1568d-1
- Update to version 2058

* Tue Aug 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2057^20220714git5705e56a0e58-1
- Update to version 2057

* Sat Aug 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2056^20220714git0bcd37bd2b83-1
- Update to version 2056

* Thu Aug 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2051^20220714gitc8c63300ac8e-2
- Fix typo in SPDX expression

* Wed Aug 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2051^20220714gitc8c63300ac8e-1
- Update to version 2051

* Wed Aug 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2050^20220714git9ef321772ecc-3
- Convert License to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2050^20220714git9ef321772ecc-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2050^20220714git9ef321772ecc-1
- Update to version 2050

* Thu Jul 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2049^20220707git03ce92df-1
- Update to version 2049

* Thu Jun 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2047^20220623git29accf5a-1
- Update to version 2047

* Wed Jun 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2043^20220615gite62d4e19-1
- Update to version 2043

* Mon Jun 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2042^20220613git2ecd43a1-1
- Update to version 2042

* Wed Jun 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2041^20220608gitfd6cae41-1
- Update to version 2041

* Mon May 02 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2014^20220413gitc114b7e0-2
- Add patch upstream status for gn-0153d369-no-O3.patch

* Sun May 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2014^20220413gitc114b7e0-1
- Handle snapshot info the “modern” way, in the Version

* Sat Apr 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2014-3.20220413gitc114b7e0
- Improve handling of bundled ICU components

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2014-2.20220413gitc114b7e0
- Stop numbering patches

* Wed Apr 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2014-1.20220413gitc114b7e0
- Update to version 2014

* Thu Apr 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2011-1.20220407gitae110f8b
- Update to version 2011

* Thu Mar 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1998-1.20220331git93f0d7a7
- Update to version 1998

* Mon Mar 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1985-1.20220321gitbd99dbf9
- Update to version 1985

* Mon Mar 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1983-1.20220314gitf27bae88
- Update to version 1983

* Fri Mar 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1977-1.20220304gitd7c2209c
- Update to version 1977

* Tue Feb 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1975-1.20220222git6109f626
- Update to version 1975

* Sat Feb 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1972-2.20220212git377f566a
- BR emacs-common for RPM macros

* Sat Feb 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1972-1.20220212git377f566a
- Update to version 1972

* Fri Feb 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1970-3.20220201git4b613b10
- Drop even the emacs-nox BR

* Fri Feb 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1970-2.20220201git4b613b10
- BR emacs-nox instead of full emacs

* Tue Feb 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1970-1.20220201git4b613b10
- Update to version 1970

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1967-2.20220112git80a40b07
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1967-1.20220112git80a40b07
- Update to version 1967

* Fri Jan 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1966-1.20220107gitf1b14125
- Update to version 1966

* Wed Dec 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1961-1.20211222git281ba2c9
- Update to version 1961

* Wed Dec 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1959-1.20211215git2e56c317
- Update to version 1959

* Sat Dec 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1958-1.20211211gitd417bc7e
- Update to version 1958

* Sun Dec 05 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1953-1.20211205gite0afadf7
- Update to version 1953

* Fri Dec 03 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1951-2.20211128gitb7903130
- Drop BR on python3, redundant with python3-devel

* Sun Nov 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1951-1.20211128gitb7903130
- Update to version 1951

* Fri Nov 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1945-1.20211119git4aa9bdfa
- Update to version 1945

* Tue Nov 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1944-1.20211116git18512455
- Update to version 1944

* Sun Nov 07 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1943-2.20211107git90294ccd
- Drop “gcc cleanup” patch (finally upstreamed)

* Sun Nov 07 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1943-1.20211107git90294ccd
- Update to version 1943

* Tue Nov 02 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1942-1.20211102git8926696a
- Update to version 1942

* Mon Oct 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1939-2.20211018git693f9fb8
- Use %%%%python3 macro instead of %%%%__python3

* Mon Oct 18 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1939-1.20211018git693f9fb8
- Update to version 1939

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1938-3.20210927git0153d369
- Reduce macro indirection in the spec file

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1938-2.20210927git0153d369
- Correctly stop overriding optimization flags

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1938-1.20210927git0153d369
- Update to version 1938

* Sun Sep 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1937-1.20210919gitde86ec41
- Update to version 1937

* Sat Sep 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1936-1.20210911git07e2e1b9
- Update to version 1936 (Fix typos in README.md)

* Mon Sep 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1935-1.20210906git46b572ce
- Update to version 1935

* Thu Aug 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1934-1.20210812git69ec4fca
- Update to version 1934

* Tue Aug 03 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1931-1.20210803giteea3906f
- Update to version 1931

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1929-3.20210720gitd565aa3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1929-2.20210720gitd565aa3e
- Drop workarounds for F32 and EPEL

* Tue Jul 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1929-1.20210720gitd565aa3e
- Update to version 1929

* Thu Jul 08 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1924-1.20210708git24e2f7df
- Update to version 1924

* Sun Jun 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1921-1.20210627git4d207c94
- Update to version 1921

* Wed Jun 23 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1920-1.20210623gitd924640c
- Update to version 1920
- Stop overriding optimization flags

* Tue Jun 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1919-1.20210622gite9b84332
- Update to version 1919

* Wed Jun 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1916-1.20210616gitd2dce752
- Update to version 1916

* Tue May 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1910-2.20210511git39a87c0b
- Rebase chromium-84.0.4147.105-gn-gcc-cleanup.patch as
  gn-39a87c0b-gcc-cleanup.patch

* Tue May 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1910-1.20210511git39a87c0b
- Update to version 1910

* Sun May 02 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1898-1.20210502git6771ce56
- Update to version 1898

* Sat Apr 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1897-1.20210410gitdba01723
- Update to version 1897

* Tue Apr 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1896-1.20210406gita95c8a3c
- Update to version 1896
- Do not use %%exclude for unpackaged files (RPM 4.17 compatibility)

* Mon Mar 29 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1894-4.20210329gitb2e3d862
- Update to version 1894

* Wed Mar 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1893-3.20210314git64b3b940
- Stop installing xemacs plugins
  (https://fedoraproject.org/wiki/Changes/Deprecate_xemacs)

* Wed Mar 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1893-2.20210314git64b3b940
- Improved source URL based on package review feedback

* Mon Mar  1 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1893-1.20210314git64b3b940
- Update to version 1893

* Mon Mar  1 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1891-1.20210127gitdfcbc6fe
- Update to version 1891

* Sun Jan  3 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1884-1.20210127git94bda7cc
- Update to version 1884

* Sun Jan  3 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1876-1.20210103git0d67e272
- Update to version 1876

* Sat Dec 19 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1875-1.20201219git4e260f1d
- Initial spec file

## END: Generated by rpmautospec
