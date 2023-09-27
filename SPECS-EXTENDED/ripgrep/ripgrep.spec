#
# spec file for package ripgrep
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global rustflags '-Clink-arg=-Wl,-z,relro,-z,now'

Name:           ripgrep
Version:        13.0.0
Release:        5%{?dist}
Summary:        A search tool that combines ag with grep
License:        MIT AND Unlicense
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Text/Utilities
URL:            https://github.com/BurntSushi/ripgrep
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.xz
Source2:        cargo_config
BuildRequires:  cargo
BuildRequires:  rust >= 1.31
BuildRequires:  rubygem(asciidoctor)

%description
ripgrep is a line oriented search tool that combines the usability of
The Silver Searcher (similar to ack) with the raw speed of GNU grep.
ripgrep works by recursively searching your current directory
for a regex pattern.

%package bash-completion
Summary:        Bash Completion for %{name}
Group:          System/Shells
Requires:       bash-completion
Supplements:    (%{name} and bash)
BuildArch:      noarch

%description bash-completion
The official bash completion script for ripgrep, generated during the build.

%package zsh-completion
Summary:        ZSH Completion for %{name}
Group:          System/Shells
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description zsh-completion
The official zsh completion script for ripgrep, generated during the build.

%package fish-completion
Summary:        Fish Completion for %{name}
Group:          System/Shells
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description fish-completion
The official fish completion script for ripgrep, generated during the build.

%prep
%autosetup -p1 -a1

install -d -m 0755 .cargo
cp %{SOURCE2} .cargo/config

%build
export RUSTFLAGS=%{rustflags}
cargo build --release %{?_smp_mflags}

%install
export RUSTFLAGS=%{rustflags}
cargo install --path . --root=%{buildroot}%{_prefix}

# remove residue crate file
rm -f %{buildroot}%{_prefix}/.crates*

install -Dm 644 target/release/build/ripgrep-*/out/rg.bash %{buildroot}%{_datadir}/bash-completion/completions/rg
install -Dm 644 target/release/build/ripgrep-*/out/rg.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/rg.fish
install -Dm 644 complete/_rg %{buildroot}%{_datadir}/zsh/site-functions/_rg

%files
%license LICENSE-MIT UNLICENSE
%doc CHANGELOG.md README.md
%{_bindir}/rg

%files bash-completion
%{_datadir}/bash-completion

%files fish-completion
%{_datadir}/fish

%files zsh-completion
%{_datadir}/zsh

%changelog
* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 13.0.0-5
- Bump package to rebuild with rust 1.72.0

* Wed Aug 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 13.0.0-4
- Bump package to rebuild with stable Rust compiler

* Tue Dec 28 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 13.0.0-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified
- Converted 'Release' tag to the '[number].[distribution]' format
- Renamed vendor.tar.xz to %{name}-%{version}-vendor.tar.xz

* Wed Jul 14 2021 Andreas Schneider <asn@cryptomilk.org>
- Build with rust flags
- Add obs service file
* Sun Jun 13 2021 Avindra Goolcharan <avindra@opensuse.org>
- update to ripgrep 13.0.0:
  * A new short flag, -., has been added. It is an alias for the --hidden
    flag, which includes hidden files and directories in search
  * ripgrep is now using a new vectorized implementation of memmem, which
    accelerates many common searches. Please report performance regressions
    (or major improvements).
  * BREAKING: Binary detection output has changed slightly. In this
    release, a tweak has been made to the output format when a
    binary file is detected.
    Previous format:
    Binary file FOO matches (found "\0" byte around offset XXX)
    New format:
    FOO: binary file matches (found "\0" byte around offset XXX)
  * vimgrep output in multi-line now only prints the first line for
    each match. In multi-line mode, --count is now equivalent
    to --count-matches.
  * VULN #1773: public facing issue tracking CVE-2021-3013. ripgrep's README
    now contains a section describing how to report a vulnerability
  * PERF #1657: Check if a file should be ignored first before issuing stat calls
  * PERF memchr#82: ripgrep now uses a new vectorized implementation of memmem
  * FEAT: Added or improved file type filtering for ASP, Bazel, dvc,
    FlatBuffers, Futhark, minified files, Mint, pofiles (from GNU gettext)
    Racket, Red, Ruby, VCL, Yang
  * FEAT #1404: ripgrep now prints a warning if nothing is searched
  * FEAT #1680: Add -. as a short flag alias for --hidden.
  * FEAT #1842: Add --field-{context,match}-separator for customizing field delimiters.
  * FEAT #1856: README now links to Spanish translation.
  * BUG #1277: document cygwin path translation behavior in the FAQ
  * BUG #1739: fix bug where replacements were buggy if the regex matched a line terminator
  * BUG #1311: fix multi-line bug where a search & replace for \n didn't work as expected
  * BUG #1401: fix buggy interaction between PCRE2 look-around and -o/--only-matching
  * BUG #1412: fix multi-line bug with searches using look-around past matching lines
  * BUG #1577: fish shell completions will continue to be auto-generated
  * BUG #1642: fixes a bug where using -m and -A printed more matches than the limit
  * BUG #1703: clarify the function of -u/--unrestricted
  * BUG #1708: clarify how -S/--smart-case works
  * BUG #1730: clarify that CLI invocation must always be valid, regardless of config file
  * BUG #1741: fix stdin detection when using PowerShell in UNIX environments
  * BUG #1756: fix bug where foo/** would match foo, but it shouldn't
  * BUG #1765: fix panic when --crlf is used in some cases
  * BUG #1638: correctly sniff UTF-8 and do transcoding, like we do for UTF-16
  * BUG #1816: add documentation for glob alternate syntax, e.g., {a,b,..}
  * BUG #1847: clarify how the --hidden flag works
  * BUG #1866: fix bug when computing column numbers in --vimgrep mode
  * BUG #1868: fix bug where --passthru and -A/-B/-C did not override each other
  * BUG #1869: clarify docs for --files-with-matches and --files-without-match
  * BUG #1878: fix bug where \A could produce unanchored matches in multiline search
  * BUG 94e4b8e3: Fix column numbers with --vimgrep is used with -U/--multiline
- ran spec-cleaner
* Tue Jul 28 2020 Martin Rey <mrey@suse.com>
- ripgrep 12.1.1
  * Corrects some egregious markup output in --help (#1581)
  * Mention the special $0 capture group in docs for the
  - r/--replace flag. (#1591)
  * Fix failing test resulting from out-of-sync dependencies.
    (#1602)
* Fri May 15 2020 Andreas Stieger <andreas.stieger@gmx.de>
- ripgrep 12.1.0
  * many bug fixes
  * performance improvements
  * --no-pcre2-unicode deprecated in favor of --no-unicode
  * --auto-hybrid-regex deprecated in favor of --engine auto
  * supports decompressing .Z files via uncompress
- drop ripgrep-11.0.2-reproducible-manpage.patch, now upstream
* Thu Apr 30 2020 Martin Wilck <mwilck@suse.com>
- Remove transient file .crates2.json during build
* Wed Mar 25 2020 Bernhard Wiedemann <bwiedemann@suse.com>
- Add ripgrep-11.0.2-reproducible-manpage.patch (boo#1100677)
* Mon Nov 11 2019 Ismail Dönmez <idonmez@suse.com>
- Update to version 11.0.2
  * See included CHANGELOG.md for the complete changelog
* Sun Sep 16 2018 Avindra Goolcharan <avindra@opensuse.org>
- Updated to version 0.10.0
- Breaking change
  * The match semantics of -w/--word-regexp have changed slightly.
    They used to be \b(?:<your pattern>)\b. Now, it's
    (?:^|\W)(?:<your pattern>)(?:$|\W). This matches the behavior
    of GNU grep and is believed to be closer to the intended
    semantics of the flag.
- Features
  * Add -U/--multiline flag that permits matching over multiple lines.
  * Add -P/--pcre2 flag that gives support for look-around and
    backreferences.
  * Add --json flag that prints results in a JSON Lines format.
  * --one-file-system flag to skip directories on different file systems.
  * Add --sort and --sortr flag for more sorting. Deprecate --sort-files.
  * The --trim flag strips prefix whitespace from all lines printed.
  * Add --null-data flag, which makes ripgrep use NUL as a line terminator.
  * The --passthru flag now works with the --replace flag.
  * Add --line-buffered and --block-buffered for forcing a buffer strategy.
  * Add --pre-glob for filtering files through the --pre flag.
- Bug fixes
  * Searching with non-zero context can now use memory maps if
    appropriate.
  * ripgrep will now stop correctly when its output pipe is closed.
  * The -w/--word-regexp flag now works more intuitively.
  * Detection of readable stdin has improved on Windows.
  * Matching empty lines now works correctly in several corner cases.
  * Color escape sequences now coalesce, which reduces output size.
  * ripgrep is now more robust with respect to memory maps failing.
  * Color escape sequences are no longer emitted for empty matches.
  * Context from the --passthru flag should not impact process exit status.
  * Fixes bug in ignore crate where first path was always treated
    as a symlink.
  * Read stderr asynchronously when running a process.
  * Add compile time and runtime CPU features to --version output.
  * Don't complete bare pattern after -f in zsh.
* Mon Aug 27 2018 jengelh@inai.de
- Update RPM groups and summary.
* Sun Aug 26 2018 viktor.saevars@gmail.com
- Updated to version 0.9.0
- Breaking changes
  * When --count and --only-matching are provided simultaneously,
    the behavior of ripgrep is as if the --count-matches flag was given.
  * Octal syntax is no longer supported.
  * The --line-number-width flag has been removed.
- Features
  * Added a --stats flag, which emits aggregate statistics
    after search results.
  * lz4 support when using the -z flag
  * Added --no-ignore-global that permits disabling global gitignores
  * Renamed --maxdepth to --max-depth
  * Added a --pre option to filter with an arbitrary program
  * Improved zsh completion
- Bug fixes
  * No longer skips tar archives when -z is used
  * Ignore gitignore files if outside of a repository
  * Use more descriptive error messages
* Tue Mar 13 2018 avindra@opensuse.org
- reduce tarball sizes
  * source tarball taken as is from github
  * vendor tarball compressed with xz
  - cleanup with spec-cleaner
  - port history to ripgrep.changes
  - mark as dual licensed with MIT
  - split completion scripts off into separate packages
* Fri Mar  9 2018 viktor.saevars@gmail.com
- Use version 0.8.1
  - Generate man file
  - Add check
  - Remove empty post and postun
* Sun Oct  8 2017 viktor.saevars@gmail.com
- Inital packaging @ 0.6.0
