#
# spec file for package byaccj
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%global jpp_release 3

Summary:        Parser Generator with Java Extension
Name:           byaccj
Version:        1.14
Release:        26%{?dist}
License:        Public Domain
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            http://byaccj.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}%{version}_src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       man-pages

%description
BYACC/J is an extension of the Berkeley v 1.8 YACC-compatible parser
generator. Standard YACC takes a YACC source file, and generates one or
more C files from it, which if compiled properly, will produce a
LALR-grammar parser. This is useful for expression parsing, interactive
command parsing, and file reading. Many megabytes of YACC code have
been written over the years. This is the standard YACC tool that is in
use every day to produce C/C++ parsers. I have added a "-J" flag which
will cause BYACC to generate Java source code, instead. So there
finally is a YACC for Java now!

%prep
%setup -q -n %{name}%{version}_src

%build
pushd src
make linux CFLAGS="$RPM_OPT_FLAGS"
popd
sed -i 's/\r//g' docs/tf.y

%install
# manual
install -d -m 755 %{buildroot}%{_mandir}/man1
mv docs/yacc.cat %{buildroot}%{_mandir}/man1
# jars
mkdir -p %{buildroot}%{_bindir}
cp -p src/yacc.linux \
  %{buildroot}%{_bindir}/%{name}

%files
%defattr(0644,root,root,0755)
%license src/readme
%doc docs/* src/README
%{_mandir}/man1/yacc.cat*
%attr(755, root, root) %{_bindir}/%{name}

%changelog
* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.14-26
- Move to SPECS
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14-25
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 1.14-24.20
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Fix linebreak in sed command.

* Tue Jan  7 2014 schwab@suse.de
- Build with $RPM_OPT_FLAGS
* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile
* Sat Apr 25 2009 mvyskocil@suse.cz
- created package
