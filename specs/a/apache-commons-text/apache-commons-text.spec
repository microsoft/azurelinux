# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global jarname commons-text

Name:           apache-%{jarname}
Version:        1.10.0
Release:        13%{?dist}
Summary:        Apache Commons Text is a library focused on algorithms working on strings
License:        Apache-2.0
URL:            https://commons.apache.org/proper/%{jarname}
BuildArch:      noarch

Source0:        https://archive.apache.org/dist/commons/text/source/%{jarname}-%{version}-src.tar.gz
Source1:        https://archive.apache.org/dist/commons/text/source/%{jarname}-%{version}-src.tar.gz.asc
Source2:        https://archive.apache.org/dist/commons/KEYS
# disable url lookup in test
Patch0:         0001-disable-url-lookup.patch

BuildRequires:  gnupg2
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.mockito:mockito-core)

%description
The Commons Text library provides additions to the standard JDK's text handling.
Our goal is to provide a consistent set of tools for processing text generally
from computing distances between Strings to being able to efficiently do String
escaping of various types.

%{?javadoc_package}

%prep
# verify signed sources
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

# -p1: strip one level directory in patch(es)
# -n: base directory name
%autosetup -p1 -n %{jarname}-%{version}-src
# there are non-utf chars, and patch, sed, awk, iconv, enca... are failing to fix it. Replacing it manually:
evil=src/main/java/org/apache/commons/text/translate/EntityArrays.java
echo "//reworked"  > $evil.nw
while read -r line; do 
  if  echo "$line" | grep -qe "&Aring;" ; then
    echo  'initialMap.put("\u00C5", "&Aring;"); // this line was changed by specfile' >> $evil.nw
  else
    echo  "$line" >> $evil.nw
  fi
done < $evil
mv $evil.nw $evil

# delete precompiled jar and class files
find -type f '(' -name '*.jar' -o -name '*.class' ')' -print -delete

# mockito-inline was merged into mockito-core
%pom_change_dep :mockito-inline :mockito-core

%build
# disable test: some test deps can't be installed
%mvn_build -f -- -Dmaven.compiler.release=8

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc README.md RELEASE-NOTES.txt

%changelog
* Wed Jul 30 2025 jiri vanek <jvanek@redhat.com> - 1.10.0-11
- Rrevert to jdk21

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.10.0-10
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.10.0-6
- Rebuilt for java-21-openjdk as system jdk

* Thu Feb 01 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.0-5
- Port to mockito 5.8.0

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 24 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.10.0-1
- Update to version 1.10.0
- Disable tests

* Sat Apr 29 2023 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.9-5
- migrated to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 23 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.9-2
- Add BR on mockito-inline
- Patch the test files to disable url lookup
- Use maven-local-openjdk11 to be able to compile test files
- Reverse the order of %%autosetup and %%gpgverify

* Wed Jul 21 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.9-1
- Initial package
