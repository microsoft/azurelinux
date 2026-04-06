## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 14;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           flexmark-java
Version:        0.64.6
Release:        %autorelease
Summary:        CommonMark/Markdown Java parser with source level AST

# Some test files carry the Apache-2.0 or CC-BY-SA-4.0 licenses, but we do not
# ship those files.
# Some files claim to be private property of the copyright holder, but upstream
# has stated that this is a mistake and that claim will be removed.  See:
# https://github.com/vsch/flexmark-java/issues/443
# https://github.com/vsch/flexmark-java/pull/590
License:        BSD-2-Clause
URL:            https://github.com/vsch/flexmark-java
VCS:            git:%{url}.git
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# https://github.com/vsch/flexmark-java/pull/635
Patch:          0001-Fix-abbreviations-matching-with-Java-19.patch
# Fix issue with native images
Patch:          %{url}/pull/578.patch
# Adapt to changes in jsoup >= 1.20
Patch:          %{name}-jsoup.patch

BuildArch:      noarch
ExclusiveArch:  noarch %{java_arches}

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-1.2-api)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-api)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-core)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.jetbrains:annotations)
BuildRequires:  mvn(org.jsoup:jsoup)
BuildRequires:  mvn(org.nibor.autolink:autolink)
BuildRequires:  mvn(org.slf4j:slf4j-api)

Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-builder = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-dependency = %{version}-%{release}
Requires:       %{name}-util-format = %{version}-%{release}
Requires:       %{name}-util-html = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}
Requires:       %{name}-util-visitor = %{version}-%{release}

%global _desc %{expand:
Flexmark-java is a Java CommonMark (spec 0.28) parser using the blocks
first, inlines after Markdown parsing architecture.

Its strengths are speed, flexibility, Markdown source element based AST
with details of the source position down to individual characters of
lexemes that make up the element and extensibility.

The API allows granular control of the parsing process and is optimized
for parsing with a large number of installed extensions.  The parser and
extensions come with plenty of options for parser behavior and HTML
rendering variations.  The end goal is to have the parser and renderer
be able to mimic other parsers with great degree of accuracy.  This is
now partially complete with the implementation of Markdown Processor
Emulation.}

%description %_desc

This package contains the core library for parsing markdown and
rendering to HTML.

%{?javadoc_package}

%package        all
Summary:        All flexmark extension and converter modules
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-abbreviation = %{version}-%{release}
Requires:       %{name}-ext-admonition = %{version}-%{release}
Requires:       %{name}-ext-anchorlink = %{version}-%{release}
Requires:       %{name}-ext-aside = %{version}-%{release}
Requires:       %{name}-ext-attributes = %{version}-%{release}
Requires:       %{name}-ext-autolink = %{version}-%{release}
Requires:       %{name}-ext-definition = %{version}-%{release}
Requires:       %{name}-ext-emoji = %{version}-%{release}
Requires:       %{name}-ext-enumerated-reference = %{version}-%{release}
Requires:       %{name}-ext-escaped-character = %{version}-%{release}
Requires:       %{name}-ext-footnotes = %{version}-%{release}
Requires:       %{name}-ext-gfm-issues = %{version}-%{release}
Requires:       %{name}-ext-gfm-strikethrough = %{version}-%{release}
Requires:       %{name}-ext-gfm-tasklist = %{version}-%{release}
Requires:       %{name}-ext-gfm-users = %{version}-%{release}
Requires:       %{name}-ext-gitlab = %{version}-%{release}
Requires:       %{name}-ext-jekyll-front-matter = %{version}-%{release}
Requires:       %{name}-ext-jekyll-tag = %{version}-%{release}
Requires:       %{name}-ext-media-tags = %{version}-%{release}
Requires:       %{name}-ext-resizable-image = %{version}-%{release}
Requires:       %{name}-ext-macros = %{version}-%{release}
Requires:       %{name}-ext-ins = %{version}-%{release}
Requires:       %{name}-ext-xwiki-macros = %{version}-%{release}
Requires:       %{name}-ext-superscript = %{version}-%{release}
Requires:       %{name}-ext-tables = %{version}-%{release}
Requires:       %{name}-ext-toc = %{version}-%{release}
Requires:       %{name}-ext-typographic = %{version}-%{release}
Requires:       %{name}-ext-wikilink = %{version}-%{release}
Requires:       %{name}-ext-yaml-front-matter = %{version}-%{release}
Requires:       %{name}-ext-youtube-embedded = %{version}-%{release}
Requires:       %{name}-html2md-converter = %{version}-%{release}
Requires:       %{name}-jira-converter = %{version}-%{release}
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-builder = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-dependency = %{version}-%{release}
Requires:       %{name}-util-format = %{version}-%{release}
Requires:       %{name}-util-html = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-options = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}
Requires:       %{name}-util-visitor = %{version}-%{release}
Requires:       %{name}-youtrack-converter = %{version}-%{release}

%description    all %_desc

This package provides all of the extension and converter modules.

%package        ext-abbreviation
Summary:        Flexmark extension for abbreviations in text
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-autolink = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-abbreviation %_desc

This package contains an extension for defining abbreviations and
turning appearance of these abbreviations in text into <abbr> tags with
titles consisting of the expansion of the abbreviation.

%package        ext-admonition
Summary:        Flexmark extension for admonition syntax processing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-admonition %_desc

This package contains an extension for Admonition Extension, Material
for MkDocs syntax processing, to create block-styled side content.

%package        ext-anchorlink
Summary:        Flexmark extension to generate anchor links for headers
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-anchorlink %_desc

This package contains an extension for generating anchor links for
headings using a GitHub-compatible ID algorithm, with options for the
rendered HTML tags.

%package        ext-aside
Summary:        Flexmark extension for converting | to aside tags
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-jira-converter = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-aside %_desc

This package contains an extension for converting text prefixed with `|`
to aside tags.  The syntax is the same as block quotes with the marker
changed to `|`.

%package        ext-attributes
Summary:        Flexmark extension for attributes
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-attributes %_desc

This package contains an extension that converts attribute syntax
(`{...}`) into attribute AST nodes and adds an attribute provider to set
attributes for the immediately preceding sibling element during HTML
rendering.

%package        ext-autolink
Summary:        Flexmark extension for autolinking
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-autolink %_desc

This package contains an extension for turning plain URLs and email
addresses into links.

%package        ext-definition
Summary:        Flexmark extension for definition list processing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-definition %_desc

This package contains an extension for definition list processing.

%package        ext-emoji
Summary:        Flexmark extension for emoji shortcuts
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-jira-converter = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-emoji %_desc

This package contains an extension for emoji shortcuts.  It converts
Emoji Cheat Sheet and GitHub Emoji API shortcuts to characters on the
Unicode Emoji List.

%package        ext-enumerated-reference
Summary:        Flexmark extension for enumerated reference processing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-attributes = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-enumerated-reference %_desc

This package contains an extension for enumerated reference processing.

%package        ext-escaped-character
Summary:        Flexmark extension for escaped characters
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-escaped-character %_desc

This package contains an extension for converting escaped characters to
AST EscapedCharacter nodes.  It has no effect on rendered HTML.

%package        ext-footnotes
Summary:        Flexmark extension for footnotes
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-footnotes %_desc

This package contains an extension that converts footnote references and
definitions to HTML footnotes.

%package        ext-gfm-issues
Summary:        Flexmark extension for GitHub issue syntax
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-gfm-issues %_desc

This package contains an extension that converts GitHub Flavored
Markdown issue syntax to HTML links.

%package        ext-gfm-strikethrough
Summary:        Flexmark extension for GitHub strikethrough syntax
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-gfm-strikethrough %_desc

This package contains an extension that converts GitHub Flavored
Markdown strikethrough syntax (~~) to HTML.

%package        ext-gfm-tasklist
Summary:        Flexmark extension for GitHub task list items
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-gfm-tasklist %_desc

This package contains an extension that converts GitHub Flavored
Markdown bullet list items that start with [ ], [x], or [X] to an AST
TaskListItem node.

%package        ext-gfm-users
Summary:        Flexmark extension for GitHub user syntax
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-gfm-users %_desc

This package contains an extension that converts GitHub Flavored
Markdown user syntax to links.

%package        ext-gitlab
Summary:        Flexmark extension for GitLab Flavored Markdown
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-gitlab %_desc

This package contains an extension that parses and renders GitLab
Flavored Markdown.

%package        ext-ins
Summary:        Flexmark extension for inserted text
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-ins %_desc

This package contains an extension that converts `++text++` syntax into
`<ins>text</ins>`, the HTML syntax for inserted text.

%package        ext-jekyll-front-matter
Summary:        Flexmark extension for Jekyll front matter
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-yaml-front-matter = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-jekyll-front-matter %_desc

This package contains an extension that converts Jekyll front matter
YAML to an AST JekyllFrontMatterBlock node.

%package        ext-jekyll-tag
Summary:        Flexmark extension for Jekyll tag parsing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-jekyll-tag %_desc

This package contains an extension that converts Jekyll tags of the form
`{% tag tag-parameters %}` into AST JekyllTag or JekyllTagBlock nodes.

%package        ext-macros
Summary:        Flexmark extension for processing macros
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-gitlab = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-macros %_desc

This package contains an extension that converts macro text to macro
definitions and macro references.

%package        ext-media-tags
Summary:        Flexmark extension for HTML5 media tags
Requires:       %{name} = %{version}-%{release}

%description    ext-media-tags %_desc

This package contains an extension for embedding media using HTML5 media
tags, in particular the audio, embed, picture, and video tags.

%package        ext-resizable-image
Summary:        Flexmark extension to set image size
Requires:       %{name} = %{version}-%{release}

%description    ext-resizable-image %_desc

This package contains an extension to set the width and height of images
by stating them as `![text](/src =WxH)`, which is used in Azure DevOps
markdown.

%package        ext-spec-example
Summary:        Flexmark extension for spec test example processing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-test-util = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-spec-example %_desc

This package contains an extension that converts flexmark spec example
syntax into AST nodes.

%package        ext-superscript
Summary:        Flexmark extension for superscript processing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-superscript %_desc

This package contains an extension that converts `^superscript^` syntax
into `<sup>superscript</sup>`.

%package        ext-tables
Summary:        Flexmark extension for tables
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-tables %_desc

This package contains an extension for tables using `|` pipes with
optional column spans and table caption.

%package        ext-toc
Summary:        Flexmark extension for table of contents
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-toc %_desc

This package contains an extension that converts `[TOC style]` text to
AST TocBlock, SimToc, and SimTocContent nodes.

%package        ext-typographic
Summary:        Flexmark extension for typographic processing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-typographic %_desc

This package contains an extension for typographic processing.  It
converts:
- apostrophe (`'`) to `&rsquo;`
- ellipsis (`...` or `. . .`) to `&hellip;`
- en dash (`--`) to `&ndash;`
- em dash (`---`) to `&mdash;`
- single quoted `'text'` to `&lsquo;text&rsquo;`
- double quoted `"text"` to `&ldquo;text&rdquo;`
- double angle quoted `<<text>>` to `&laquo;text&raquo;`

%package        ext-wikilink
Summary:        Flexmark extension for wiki links
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-wikilink %_desc

This package contains an extension that converts references that are
wrapped in `[[]]` into wiki links with optional text separated by `|`.
Optional syntax to convert `![[]]` to image links is available.

%package        ext-xwiki-macros
Summary:        Flexmark extension for xwiki application-specific macros
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-xwiki-macros %_desc

This package contains an extension for xwiki application-specific
macros.  Both block and inline macros are supported.

%package        ext-yaml-front-matter
Summary:        Flexmark extension for YAML front matter
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-yaml-front-matter %_desc

This package contains an extension for YAML front matter.

%package        ext-youtube-embedded
Summary:        Flexmark extension for YouTube links
Requires:       %{name} = %{version}-%{release}

%description    ext-youtube-embedded %_desc

This package contains an extension for converting YouTube links to
embedded video iframes.

%package        ext-zzzzzz
Summary:        Flexmark extension for zzzzzz
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    ext-zzzzzz %_desc

This package contains an extension that supports zzzzzz syntax.

%package        html2md-converter
Summary:        Flexmark HTML to Markdown extensible converter
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-emoji = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    html2md-converter %_desc

This package contains a customizable extension to convert HTML to
Markdown.

%package        jira-converter
Summary:        Convert flexmark AST to Jira formatted text
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-gfm-strikethrough = %{version}-%{release}
Requires:       %{name}-ext-ins = %{version}-%{release}
Requires:       %{name}-ext-superscript = %{version}-%{release}
Requires:       %{name}-ext-tables = %{version}-%{release}
Requires:       %{name}-ext-wikilink = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    jira-converter %_desc

This package contains an extension for rendering flexmark AST as Jira
formatted text.

%package        osgi
Summary:        Flexmark OSGi bundle
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-abbreviation = %{version}-%{release}
Requires:       %{name}-ext-admonition = %{version}-%{release}
Requires:       %{name}-ext-anchorlink = %{version}-%{release}
Requires:       %{name}-ext-aside = %{version}-%{release}
Requires:       %{name}-ext-attributes = %{version}-%{release}
Requires:       %{name}-ext-autolink = %{version}-%{release}
Requires:       %{name}-ext-definition = %{version}-%{release}
Requires:       %{name}-ext-emoji = %{version}-%{release}
Requires:       %{name}-ext-enumerated-reference = %{version}-%{release}
Requires:       %{name}-ext-escaped-character = %{version}-%{release}
Requires:       %{name}-ext-footnotes = %{version}-%{release}
Requires:       %{name}-ext-gfm-issues = %{version}-%{release}
Requires:       %{name}-ext-gfm-strikethrough = %{version}-%{release}
Requires:       %{name}-ext-gfm-tasklist = %{version}-%{release}
Requires:       %{name}-ext-gfm-users = %{version}-%{release}
Requires:       %{name}-ext-gitlab = %{version}-%{release}
Requires:       %{name}-ext-jekyll-front-matter = %{version}-%{release}
Requires:       %{name}-ext-jekyll-tag = %{version}-%{release}
Requires:       %{name}-ext-media-tags = %{version}-%{release}
Requires:       %{name}-ext-resizable-image = %{version}-%{release}
Requires:       %{name}-ext-ins = %{version}-%{release}
Requires:       %{name}-ext-xwiki-macros = %{version}-%{release}
Requires:       %{name}-ext-superscript = %{version}-%{release}
Requires:       %{name}-ext-tables = %{version}-%{release}
Requires:       %{name}-ext-toc = %{version}-%{release}
Requires:       %{name}-ext-typographic = %{version}-%{release}
Requires:       %{name}-ext-wikilink = %{version}-%{release}
Requires:       %{name}-ext-yaml-front-matter = %{version}-%{release}
Requires:       %{name}-ext-youtube-embedded = %{version}-%{release}
Requires:       %{name}-html2md-converter = %{version}-%{release}
Requires:       %{name}-jira-converter = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-builder = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-dependency = %{version}-%{release}
Requires:       %{name}-util-format = %{version}-%{release}
Requires:       %{name}-util-html = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-options = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}
Requires:       %{name}-util-visitor = %{version}-%{release}
Requires:       %{name}-youtrack-converter = %{version}-%{release}

%description    osgi %_desc

This package contains all extension modules and converter modules except
the PDF converter in OSGi bundle format.

%package        test-util
Summary:        Flexmark test utilities
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-format = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}

%description    test-util %_desc

This package contains test utilities.

%package        tree-iteration
Summary:        Flexmark library for recursive tree iteration
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}

%description    tree-iteration %_desc

This package contains a library that allows recursive child and sibling
iteration with filtering, recursion and item mapping provided by
downstream users.

%package        util
Summary:        Flexmark utility classes
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-builder = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-dependency = %{version}-%{release}
Requires:       %{name}-util-format = %{version}-%{release}
Requires:       %{name}-util-html = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-options = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}
Requires:       %{name}-util-visitor = %{version}-%{release}

%description    util %_desc

This package contains utility classes.

%package        util-ast
Summary:        Flexmark AST utilities
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}
Requires:       %{name}-util-visitor = %{version}-%{release}

%description    util-ast %_desc

This package contains AST utility classes.

%package        util-builder
Summary:        Flexmark builder utilities
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}

%description    util-builder %_desc

This package contains builder utility classes.

%package        util-collection
Summary:        Flexmark collection utilities
Requires:       %{name}-util-misc = %{version}-%{release}

%description    util-collection %_desc

This package contains collection utility classes.

%package        util-data
Summary:        Flexmark data utilities
Requires:       %{name}-util-misc = %{version}-%{release}

%description    util-data %_desc

This package contains data utility classes.

%package        util-dependency
Summary:        Flexmark dependency utilities
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}

%description    util-dependency %_desc

This package contains dependency utility classes.

%package        util-experimental
Summary:        Flexmark experimental utilities
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}

%description    util-experimental %_desc

This package contains experimental utility classes that may or may not
work in all cases.  Use at your own risk.

%package        util-format
Summary:        Flexmark format utilities
Requires:       %{name}-util-ast = %{version}-%{release}
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-html = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}

%description    util-format %_desc

This package contains format utility classes.

%package        util-html
# BSD-2-Clause: the project as a whole
# Apache-2.0:
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/BackgroundColor.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/Color.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/ColorStyler.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/FontStyle.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/FontStyleStyler.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/FontStyler.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/HtmlBuilder.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/HtmlHelpers.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/HtmlStyler.java
# - flexmark-util-html/src/main/java/com/vladsch/flexmark/util/html/ui/HtmlStylerBase.java
License:        BSD-2-Clause AND Apache-2.0
Summary:        Flexmark HTML utilities
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}

%description    util-html %_desc

This package contains HTML utility classes.

%package        util-misc
# BSD-2-Clause: the project as a whole
# Apache-2.0:
# - flexmark-util-misc/src/main/java/com/vladsch/flexmark/util/misc/DelimitedBuilder.java
License:        BSD-2-Clause AND Apache-2.0
Summary:        Flexmark miscellaneous utilities

%description    util-misc %_desc

This package contains miscellaneous utility classes.

%package        util-options
Summary:        Flexmark options utilities
Requires:       %{name}-util-misc = %{version}-%{release}
Requires:       %{name}-util-sequence = %{version}-%{release}

%description    util-options %_desc

This package contains options utility classes.

%package        util-sequence
Summary:        Flexmark sequence utilities
Requires:       %{name}-util-collection = %{version}-%{release}
Requires:       %{name}-util-data = %{version}-%{release}
Requires:       %{name}-util-misc = %{version}-%{release}

%description    util-sequence %_desc

This package contains sequence utility classes.

%package        util-visitor
Summary:        Flexmark visitor utilities

%description    util-visitor %_desc

This package contains visitor utility classes.

%package        youtrack-converter
Summary:        Flexmark extension for YouTrack conversion
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ext-gfm-strikethrough = %{version}-%{release}
Requires:       %{name}-ext-tables = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}

%description    youtrack-converter %_desc

This package contains an extension that renders flexmark AST as YouTrack
formatted text (before YouTrack implemented Markdown comment option).

%prep
%autosetup -p1

%conf
# Remove prebuilt jars
rm lib/*.jar

# Not needed for an RPM build
%pom_remove_plugin org.codehaus.mojo:versions-maven-plugin

# We do not want to run benchmarks
%pom_remove_dep -r org.openjdk.jmh:jmh-core
%pom_remove_dep -r org.openjdk.jmh:jmh-generator-annprocess
rm flexmark-core-test/src/test/java/com/vladsch/flexmark/core/test/util/parser/SpecBenchmark.java

# Pegdown is not available in Fedora
%pom_remove_dep -r org.pegdown:pegdown
%pom_remove_dep com.vladsch.flexmark:flexmark-profile-pegdown flexmark-all
%pom_remove_dep com.vladsch.flexmark:flexmark-profile-pegdown flexmark-osgi
%pom_disable_module flexmark-profile-pegdown
rm flexmark-integration-test/src/test/java/com/vladsch/flexmark/integration/test/PegDownBenchmark.java

# Disable due to missing docx4j dependency
%pom_disable_module flexmark-docx-converter

# Disable due to missing openhtmltopdf dependency
%pom_disable_module flexmark-pdf-converter
%pom_remove_dep com.vladsch.flexmark:flexmark-pdf-converter flexmark-all

%build
%mvn_build -s

%install
%mvn_install

# We do not want to package the test packages
for m in core-test integration-test test-specs; do
  rm %{buildroot}%{_javadir}/flexmark-java/flexmark-$m.jar
  rm %{buildroot}%{_mavenpomdir}/flexmark-java/flexmark-$m.pom
  rm %{buildroot}%{_datadir}/maven-metadata/flexmark-java-flexmark-$m.xml
done

%files -f .mfiles-flexmark -f .mfiles-flexmark-java
%doc README.md
%license LICENSE.txt

%files all -f .mfiles-flexmark-all

%files ext-abbreviation -f .mfiles-flexmark-ext-abbreviation

%files ext-admonition -f .mfiles-flexmark-ext-admonition

%files ext-anchorlink -f .mfiles-flexmark-ext-anchorlink

%files ext-aside -f .mfiles-flexmark-ext-aside

%files ext-attributes -f .mfiles-flexmark-ext-attributes

%files ext-autolink -f .mfiles-flexmark-ext-autolink

%files ext-definition -f .mfiles-flexmark-ext-definition

%files ext-emoji -f .mfiles-flexmark-ext-emoji

%files ext-enumerated-reference -f .mfiles-flexmark-ext-enumerated-reference

%files ext-escaped-character -f .mfiles-flexmark-ext-escaped-character

%files ext-footnotes -f .mfiles-flexmark-ext-footnotes

%files ext-gfm-issues -f .mfiles-flexmark-ext-gfm-issues

%files ext-gfm-strikethrough -f .mfiles-flexmark-ext-gfm-strikethrough

%files ext-gfm-tasklist -f .mfiles-flexmark-ext-gfm-tasklist

%files ext-gfm-users -f .mfiles-flexmark-ext-gfm-users

%files ext-gitlab -f .mfiles-flexmark-ext-gitlab

%files ext-ins -f .mfiles-flexmark-ext-ins

%files ext-jekyll-front-matter -f .mfiles-flexmark-ext-jekyll-front-matter

%files ext-jekyll-tag -f .mfiles-flexmark-ext-jekyll-tag

%files ext-macros -f .mfiles-flexmark-ext-macros

%files ext-media-tags -f .mfiles-flexmark-ext-media-tags

%files ext-resizable-image -f .mfiles-flexmark-ext-resizable-image

%files ext-spec-example -f .mfiles-flexmark-ext-spec-example

%files ext-superscript -f .mfiles-flexmark-ext-superscript

%files ext-tables -f .mfiles-flexmark-ext-tables

%files ext-toc -f .mfiles-flexmark-ext-toc

%files ext-typographic -f .mfiles-flexmark-ext-typographic

%files ext-wikilink -f .mfiles-flexmark-ext-wikilink

%files ext-xwiki-macros -f .mfiles-flexmark-ext-xwiki-macros

%files ext-yaml-front-matter -f .mfiles-flexmark-ext-yaml-front-matter

%files ext-youtube-embedded -f .mfiles-flexmark-ext-youtube-embedded

%files ext-zzzzzz -f .mfiles-flexmark-ext-zzzzzz

%files html2md-converter -f .mfiles-flexmark-html2md-converter

%files jira-converter -f .mfiles-flexmark-jira-converter

%files osgi -f .mfiles-flexmark-osgi

%files test-util -f .mfiles-flexmark-test-util

%files tree-iteration -f .mfiles-flexmark-tree-iteration

%files util -f .mfiles-flexmark-util

%files util-ast -f .mfiles-flexmark-util-ast

%files util-builder -f .mfiles-flexmark-util-builder

%files util-collection -f .mfiles-flexmark-util-collection

%files util-data -f .mfiles-flexmark-util-data

%files util-dependency -f .mfiles-flexmark-util-dependency

%files util-experimental -f .mfiles-flexmark-util-experimental

%files util-format -f .mfiles-flexmark-util-format

%files util-html -f .mfiles-flexmark-util-html

%files util-misc -f .mfiles-flexmark-util-misc
%license LICENSE.txt

%files util-options -f .mfiles-flexmark-util-options

%files util-sequence -f .mfiles-flexmark-util-sequence

%files util-visitor -f .mfiles-flexmark-util-visitor
%license LICENSE.txt

%files youtrack-converter -f .mfiles-flexmark-youtrack-converter

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 0.64.6-14
- Latest state for flexmark-java

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 0.64.6-13
- Rebuilt for java-25-openjdk as preffered jdk

* Mon Jul 28 2025 Jerry James <loganjerry@gmail.com> - 0.64.6-12
- Fix FTBFS due to changes in jsoup >= 1.20

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Jerry James <loganjerry@gmail.com> - 0.64.6-9
- Move configuration steps to %%conf

* Wed Nov 20 2024 Jerry James <loganjerry@gmail.com> - 0.64.6-8
- Avoid unexpanded macro in package %%description

* Wed Sep 25 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.64.6-7
- Fix incompatibility with OpenJDK 21
- Resolves: rhbz#2310596

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jerry James <loganjerry@gmail.com> - 0.64.6-5
- Add VCS field

* Thu Jun 27 2024 Jerry James <loganjerry@gmail.com> - 0.64.6-4
- Build with OpenJDK 17

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 30 2023 Jerry James <loganjerry@gmail.com> - 0.64.6-1
- Initial RPM
## END: Generated by rpmautospec
