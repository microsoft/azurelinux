Summary:        Exuberant Ctags - a multi-language source code indexing tool
Name:           ctags
Version:        5.8
Release:        5%{?dist}
License:        GPL
URL:            http://ctags.sourceforge.net
Source:         http://prdownloads.sourceforge.net/ctags/ctags-%{version}.tar.gz
%define sha1 ctags=482da1ecd182ab39bbdc09f2f02c9fba8cd20030
Group:          Development/Tools
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Vendor:         Microsoft Corporation
Distribution:   Mariner

Patch0:         ctags-fix-format-security.patch

%description
Exuberant Ctags generates an index (or tag) file of language objects
found in source files for many popular programming languages. This index
makes it easy for text editors and other tools to locate the indexed
items. Exuberant Ctags improves on traditional ctags because of its
multilanguage support, its ability for the user to define new languages
searched by regular expressions, and its ability to generate emacs-style
TAGS files.

%prep
%setup -q
%patch0 -p1

%build
%configure
make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/ctags
%{_mandir}/man1/ctags*

%changelog
*   Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.8-5
-   Add patch to fix format-security errors.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.8-4
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5.8-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.8-2
-	GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
