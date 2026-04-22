# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           gpgverify
Version:        2.2
Release: 4%{?dist}
Summary:        Signature verifier for easy and safe scripting

License:        Boehm-GC
URL:            https://src.fedoraproject.org/rpms/gpgverify
Source:         gpgverify
Source:         macros.gpgverify.in
Source:         license.txt
BuildArch:      noarch

Requires:       grep gnupg2 gnupg2-verify

%description
GPGverify is a wrapper around GnuPG's gpgv. It verifies a file against an
OpenPGP signature and one or more keyrings. Rather than assuming manual use by
a knowledgeable user, GPGverify is designed to be easy to use safely in a
script. It avoids various unsafe ways of using gpgv that could make a script
vulnerable.

%prep
# Enable use of filenames instead of source numbers.
%setup -c -T
cp --preserve=timestamps %{sources} .

%conf
# Convey the location of the shellscript to macros.gpgverify. To keep build
# dependencies minimal, do substitution in Bash instead of something like Sed.
macrofile=$(<macros.gpgverify.in)
echo -E "${macrofile/@libexecdir@/'%{_libexecdir}'}" >macros.gpgverify

%install
mkdir --parents %{buildroot}%{rpmmacrodir} %{buildroot}%{_libexecdir}
cp --preserve=timestamps gpgverify %{buildroot}%{_libexecdir}/
cp macros.gpgverify %{buildroot}%{rpmmacrodir}/

%files
%attr(0755,-,-) %{_libexecdir}/gpgverify
%attr(0644,-,-) %{rpmmacrodir}/macros.gpgverify
%license license.txt

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Björn Persson <Bjorn@Rombobjörn.se> - 2.2-2
- Adapted the dependencies because the gnupg2 package has been split.

* Fri Jun 27 2025 Björn Persson <Bjorn@Rombobjörn.se> - 2.2-1
- Evaluate _libexecdir at build time, not at run time (reported by Yaakov
  Selkowitz).

* Fri May 09 2025 Björn Persson <Bjorn@Rombobjörn.se> - 2.1-3
- Rebuilt to retry the testsuite.

* Wed May 07 2025 Björn Persson <Bjorn@Rombobjörn.se> - 2.1-2
- Added a separate license file.

* Mon Apr 14 2025 Björn Persson <Bjorn@Rombobjörn.se> - 2.1-1
- GPGverify has been split out from redhat-rpm-config.
