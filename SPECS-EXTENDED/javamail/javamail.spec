Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package javamail
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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


%global git_tag JAVAMAIL-1_5_2
Name:           javamail
Version:        1.5.2
Release:        3%{?dist}
Summary:        Java Mail API
License:        CDDL-1.0 OR GPL-2.0-only WITH Classpath-exception-2.0
Group:          Development/Libraries/Java
URL:            http://www.oracle.com/technetwork/java/javamail
Source:         https://github.com/javaee/javamail/archive/%{git_tag}.tar.gz
Patch0:         %{name}-javadoc.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  perl-XML-XPath
# Adapted from the classpathx-mail (and JPackage glassfish-javamail) Provides.
Provides:       javamail-monolithic = %{version}-%{release}
Provides:       javax.mail
BuildArch:      noarch

%description
The JavaMail API provides a platform-independent and protocol-independent
framework to build mail and messaging applications.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{git_tag}
%patch0 -p1

add_dep() {
    %pom_xpath_inject pom:project "<dependencies/>" ${2}
    %pom_add_dep com.sun.mail:${1}:%{version}:provided ${2}
}

add_dep smtp mailapi
add_dep javax.mail smtp
add_dep javax.mail pop3
add_dep javax.mail imap
add_dep javax.mail mailapijar

# Remove profiles containing demos and other stuff that is not
# supposed to be deployable.
%pom_xpath_remove /pom:project/pom:profiles

# osgiversion-maven-plugin is used to set ${mail.osgiversion} property
# based on ${project.version}. We don't have osgiversion plugin so we
# will set ${mail.osgiversion} explicitly.
%pom_remove_plugin org.glassfish.hk2:osgiversion-maven-plugin
%pom_remove_dep javax.activation:activation
%pom_xpath_inject /pom:project/pom:properties "<mail.osgiversion>%{version}</mail.osgiversion>"
%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>"

# Tests failing due to networking limitations
rm mail/src/test/java/com/sun/mail/imap/IMAPIdleUntaggedResponseTest.java
rm mail/src/test/java/com/sun/mail/smtp/SMTPWriteTimeoutTest.java

%pom_remove_parent .

%build
%{ant} -Djavac.source=1.6 -Djavac.target=1.6 jar jars docs

%install
get_name() {
    xpath -q -e '/project/artifactId/text()' ${1}
}

# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/release/mail.jar %{buildroot}%{_javadir}/%{name}/$(get_name mail/pom.xml).jar
for i in mailapi smtp imap gimap pop3 dsn; do
  install -pm 0644 target/release/lib/${i}.jar %{buildroot}%{_javadir}/%{name}/$(get_name ${i}/pom.xml).jar
done
install -pm 0644 target/release/lib/mailapi.jar %{buildroot}%{_javadir}/%{name}/$(get_name mailapijar/pom.xml).jar
ln -sf javax.mail.jar %{buildroot}%{_javadir}/%{name}/mail.jar
ln -sf %{name}/javax.mail.jar  %{buildroot}%{_javadir}/javax.mail.jar
install -d -m 755 %{buildroot}%{_javadir}/javax.mail/
ln -sf ../%{name}/javax.mail.jar %{buildroot}%{_javadir}/javax.mail/

# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/$(get_name pom.xml).pom
pompart=%{name}/$(get_name pom.xml).pom
%add_maven_depmap ${pompart}
for i in mailapijar smtp imap gimap pop3 dsn; do
  install -pm 0644 ${i}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/$(get_name ${i}/pom.xml).pom
  pompart=%{name}/$(get_name ${i}/pom.xml).pom
  jarpart=%{name}/$(get_name ${i}/pom.xml).jar
  %add_maven_depmap ${pompart} ${jarpart}
done
install -pm 0644 mail/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/$(get_name mail/pom.xml).pom
pompart=%{name}/$(get_name mail/pom.xml).pom
jarpart=%{name}/$(get_name mail/pom.xml).jar
%add_maven_depmap ${pompart} ${jarpart} -a javax.mail:mail,org.eclipse.jetty.orbit:javax.mail.glassfish
install -pm 0644 mailapi/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/$(get_name mailapi/pom.xml).pom
pompart=%{name}/$(get_name mailapi/pom.xml).pom
jarpart=%{name}/$(get_name mailapi/pom.xml).jar
%add_maven_depmap ${pompart} ${jarpart} -a javax.mail:mailapi

# javadoc
mkdir -p %{buildroot}%{_javadocdir}
cp -pr target/release/docs %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc mail/src/main/java/overview.html
%license mail/src/main/resources/META-INF/LICENSE.txt
%{_javadir}/javax.mail
%{_javadir}/javax.mail.jar
%{_javadir}/%{name}/mail.jar

%files javadoc
%{_javadocdir}/%{name}
%license mail/src/main/resources/META-INF/LICENSE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.2-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.5.2-2.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Remove suse_version check.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the jvnet-parent pom since we are not building
  with maven
* Tue Jan 22 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of javamail 1.5.2
- Install as maven artifacts
