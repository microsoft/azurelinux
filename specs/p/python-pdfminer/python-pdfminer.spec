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

Name:           python-pdfminer
Version:        20260107
Release:        %autorelease
Summary:        Tool for extracting information from PDF documents

# The entire source is MIT except:
#
# LicenseRef-Fedora-Public-Domain:
#   pdfminer/arcfour.py
#     - If this is a bundled library, its origin is unclear
#   pdfminer/ascii85.py
#     - If this is a bundled library, its origin is unclear
# The public-domain dedication text was added to public-domain-text.txt in
# fedora-license-data in commit e75b02b91633c17388b6e67dc5884702f8bee22b:
# https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/194
#
# APAFML:
#   pdfminer/fontmetrics.py
#     - Data extracted and converted from the AFM files:
#       https://www.ctan.org/tex-archive/fonts/adobe/afm/
#
# BSD-3-Clause:
#   pdfminer/cmap/*
#     - Both the original bundled data and the data generated from the
#       adobe-mappings-cmap package are BSD-3-Clause-licensed.
#
# Apache-2.0 AND MIT:
#   pdfminer/_saslprep.py
#     - Forked from from Apache-2.0 code by MongoDB, Inc.—originally
#       pymongo/saslprep.py in mongo-python-driver (python-pymongo), with
#       additional modifications in pyHanko (not yet packaged); see
#       docs/licenses/LICENSE.pyHanko.
#
# Adobe-Glyph:
#   pdfminer/glyphlist.py
#     - Contains both code under the base MIT license and data extracted and
#       converted from
#       https://partners.adobe.com/public/developer/en/opentype/glyphlist.txt
#       under the Adobe Glyph List License
License:        %{shrink:
                MIT AND
                LicenseRef-Fedora-Public-Domain AND
                APAFML AND
                BSD-3-Clause AND
                (Apache-2.0 AND MIT) AND
                Adobe-Glyph
                }
URL:            https://github.com/pdfminer/pdfminer.six
# This has the samples/ directory stripped out. While upstream claims the
# sample PDFs are “freely distributable”, they have unclear or unspecified
# licenses, which makes them unsuitable for Fedora. This applies especially,
# but not exclusively, to the contents of samples/nonfree.
#
# Generated with ./get_source.sh %%{version}
Source0:        pdfminer.six-%{version}-filtered.tar.zst
# Script to generate Source0; see comments above.
Source1:        get_source.sh
# Man pages written by hand for Fedora in groff_man(7) format using the
# command’s --help output
Source2:        dumppdf.1
Source3:        pdf2txt.1

BuildSystem:            pyproject
BuildOption(prep):      -S git
BuildOption(generate_buildrequires): -x image
BuildOption(install):   -l pdfminer

BuildArch:      noarch

BuildRequires:  git-core
BuildRequires:  make

# We use the Japan1, Korea1, GB1, and CNS1 CMaps:
BuildRequires:  adobe-mappings-cmap-devel >= 20190730

# We do not generate BR’s from the “dev” extra because it includes an exact
# version requirement on mypy (and we do not intend to do typechecking), and it
# pulls in nox and black. We just want to use plain pytest.
BuildRequires:  %{py3_dist pytest}

%global common_description %{expand:
Pdfminer.six is a community maintained fork of the original PDFMiner. It is a
tool for extracting information from PDF documents. It focuses on getting and
analyzing text data. Pdfminer.six extracts the text from a page directly from
the sourcecode of the PDF. It can also be used to get the exact location, font
or color of the text.

It is built in a modular way such that each component of pdfminer.six can be
replaced easily. You can implement your own interpreter or rendering device
that uses the power of pdfminer.six for other purposes than text analysis.

Check out the full documentation on Read the Docs
(https://pdfminersix.readthedocs.io/).

Features:

  • Written entirely in Python.
  • Parse, analyze, and convert PDF documents.
  • PDF-1.7 specification support. (well, almost).
  • CJK languages and vertical writing scripts support.
  • Various font types (Type1, TrueType, Type3, and CID) support.
  • Support for extracting images (JPG, JBIG2, Bitmaps).
  • Support for various compressions (ASCIIHexDecode, ASCII85Decode, LZWDecode,
    FlateDecode, RunLengthDecode, CCITTFaxDecode)
  • Support for RC4 and AES encryption.
  • Support for AcroForm interactive form extraction.
  • Table of contents extraction.
  • Tagged contents extraction.
  • Automatic layout analysis.}

%description %{common_description}


%package -n     python3-pdfminer
Summary:        %{summary}

# The import name is pdfminer. The upstream project name (as specified in
# setup.py) is pdfminer.six, which results in a canonical project name of
# pdfminer-six.
%py_provides python3-pdfminer-six

# One file, pdfminer/_saslprep.py, is forked from from ASL 2.0 code by MongoDB,
# Inc.—originally pymongo/saslprep.py in mongo-python-driver
# (python-pymongo)—with additional modifications in pyHanko (not yet packaged),
# where it is pyhanko/pdf_utils/_saslprep.py.
#
# Since this is a fork of the python-pymongo module, and since the fork is not
# part of pyHanko’s public API, there is no possibility of using an unbundled
# version.
#
# The version history of the fork is not clear. We add unversioned virtual
# Provides for both libraries of origin.
Provides:       bundled(python3dist(pymongo))
Provides:       bundled(python3dist(pyhanko))

# We no longer bother to build and install the PDF manual. Since we removed the
# -doc package for Fedora 43, this can be removed after Fedora 45.
Obsoletes:      python-pdfminer-doc < 20240706-4

%description -n python3-pdfminer %{common_description}


%pyproject_extras_subpkg -n python3-pdfminer image


%prep -a
# Unbundle cmap data; it will be replaced in %%build.
rm -vf cmaprsrc/* pdfminer/cmap/*

# Remove shebang line in non-script source
sed -r -i '1{/^#!/d}' pdfminer/psparser.py

# Copy the pyHanko license to the top-level directory so it is automatically
# included in the licenses in the installed dist-info directory.
cp -p docs/licenses/LICENSE.pyHanko ./


%build -p
# Symlink the unbundled CMap resources and convert to the compressed JSON
# format.
for cmap in Japan1 Korea1 GB1 CNS1
do
  ln -s "%{adobe_mappings_rootpath}/${cmap}/cid2code.txt" \
      "cmaprsrc/cid2code_Adobe_${cmap}.txt"
done
# Prior to release 20251229, there was a “cmap” Makefile target. It was
# removed, perhaps accidentally.
#
# %%make_build cmap PYTHON='%%{python3}'
#
# The following is equivalent to what the “cmap” target used to do.
mkdir -p pdfminer/cmap
%{python3} tools/conv_cmap.py -c B5=cp950 -c UniCNS-UTF8=utf-8 \
    pdfminer/cmap Adobe-CNS1 cmaprsrc/cid2code_Adobe_CNS1.txt
%{python3} tools/conv_cmap.py -c GBK-EUC=cp936 -c UniGB-UTF8=utf-8 \
    pdfminer/cmap Adobe-GB1 cmaprsrc/cid2code_Adobe_GB1.txt
%{python3} tools/conv_cmap.py -c RKSJ=cp932 -c EUC=euc-jp \
    -c UniJIS-UTF8=utf-8 \
    pdfminer/cmap Adobe-Japan1 cmaprsrc/cid2code_Adobe_Japan1.txt
%{python3} tools/conv_cmap.py -c KSC-EUC=euc-kr -c KSC-Johab=johab \
    -c KSCms-UHC=cp949 -c UniKS-UTF8=utf-8 \
    pdfminer/cmap Adobe-Korea1 cmaprsrc/cid2code_Adobe_Korea1.txt

# Make an updated git commit and set a tag for setuptools_git_version.
#
# Normally this kind of thing would be in %%prep, but we must do this
# immediately before building the wheel, and after any other changes such as
# rebuilding the compressed JSON CMap resources, lest setuptools_git_version
# determine that the tree is “dirty” and produce a “post” version, appearing in
# the binary RPMs as something like YYYYMMDD^post0.
#
# We *also* need to ensure that git ignores anything that might be written
# during %%pyproject_wheel, or we will still end up with a dirty/postrelease
# version.
echo '*pyproject*' >> .gitignore
git add -A
git commit -m 'Imitate upstream release %{version}'
git tag '%{version}'


# %%build -a
# Debug dynamic versioning:
# git status
# %%{python3} -m setuptools_git_versioning --verbose


%install -a
install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 \
    '%{SOURCE2}' '%{SOURCE3}'

%py3_shebang_fix '%{buildroot}%{_bindir}'

# Also, ship symlinks of the scripts without the .py extension.
for script in pdf2txt dumppdf
do
  ln -sf "${script}.py" "%{buildroot}%{_bindir}/${script}"
done


%check -a
# Skipped tests (and ignored files) are those that require the sample PDFs,
# which are not included in our version of the source tarball.
k="${k-}${k+ and }not TestColorSpace"
k="${k-}${k+ and }not TestDumpImages"
k="${k-}${k+ and }not TestDumpPDF"
k="${k-}${k+ and }not TestExtractPages"
k="${k-}${k+ and }not TestExtractText"
k="${k-}${k+ and }not TestOpenFilename"
k="${k-}${k+ and }not TestPdf2Txt"
k="${k-}${k+ and }not TestPdfDocument"
k="${k-}${k+ and }not TestPdfPage"
k="${k-}${k+ and }not test_cmap_font_12"
k="${k-}${k+ and }not test_font_size"
k="${k-}${k+ and }not test_paint_path_quadrilaterals"
k="${k-}${k+ and }not test_pdf_with_empty_characters_horizontal"
k="${k-}${k+ and }not test_pdf_with_empty_characters_vertical"
k="${k-}${k+ and }not (TestPaintPath and test_linewidth)"

ignore="${ignore-} --ignore=tests/test_tools_dumppdf.py"
ignore="${ignore-} --ignore=tests/test_tools_pdf2txt.py"

%pytest -k "${k-}" ${ignore-}


%files -n python3-pdfminer -f %{pyproject_files}
%doc CHANGELOG.md README.md

%{_bindir}/pdf2txt
%{_bindir}/pdf2txt.py
%{_mandir}/man1/pdf2txt.1*
%{_bindir}/dumppdf
%{_bindir}/dumppdf.py
%{_mandir}/man1/dumppdf.1*


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 20260107-2
- test: add initial lock files

* Wed Jan 07 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 20260107-1
- Update to 20260107 (close RHBZ#2427570)

* Wed Dec 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20251230-1
- Update to 20251230; Fixes RHBZ#2426287
- Security fix for CVE-2025-64512

* Tue Dec 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20251229-1
- Update to 20251229 (close RHBZ#2425927)

* Sun Dec 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20251228-1
- Update to 20251228 (close RHBZ#2425643)

* Fri Nov 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20251107-1
- Update to 20251107 (fixes RHBZ#2413443)
- Security fix for GHSA-wf5f-4jwr-ppcp

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 20250506-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 20250506-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20250506-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 20250506-2
- Rebuilt for Python 3.14

* Wed May 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250506-1
- Update to 20250506 (close RHBZ#2364455)

* Wed Apr 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250416-1
- Update to 20250416 (close RHBZ#2360105)

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250327-4
- Remove EPEL10 conditionals; the branch has already diverged anyway

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250327-3
- Rawhide/F43 now has setuptools with PEP 639 support

* Wed Apr 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250327-2
- Fix unversioned Python shebangs in %%install rather than %%prep

* Wed Apr 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250327-1
- Update to 20250327 (close RHBZ#2354478)

* Wed Apr 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20240706-5
- Use the provisional pyproject declarative buildsystem

* Wed Apr 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20240706-4
- F43+: No longer build PDF docs (simplify the package)
- The -doc subpackage is dropped and Obsoleted

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240706-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240706-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20240706-1
- Update to 20240706 (close RHBZ#2296104)

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 20231228-11
- Rebuilt for Python 3.13

* Thu Apr 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20231228-10
- Allow setuptools-git-versioning 2.x

* Fri Apr 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20231228-8
- Better preserve the timestamp information in the original source

* Thu Apr 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20231228-7
- Improve reproducibility of the filtered source archive

* Thu Apr 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20231228-6
- Use zstandard instead of xz for compressing the filtered source

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231228-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20231228-1
- Update to 20231228 (close RHBZ#2256142)

* Mon Dec 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-11
- Assert that %%pyproject_files contains a license file
- Copy the pyHanko license so it ends up in dist-info

* Sun Oct 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-9
- Break a long line in the spec file

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221105-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-7
- When PDF docs are disabled, omit the -doc subpackage
- Do not package CONTRIBUTING.md, which is about interacting with upstream

* Fri Jul 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-6
- Use new (rpm 4.17.1+) bcond style

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 20221105-5
- Rebuilt for Python 3.12

* Sat Mar 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-4
- Don’t assume %%_smp_mflags is -j%%_smp_build_ncpus

* Tue Mar 14 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-3
- Document that public-domain license text was added to fedora-license-data

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20221105-1
- Update to 20221105 (close RHBZ#2140331)

* Tue Nov 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220524-5
- Update License to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220524-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220524-3
- Fix extra newline in description

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 20220524-2
- Rebuilt for Python 3.11

* Thu May 26 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220524-1
- Update to 20220524 (close RHBZ#2089917)

* Sun May 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220506-2
- Replace sed-patch with upstream PR#755

* Sat May 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220506-1
- Update to 20220506 (close RHBZ#2082716)

* Mon Mar 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220319-2
- Generate BR for “image” extra even when docs are disabled

* Sun Mar 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220319-1
- Update to 20220319 (close RHBZ#2065998)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211012-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20211012-4
- Reduce LaTeX PDF build verbosity

* Mon Nov 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20211012-3
- Minor spec file style changes

* Mon Oct 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20211012-2
- Use %%%%python3 macro instead of %%%%__python3

* Tue Oct 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20211012-1
- Update to 20211012 (close RHBZ#1763506)

* Sun Oct 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20200517-12
- Another small man page fix

* Sun Oct 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20200517-11
- Man page typo fix

* Thu Oct 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20200517-10
- Use adobe_mappings_rootpath macro

* Thu Oct 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20200517-9
- Add BSD to the base License field; make -doc MIT only

* Thu Oct 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 20200517-8
- Comprehensive packaging improvements
- Switch to pyproject-rpm-macros (“new guidelines”)
- Do not distribute questionably-licensed sample PDFs, and skip the tests
  that require them
- Build PDF documentation in a new -doc subpackage (instead of simply
  distributing the documentation sources)
- Correct License field from “MIT” to “MIT and Public Domain and APAFML”
- Add downstream man pages for command-line tools
- Switch cmap-resources BR to adobe-mappings-cmap

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200517-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 20200517-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200517-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200517-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 20200517-1
- Update to latest version

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 20181108-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20181108-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 20181108-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 20181108-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181108-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 20181108-1
- Update to latest version
- Enable tests
- Fix crypto dependency
- Switch to automatic Requires
- Drop Python 2 subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170720-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Ben Rosser <rosser.bjr@gmail.com> - 20170720-7
- Stop package from using 'python' to run cmap script.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 20170720-6
- Rebuilt for Python 3.7

* Tue May 22 2018 Ben Rosser <rosser.bjr@gmail.com> - 20170720-5
- Rebuild against new cmap resources package.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170720-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 20170720-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Ben Rosser <rosser.bjr@gmail.com> - 20170720-1
- Update to latest upstream release.

* Fri Apr 21 2017 Ben Rosser <rosser.bjr@gmail.com> - 20170419-1
- Update to latest upstream release, fixing a logging bug from 20170418.

* Fri Apr 21 2017 Ben Rosser <rosser.bjr@gmail.com> - 20170418-2
- Now that upstream patch removing chbangs was merged, don't chmod library files.

* Wed Apr 19 2017 Ben Rosser <rosser.bjr@gmail.com> - 20170418-1
- Updated to latest upstream release.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160614-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 20160614-6
- Rebuild for Python 3.6

* Sat Oct 22 2016 Ben Rosser <rosser.bjr@gmail.com> - 20160614-5
- Add missing requires on python-six and python-chardet.

* Fri Sep  9 2016 Ben Rosser <rosser.bjr@gmail.com> - 20160614-4
- Rebuild against latest cmap-resources.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20160614-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 21 2016 Ben Rosser <rosser.bjr@gmail.com> 20160614-2
- I forgot to actually apply the patch to remove chbangs from library files. Apply said patch.

* Tue Jun 14 2016 Ben Rosser <rosser.bjr@gmail.com> 20160614-1
- Update to latest upstream version of package.
- Use local version of patch.

* Sat Feb 27 2016 Ben Rosser <rosser.bjr@gmail.com> 20160202-3
- Added a patch to remove the chbangs from all library files.
- Write correct sed command to make python3 scripts run with python3.

* Sat Feb 27 2016 Ben Rosser <rosser.bjr@gmail.com> 20160202-2
- Through the use of some gratuitious sed, the python2 package only depends on /usr/bin/python2.
- The python3 version is still a little weird; it pulls in /usr/bin/python and I'm not sure why.
- Also, make the python 3 scripts be the default ones.

* Fri Feb 26 2016 Ben Rosser <rosser.bjr@gmail.com> 20160202-1
- Update to latest upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151013-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 1 2016 Ben Rosser <rosser.bjr@gmail.com> 20151013-5
- Version bump to silence rpmlint.

* Fri Jan 1 2016 Ben Rosser <rosser.bjr@gmail.com> 20151013-4
- Upgrade path; obsolete and provide the pdfminer-six package in the COPR.
- Now replace the original python-pdfminer package with this one.

* Fri Jan 1 2016 Ben Rosser <rosser.bjr@gmail.com> 20151013-3
- Upgrade path; obsolete and provide python-pdfminer up until rawhide.

* Sat Dec 19 2015 Ben Rosser <rosser.bjr@gmail.com> 20151013-2
- Ship symlinks of the pdfminer scripts without the .py suffix.

* Fri Dec 18 2015 Ben Rosser <rosser.bjr@gmail.com> - 20151013-1
- Initial package of the pdfminer.six fork using pyp2rpm.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140328-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 23 2014 Ben Rosser <rosser.bjr@gmail.com> 20140328-2
- Replaced /usr/bin with bindir macro in install section.

* Sat Aug 16 2014 Ben Rosser <rosser.bjr@gmail.com> 20140328-1
- Updated to latest version of pdfminer.
- Changed specfile to depend on the correct cmap-* packages.

* Thu Sep 20 2012 Ben Rosser <rosser.bjr@gmail.com> 20110515-4
- Removed bundled cmap, changed to depend on cmap package instead

* Thu Jul 05 2012 Ben Rosser <rosser.bjr@gmail.com> 20110515-3
- Removed BuildRoot, clean, and first line of install
- Fixed issue with cmap data not being copied into package
- Fixed license (cmap is under BSD, not MIT)

* Tue May 22 2012 Ben Rosser <rosser.bjr@gmail.com> 20110515-2
- Fixed unowned directory issue and cleaned up the spec file

* Fri May 18 2012 Ben Rosser <rosser.bjr@gmail.com> 20110515-1
- Initial version of the package

## END: Generated by rpmautospec
