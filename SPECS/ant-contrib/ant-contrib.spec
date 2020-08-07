Summary:        Ant contrib
Name:           ant-contrib
Version:        1.0b3
Release:        18%{?dist}
License:        ASL 1.1
URL:            https://ant-contrib.sourceforge.net
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch

Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}-src.tar.gz

BuildRequires:  openjre8
BuildRequires:  openjdk8
BuildRequires:  ant
Requires:       openjre8
Requires:       ant

%define _prefix /var/opt/ant-contrib

%description
The Ant Contrib project is a collection of tasks for Apache Ant.

%prep
%setup -n %{name}
find . -name '*.jar' -or -name '*.class' -exec rm -rf {} +

%clean
rm -rf %{buildroot}

%build
export JAVA_HOME=$(find /usr/lib/jvm -name "OpenJDK*")
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")
ant -Ddist.dir="." -Dproject.version=%{version} dist

%install
mkdir -p -m 700 %{buildroot}/var/opt
cd %{buildroot}/var/opt && tar xvzf %{_builddir}/%{name}/%{name}-%{version}-bin.tar.gz --wildcards "*.jar"
%files
%defattr(-,root,root)
%license docs/LICENSE.txt
%dir %{_prefix}
%dir %{_prefix}/lib
%{_prefix}/*.jar
%{_prefix}/lib/*.jar

%changelog
* Sat May 09 00:20:49 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.0b3-18
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.0b3-17
-   Renaming apache-ant to ant
*   Fri Apr 24 2020 Nicolas Guibourge <nicolasg@microsoft.com> 1.0b3-16
-   Add path to libjli.so in LD_LIBRARY_PATH
*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 1.0b3-15
-   Fix URL.
-   Update License.
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0b3-14
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.0b3-13
-   Removed dependency on JAVA8_VERSION macro
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-12
-   Removed dependency on ANT_HOME
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3-11
-   Renamed openjdk to openjdk8
*   Fri Apr 07 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-10
-   Removed prebuilt binaries from source tar ball
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-9
-   Updated JAVA_HOME path to point to latest.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-8
-   Updated JAVA_HOME path to point to latest.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-7
-	GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 1.0b3-6
-   Updated JAVA_HOME path to point to latest.
*   Wed Mar 02 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-5
-   Updated apache-ant to version 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0b3.0-4
-   Updated JAVA_HOME path to point to latest.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.0b3.0-2
-   Change path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-1
-   Updated dependencies after repackaging openjdk.
*   Tue Jun 9 2015 Sriram Nambakam <snambakam@vmware.com> 1.0b3.0-0
-   Initial commit
