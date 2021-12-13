<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:rng="http://relaxng.org/ns/structure/1.0"
                xmlns="http://relaxng.org/ns/structure/1.0"
                exclude-result-prefixes="rng">
<xsl:output format="xml" indent="yes"/>
<xsl:strip-space elements="*"/>

<xsl:param name="filename-or-version" select="'99.99'"/>
<xsl:variable name="version">
    <xsl:variable name="version-local">
        <xsl:choose>
            <xsl:when test="starts-with($filename-or-version, 'pacemaker-')">
                <xsl:variable name="version-tail"
                              select="substring-after($filename-or-version, 'pacemaker-')"/>
                <xsl:choose>
                    <xsl:when test="contains(substring-after($version-tail, '.'), '.')">
                        <xsl:value-of select="substring(
                                                  $version-tail,
                                                  1,
                                                  string-length($version-tail)
                                                  -
                                                  1
                                                  -
                                                  string-length(
                                                      substring-after(
                                                          substring-after(
                                                              $version-tail,
                                                              '.'
                                                          ),
                                                          '.'
                                                      )
                                                  )
                                              )"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$version-tail"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$filename-or-version"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:if test="number($version-local) = number('NaN')">
        <xsl:message terminate="yes">
            <xsl:value-of select="concat('Wrong number specification: ', $version-local)"/>
        </xsl:message>
    </xsl:if>
    <xsl:value-of select="$version-local"/>
</xsl:variable>
<xsl:variable name="version-major">
    <xsl:choose>
        <xsl:when test="contains($version, '.')">
            <xsl:value-of select="number(substring-before($version, '.'))"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="number($version)"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:variable>
<xsl:variable name="version-minor">
    <xsl:value-of select="number(concat('0', substring-after($version, '.')))"/>
</xsl:variable>

<xsl:template match="/rng:grammar">
    <xsl:copy>
        <xsl:copy-of select="@*"/>
        <xsl:attribute name="datatypeLibrary">
            <xsl:value-of select="'http://www.w3.org/2001/XMLSchema-datatypes'"/>
        </xsl:attribute>
        <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

<!-- drop these -->
<xsl:template match="@ns[. = '']"/>
<xsl:template match="@datatypeLibrary[
                         . = ''
                         or
                         . = 'http://www.w3.org/2001/XMLSchema-datatypes'
                     ]"/>

<!-- limit highest schema version in /cib/@validate-with to that
     of the file processed -->
<xsl:template match="rng:attribute[@name = 'validate-with']/rng:choice/rng:value">
    <xsl:choose>
        <xsl:when test="starts-with(text(), 'pacemaker-')
                        and
                        (
                            number(
                                substring-before(substring-after(text(), 'pacemaker-'), '.')
                            ) &gt; $version-major
                            or
                            (
                                number(
                                    substring-before(substring-after(text(), 'pacemaker-'), '.')
                                ) = $version-major
                                and
                                number(
                                    concat('0', substring-after(substring-after(text(), 'pacemaker-'), '.'))
                                ) &gt; $version-minor

                            )
                        )"/>
        <xsl:otherwise>
            <xsl:copy>
                <xsl:apply-templates select="@*|node()"/>
            </xsl:copy>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- ensure "status" section is optional; see also:
     - https://github.com/ClusterLabs/pacemaker/commit/89f5177
     - https://pagure.io/clufter/c/a3985ec -->
<xsl:template match="*[name() != 'optional']/rng:ref[@name = 'status']">
    <optional>
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </optional>
</xsl:template>

<!-- ensure neither "score-attribute" nor "score-attribute-mangle" attributes
     of rsc_colocation are supported; see also:
     - https://github.com/ClusterLabs/pacemaker/commit/30383cc
     - https://pagure.io/clufter/c/abd2d45 (+ 53b8215) -->
<xsl:template match="rng:element[@name = 'rsc_colocation']//rng:choice[
                         rng:attribute[@name = 'score']
                     ]">
    <xsl:apply-templates select="rng:attribute[@name = 'score']"/>
</xsl:template>

<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
