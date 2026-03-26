<?xml version="1.0" encoding="UTF-8"?>
<!-- This stylesheet will:
     - reorder, indent and normalize a comps file,
     - merge duplicate groups and categories,
     - warn about packages referenced by multiple groups,
     - kill multiple references to the same package within a group,

     Typical usage is:
     $ xsltproc -o output-file comps-cleanup.xsl original-file

     You can use the ‑‑novalid xsltproc switch to kill the warning about
     Fedora not installing the comps DTD anywhere xsltproc can find it.
     However without DTD there is no way to check the files completely.

     © Nicolas Mailhot <nim at fedoraproject dot org> 2006-2008 -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:exsl="http://exslt.org/common" version="1.0" extension-element-prefixes="exsl">
  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" indent="yes" encoding="UTF-8" doctype-system="comps.dtd" doctype-public="-//Red Hat, Inc.//DTD Comps info//EN"/>
  <xsl:key name="unique-groups" match="/comps/group" use="id/text()"/>
  <xsl:key name="unique-environments" match="/comps/environment" use="id/text()"/>
  <xsl:key name="unique-categories" match="/comps/category" use="id/text()"/>
  <xsl:key name="packages-by-group" match="/comps/group/packagelist/packagereq" use="../../id/text()"/>
  <xsl:key name="unique-package-entries" match="/comps/group/packagelist/packagereq" use="concat(../../id/text(),'/',text())"/>
  <xsl:key name="unique-packages" match="/comps/group/packagelist/packagereq[generate-id(.) = generate-id(key('unique-package-entries',concat(../../id/text(),'/',text()))[1])]" use="text()"/>
  <xsl:key name="groups-by-category" match="/comps/category/grouplist/groupid" use="../../id/text()"/>
  <xsl:key name="unique-group-entries" match="/comps/category/grouplist/groupid" use="concat(../../id/text(),'/',text())"/>
  <xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
  <xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
  <xsl:variable name="type-sort-order">
    <unknown/>
    <mandatory/>
    <conditional/>
    <default/>
    <optional/>
  </xsl:variable>
  <xsl:variable name="attribute-sort-order">
    <unknown/>
    <arch/>
    <name/>
    <package/>
    <type/>
    <requires/>
    <basearch/>
  </xsl:variable>
  <!-- Preserve most nodes -->
  <xsl:template match="*" priority="0">
    <xsl:apply-templates select="." mode="normalize"/>
  </xsl:template>
  <xsl:template match="*" mode="normalize">
    <!-- Group comments with the logically-following element -->
    <xsl:apply-templates select="preceding-sibling::node()[normalize-space()][1][self::comment()] "/>
    <xsl:copy>
      <xsl:apply-templates select="@*">
        <xsl:sort select="count(exsl:node-set($attribute-sort-order)/*[name() = name(current())]/preceding-sibling::*)" data-type="number"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="*|text()"/>
    </xsl:copy>
  </xsl:template>
  <!-- Preserve attributes and text nodes -->
  <xsl:template match="comment()|text()">
    <xsl:apply-templates select="preceding-sibling::node()[normalize-space()][1][self::comment()] "/>
    <xsl:copy/>
  </xsl:template>
  <!-- Preserve attributes -->
  <xsl:template match="@*">
    <xsl:copy/>
  </xsl:template>
  <!-- Sort groups by id, and categories by display order -->
  <xsl:template match="comps" priority="1">
    <xsl:apply-templates select="preceding-sibling::node()[normalize-space()][1][self::comment()] "/>
    <xsl:copy>
      <xsl:apply-templates select="group">
        <xsl:sort select="translate(id/text(),$lcletters,$ucletters)"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="environment">
        <xsl:sort select="display_order/text()"/>
        <xsl:sort select="translate(id/text(),$lcletters,$ucletters)"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="category">
        <xsl:sort select="display_order/text()"/>
        <xsl:sort select="translate(id/text(),$lcletters,$ucletters)"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="langpacks"/>
      <xsl:apply-templates select="blacklist"/>
      <xsl:apply-templates select="whiteout"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="langpacks" priority="1">
    <xsl:copy>
      <xsl:apply-templates select="match">
       <xsl:sort select="@name"/>
       <xsl:sort select="@install"/>
    </xsl:apply-templates>
   </xsl:copy>
 </xsl:template>
  <xsl:template match="blacklist" priority="1">
    <xsl:copy>
      <xsl:apply-templates select="package">
        <xsl:sort select="@arch"/>
        <xsl:sort select="@name"/>
      </xsl:apply-templates>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="whiteout" priority="1">
    <xsl:copy>
      <xsl:apply-templates select="ignoredep">
        <xsl:sort select="@package"/>
        <xsl:sort select="@requires"/>
      </xsl:apply-templates>
    </xsl:copy>
  </xsl:template>
  <!-- Warn about empty groups -->
  <xsl:template match="group[count(key('packages-by-group',id/text()))=0]" priority="2">
    <xsl:message>☹☹☹ Empty group <xsl:value-of select="concat(_name/text(),' (',id/text(),')')"/>!</xsl:message>
    <xsl:apply-templates select="." mode="normalize"/>
  </xsl:template>
  <!-- Warn about duplicate groups being merged -->
  <xsl:template match="group[generate-id(.) != generate-id(key('unique-groups',id/text())[1])]" priority="3">
    <xsl:message> ☹☹ Duplicate group <xsl:value-of select="concat(_name/text(),' (',id/text(),')')"/> will be merged.</xsl:message>
  </xsl:template>
  <!-- Warn about empty categories -->
  <xsl:template match="category[count(key('groups-by-category',id/text()))=0]" priority="2">
    <xsl:message>☹☹☹ Empty category <xsl:value-of select="concat(_name/text(),' (',id/text(),')')"/>!</xsl:message>
    <xsl:apply-templates select="." mode="normalize"/>
  </xsl:template>
  <!-- Warn about duplicate environments being merged -->
  <xsl:template match="environment[generate-id(.) != generate-id(key('unique-environments',id/text())[1])]" priority="3">
    <xsl:message> ☹☹ Duplicate environment <xsl:value-of select="concat(_name/text(),' (',id/text(),')')"/> will be merged.</xsl:message>
  </xsl:template>
  <!-- Warn about duplicate categories being merged -->
  <xsl:template match="category[generate-id(.) != generate-id(key('unique-categories',id/text())[1])]" priority="3">
    <xsl:message> ☹☹ Duplicate category <xsl:value-of select="concat(_name/text(),' (',id/text(),')')"/> will be merged.</xsl:message>
  </xsl:template>
  <!-- Sort packages within a group by class then name -->
  <xsl:template match="packagelist" priority="1">
    <xsl:copy>
      <xsl:apply-templates select="key('packages-by-group',../id/text())">
        <xsl:sort select="count(exsl:node-set($type-sort-order)/*[name() = current()/@type]/preceding-sibling::*)" data-type="number"/>
        <xsl:sort select="translate(text(),$lcletters,$ucletters)"/>
      </xsl:apply-templates>
    </xsl:copy>
  </xsl:template>
  <!-- Sort groups within a category by name -->
  <xsl:template match="category/grouplist" priority="1">
    <xsl:copy>
      <xsl:apply-templates select="key('groups-by-category',../id/text())">
        <xsl:sort select="translate(text(),$lcletters,$ucletters)"/>
      </xsl:apply-templates>
    </xsl:copy>
  </xsl:template>
  <!-- Kill duplicate package entries -->
  <xsl:template match="packagereq[generate-id(.) != generate-id(key('unique-package-entries',concat(../../id/text(),'/',text()))[1])]" priority="2">
    <xsl:message>☹☹☹ Ignoring duplicate reference to <xsl:value-of select="concat(@type,' package ',text())"/> in group <xsl:value-of select="concat(../../_name/text(),' (',../../id/text(),')')"/>.</xsl:message>
    <xsl:message>     ⇒ Only its first reference (<xsl:value-of select="key('unique-package-entries',concat(../../id/text(),'/',text()))[1]/@type"/> package) will be kept.</xsl:message>
  </xsl:template>
  <!-- Kill duplicate group entries -->
  <xsl:template match="category/grouplist/groupid[generate-id(.) != generate-id(key('unique-group-entries',concat(../../id/text(),'/',text()))[1])]" priority="1">
    <xsl:message>  ☹ Ignoring duplicate reference to group <xsl:value-of select="text()"/> in category <xsl:value-of select="concat(../../_name/text(),' (',../../id/text(),')')"/>.</xsl:message>
  </xsl:template>
  <!-- Warn about packages referenced several times
  <xsl:template match="packagereq[generate-id(.) = generate-id(key('unique-packages',text())[2])]" priority="1">
    <xsl:variable name="dupes" select="key('unique-packages',text())"/>
    <xsl:message>  ☹ Package <xsl:value-of select="text()"/> is referenced in <xsl:value-of select="count($dupes)"/> groups:</xsl:message>
    <xsl:for-each select="$dupes">
      <xsl:sort select="translate(../../id/text(),$lcletters,$ucletters)"/>
      <xsl:message>     ✓ <xsl:value-of select="@type"/> package in group <xsl:value-of select="concat(../../_name/text(),' (',../../id/text(),')')"/></xsl:message>
    </xsl:for-each>
    <xsl:apply-templates select="." mode="normalize"/>
  </xsl:template> -->
</xsl:stylesheet>
