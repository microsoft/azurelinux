Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global tag_version release-%%(echo "%version" | tr '~' '-' | tr '.' '-')
#%%global is_official 0%%(echo %%{tag_version} | grep -qE 'alpha|beta|final'; echo $?)
#%%global is_official 0
%global is_official 0

Name:       cldr-emoji-annotation
Version:    46.1~beta2
Release:    2%{?dist}
%if 0%{?fedora:1}%{?rhel:0}
Epoch:      1
%endif
# Annotation files are in Unicode license
Summary:    Emoji annotation files in CLDR
License:    Unicode-DFS-2016
URL:        https://unicode.org/cldr
%if %is_official
Source0:    https://github.com/unicode-org/cldr/releases/download/%{tag_version}/cldr-core-%{version}.zip
%else
Source0:    https://github.com/unicode-org/cldr/archive/refs/tags/%{tag_version}.zip#/cldr-%{tag_version}.zip
%endif
#Patch0:     %%{name}-HEAD.patch
BuildRequires: autoconf
BuildRequires: automake
BuildArch:  noarch
Requires:  %{name}-dtd

%description
This package provides the emoji annotation file by language in CLDR.

%package dtd
Summary:    DTD files of CLDR common
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:  noarch

%description dtd
This package contains DTD files of CLDR common which are required by
cldr-emoji-annotations.

%package devel
Summary:    Files for development using cldr-annotations
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   pkgconfig
BuildArch:  noarch

%description devel
This package contains the pkg-config files for development
when building programs that use cldr-emoji-annotations.


%prep
%if %is_official
%autosetup -c -n cldr-%{tag_version}
%else
%autosetup -n cldr-%{tag_version}
%endif


%install
pushd $PWD
ANNOTATION_DIR=common/annotations
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
pushd $ANNOTATION_DIR
for xml in *.xml ; do
    install -pm 644 -D $xml $RPM_BUILD_ROOT$CLDR_DIR/$xml
done
popd

ANNOTATION_DIR=common/annotationsDerived
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
pushd $ANNOTATION_DIR
for xml in *.xml ; do
    install -pm 644 -D $xml $RPM_BUILD_ROOT$CLDR_DIR/$xml
done
popd

DTD_DIR=common/dtd
CLDR_DIR=%{_datadir}/unicode/cldr/$DTD_DIR
pushd $DTD_DIR
for dtd in *.dtd ; do
    install -pm 644 -D $dtd $RPM_BUILD_ROOT$CLDR_DIR/$dtd
done
popd

install -pm 755 -d $RPM_BUILD_ROOT%{_datadir}/pkgconfig
cat >> $RPM_BUILD_ROOT%{_datadir}/pkgconfig/%{name}.pc <<_EOF
prefix=/usr

Name: cldr-emoji-annotations
Description: annotation files in CLDR
Version: %{version}
_EOF


%check
ANNOTATION_DIR=common/annotations
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
for xml in $ANNOTATION_DIR/*.xml ; do
    xmllint --noout --valid --postvalid $xml
done

ANNOTATION_DIR=common/annotationsDerived
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
for xml in $ANNOTATION_DIR/*.xml ; do
    xmllint --noout --valid --postvalid $xml
done


%files
%if %is_official
%doc README-common.md
%license LICENSE.txt
%else
%doc README.md
%license LICENSE
%endif
%{_datadir}/unicode/cldr/common/annotations
%{_datadir}/unicode/cldr/common/annotationsDerived

%files dtd
%dir %{_datadir}/unicode
%dir %{_datadir}/unicode/cldr
%dir %{_datadir}/unicode/cldr/common
%{_datadir}/unicode/cldr/common/dtd

%files devel
%{_datadir}/pkgconfig/*.pc

%changelog
* Tue Dec 17 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 46.1~beta2-2
- Azurelinux import from Fedora 41 (license: MIT).
- License verified

