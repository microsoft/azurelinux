## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           msopenjdk-25-fedora-compat
Version:        25.0.4.1
Release:        %autorelease
Summary:        Fedora compatibility aliases for Microsoft Build of OpenJDK 25
License:        MIT
URL:            https://aka.ms/openjdk
ExclusiveArch:  x86_64 aarch64

%global jvmdir %{_prefix}/lib/jvm
%global provider_cacerts %{jvmdir}/msopenjdk-25/lib/security/cacerts
%global provider_cacerts_backup %{provider_cacerts}.upstream
%global system_cacerts %{_sysconfdir}/pki/java/cacerts

# Removing Fedora OpenJDK 25 from the repositories does not uninstall its RPMs.
# Obsolete every package shipped in PMC so upgrades remove the retired provider.
Obsoletes:      java-25-openjdk < 1:26
Obsoletes:      java-25-openjdk-demo < 1:26
Obsoletes:      java-25-openjdk-demo-fastdebug < 1:26
Obsoletes:      java-25-openjdk-devel < 1:26
Obsoletes:      java-25-openjdk-devel-fastdebug < 1:26
Obsoletes:      java-25-openjdk-fastdebug < 1:26
Obsoletes:      java-25-openjdk-headless < 1:26
Obsoletes:      java-25-openjdk-headless-fastdebug < 1:26
Obsoletes:      java-25-openjdk-javadoc < 1:26
Obsoletes:      java-25-openjdk-javadoc-zip < 1:26
Obsoletes:      java-25-openjdk-jmods < 1:26
Obsoletes:      java-25-openjdk-jmods-fastdebug < 1:26
Obsoletes:      java-25-openjdk-src < 1:26
Obsoletes:      java-25-openjdk-src-fastdebug < 1:26
Obsoletes:      java-25-openjdk-static-libs < 1:26
Obsoletes:      java-25-openjdk-static-libs-fastdebug < 1:26
Conflicts:      java-25-openjdk%{?_isa}
Conflicts:      java-25-openjdk-headless%{?_isa}
Conflicts:      java-25-openjdk-devel%{?_isa}

Provides:       java-25-openjdk = 1:%{version}-%{release}
Provides:       java-25 = 1:%{version}-%{release}
Provides:       java-openjdk = 1:%{version}-%{release}
Provides:       java = 1:%{version}-%{release}
Provides:       jre-25-openjdk = 1:%{version}-%{release}
Provides:       jre-25 = 1:%{version}-%{release}
Provides:       jre-openjdk = 1:%{version}-%{release}
Provides:       jre = 1:%{version}-%{release}
Provides:       java-25-openjdk-headless = 1:%{version}-%{release}
Provides:       java-25-headless = 1:%{version}-%{release}
Provides:       java-openjdk-headless = 1:%{version}-%{release}
Provides:       java-headless = 1:%{version}-%{release}
Provides:       jre-25-openjdk-headless = 1:%{version}-%{release}
Provides:       jre-25-headless = 1:%{version}-%{release}
Provides:       jre-openjdk-headless = 1:%{version}-%{release}
Provides:       jre-headless = 1:%{version}-%{release}
Provides:       libjawt.so()(64bit)
Provides:       java-sdk-25-openjdk = 1:%{version}-%{release}
Provides:       java-sdk-25 = 1:%{version}-%{release}
Provides:       java-25-devel = 1:%{version}-%{release}
Provides:       java-25-openjdk-devel = 1:%{version}-%{release}
Provides:       java-devel-openjdk = 1:%{version}-%{release}
Provides:       java-sdk-openjdk = 1:%{version}-%{release}
Provides:       java-devel = 1:%{version}-%{release}
Provides:       java-sdk = 1:%{version}-%{release}

# Suggest system trust and Fedora compatibility for direct provider installs.
# Weak dependencies may be disabled; runtime consumers must still require compat.
Supplements:    msopenjdk-25

Requires:       msopenjdk-25%{?_isa} >= %{version}-1
Requires:       javapackages-filesystem
Requires:       ca-certificates
Requires:       coreutils
# classloader-leak-test-framework fails its Swing test when Microsoft Build of
# OpenJDK cannot load libfreetype.so.6 or initialize the system font configuration.
Requires:       freetype
Requires:       fontconfig
Requires:       xorg-x11-fonts-Type1
Requires:       libX11
Requires:       libXcomposite
Requires:       libXext
Requires:       libXi
Requires:       libXrender
Requires:       libXtst
Requires(posttrans): /usr/sbin/alternatives
Requires(posttrans): /usr/bin/find
Requires(preun): /usr/sbin/alternatives

%description
Compatibility package that exposes Microsoft Build of OpenJDK 25 through
Fedora-compatible Java capabilities and JVM directory alternatives. It contains
no Java runtime files.

%install
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
printf '%s\n' 'Fedora compatibility aliases for msopenjdk-25.' > %{buildroot}%{_datadir}/doc/%{name}/README
mkdir -p %{buildroot}%{_libdir}
ln -s %{jvmdir}/msopenjdk-25/lib/libjawt.so %{buildroot}%{_libdir}/libjawt.so

%posttrans
# JSSE reads java.home/lib/security/cacerts by default, but the Microsoft RPM
# ships a private store that update-ca-trust does not refresh. Preserve that
# store and use AZL's system-managed Java trust store instead. Remove this
# integration once msopenjdk-25 packages this symlink itself.
if [ ! -L %{provider_cacerts} ]; then
    mv -f %{provider_cacerts} %{provider_cacerts_backup} || exit 1
fi
ln -sfn %{system_cacerts} %{provider_cacerts} || exit 1

# Fedora OpenJDK removal can leave empty directories that block the alternatives symlink.
find %{jvmdir}/java-25-openjdk -depth -type d -empty -delete 2>/dev/null || :
# Fedora-built consumers expect the generic paths /usr/lib/jvm/jre and /usr/lib/jvm/java,
# but msopenjdk-25 installs the JDK only under /usr/lib/jvm/msopenjdk-25.
# Remove the followers once msopenjdk-25 owns them.
alternatives --add-follower java %{jvmdir}/msopenjdk-25/bin/java %{jvmdir}/jre jre %{jvmdir}/msopenjdk-25
alternatives --add-follower javac %{jvmdir}/msopenjdk-25/bin/javac %{jvmdir}/java java_sdk %{jvmdir}/msopenjdk-25
alternatives --install %{jvmdir}/java-25-openjdk java_sdk_25_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/java-25 java_sdk_25 %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/java-openjdk java_sdk_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-25-openjdk jre_25_openjdk %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-25 jre_25 %{jvmdir}/msopenjdk-25 2511
alternatives --install %{jvmdir}/jre-openjdk jre_openjdk %{jvmdir}/msopenjdk-25 2511
exit 0

%triggerin -- msopenjdk-25
# Provider updates replace the trust-store symlink with their bundled file.
# Preserve the updated file and restore the system trust-store connection.
if [ ! -L %{provider_cacerts} ]; then
    mv -f %{provider_cacerts} %{provider_cacerts_backup} || exit 1
fi
ln -sfn %{system_cacerts} %{provider_cacerts} || exit 1

# The provider's %post rewrites these alternatives entries without compat's
# followers. Restore them after every provider installation or upgrade.
alternatives --add-follower java %{jvmdir}/msopenjdk-25/bin/java %{jvmdir}/jre jre %{jvmdir}/msopenjdk-25
alternatives --add-follower javac %{jvmdir}/msopenjdk-25/bin/javac %{jvmdir}/java java_sdk %{jvmdir}/msopenjdk-25
exit 0

%preun
if [ $1 -eq 0 ]; then
    alternatives --remove-follower java %{jvmdir}/msopenjdk-25/bin/java jre
    alternatives --remove-follower javac %{jvmdir}/msopenjdk-25/bin/javac java_sdk
    alternatives --remove java_sdk_25_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove java_sdk_25 %{jvmdir}/msopenjdk-25
    alternatives --remove java_sdk_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove jre_25_openjdk %{jvmdir}/msopenjdk-25
    alternatives --remove jre_25 %{jvmdir}/msopenjdk-25
    alternatives --remove jre_openjdk %{jvmdir}/msopenjdk-25
    # Final compat removal must leave msopenjdk-25 in its original state:
    # replace our system-store symlink with the provider's preserved store.
    if [ -L %{provider_cacerts} ] && [ -f %{provider_cacerts_backup} ]; then
        rm -f %{provider_cacerts}
        mv -f %{provider_cacerts_backup} %{provider_cacerts}
    fi
fi
exit 0

%files
%ghost %{jvmdir}/java
%ghost %{jvmdir}/java-25-openjdk
%ghost %{jvmdir}/java-25
%ghost %{jvmdir}/java-openjdk
%ghost %{jvmdir}/jre
%ghost %{jvmdir}/jre-25-openjdk
%ghost %{jvmdir}/jre-25
%ghost %{jvmdir}/jre-openjdk
%{_libdir}/libjawt.so
%{_datadir}/doc/%{name}/README

%changelog
## START: Generated by rpmautospec
* Thu Sep 17 2026 Nan Liu <liunan@microsoft.com> - 25.0.4.1-2
- feat(java): migrate to Microsoft OpenJDK 25

* Thu Jan 01 1970 azldev <> - 25.0.4.1-1
- Initial sources
## END: Generated by rpmautospec
