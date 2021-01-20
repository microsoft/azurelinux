-- Lua code used by macros.forge and derivatives

-- Computes the suffix of a version string, removing vprefix if it matches
-- For example with vprefix 1.2.3: 1.2.3.rc2 → .rc2 but 1.2.30 → 1.2.30 not 0
local function getversionsuffix(vstring,vprefix)
  if (string.sub(vstring, 1, #vprefix) == vprefix) and
     (not string.match(string.sub(vstring, #vprefix + 1), "^%.?%d")) then
    return string.sub(vstring, #vprefix + 1)
  else
    return vstring
  end
end

-- Check if an identified url is sane
local function checkforgeurl(url, id, silent)
  local checkedurl  = nil
  local checkedid   = nil
  local urlpatterns = {
    gitlab = {
      pattern     = 'https://[^/]+/[^/]+/[^/#?]+',
      description = 'https://(…[-.])gitlab[-.]…/owner/repo'},
    pagure = {
      pattern     = 'https://[^/]+/[^/#?]+',
      description = 'https://pagure.io/repo'},
    pagure_ns = {
      pattern     = 'https://[^/]+/[^/]+/[^/#?]+',
      description = 'https://pagure.io/namespace/repo'},
    pagure_fork = {
      pattern     = 'https://[^/]+/fork/[^/]+/[^/#?]+',
      description = 'https://pagure.io/fork/owner/repo'},
    pagure_ns_fork = {
      pattern     = 'https://[^/]+/fork/[^/]+/[^/]+/[^/#?]+',
      description = 'https://pagure.io/fork/owner/namespace/repo'},
    github = {
      pattern     = 'https://[^/]+/[^/]+/[^/#?]+',
      description = 'https://(…[-.])github[-.]…/owner/repo'},
    ["code.googlesource.com"] = {
      pattern     = 'https://code.googlesource.com/[^#?]*[^/#?]+',
      description = 'https://code.googlesource.com/…/repo'},
    ["bitbucket.org"] = {
      pattern     = 'https://[^/]+/[^/]+/[^/#?]+',
      description = 'https://bitbucket.org/owner/repo'}}
  if (urlpatterns[id] ~= nil) then
    checkedurl = string.match(url,urlpatterns[id]["pattern"])
    if (checkedurl == nil) then
      if not silent then
        rpm.expand("%{error:" .. id .. " URLs must match " .. urlpatterns[id]["description"] .. " !}")
      end
    else
      checkedid = id
    end
  end
  return checkedurl, checkedid
end

-- Check if an url matches a known forge
local function idforge(url, silent)
  local forgeurl = nil
  local forge    = nil
  if (url ~= "") then
    forge = string.match(url, "^[^:]+://([^/]+)/")
    if (forge == nil) then
      if not silent then
        rpm.expand("%{error:URLs must include a protocol such as https:// and a path starting with / !}")
      end
    else
      if (forge == "pagure.io") then
        if     string.match(url, "[^:]+://pagure.io/fork/[^/]+/[^/]+/[^/]+") then
          forge = "pagure_ns_fork"
        elseif string.match(url, "[^:]+://pagure.io/fork/[^/]+/[^/]+") then
          forge = "pagure_fork"
        elseif  string.match(url, "[^:]+://pagure.io/[^/]+/[^/]+") then
          forge = "pagure_ns"
        elseif  string.match(url, "[^:]+://pagure.io/[^/]+") then
          forge = "pagure"
        end
      elseif (string.match(forge, "^gitlab[%.-]") or string.match(forge, "[%.-]gitlab[%.]")) then
        forge = "gitlab"
      elseif (string.match(forge, "^github[%.-]") or string.match(forge, "[%.-]github[%.]")) then
        forge = "github"
      end
      forgeurl, forge = checkforgeurl(url, forge, silent)
    end
  end
  return forgeurl, forge
end

-- The forgemeta macro main processing function
-- See the documentation in the macros.forge file for argument description
-- Also called directly by gometa
local function meta(suffix, verbose, informative, silent)
  local mariner = require "mariner.common"
  local ismain = (suffix == "") or (suffix == "0")
  if ismain then
    mariner.zalias({"forgeurl", "forgesource", "forgesetupargs",
                      "archivename", "archiveext", "archiveurl",
                      "topdir", "extractdir", "repo", "owner", "namespace",
                      "scm", "tag", "commit", "shortcommit", "branch", "version",
                      "date", "distprefix"}, verbose)
  end
  local variables = {
    default = {
      scm         = "git",
      archiveext  = "tar.bz2",
      repo        = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "^[^:]+://[^/]+/[^/]+/([^/?#]+)"))}',
      archivename = "%{repo"         .. suffix .. "}-%{ref"           .. suffix .. "}",
      topdir      = "%{archivename"  .. suffix .. "}" },
    gitlab = {
      archiveurl  = "%{forgeurl"     .. suffix .. "}/-/archive/%{ref" .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}" },
    pagure = {
      archiveext  = "tar.gz",
      repo        = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "^[^:]+://[^/]+/([^/?#]+)"))}',
      archiveurl  = "%{forgeurl"     .. suffix .. "}/archive/%{ref"   .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}" },
    pagure_ns = {
      archiveext  = "tar.gz",
      namespace   = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "^[^:]+://[^/]+/([^/]+)/[^/?#]+"))}',
      repo        = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "^[^:]+://[^/]+/[^/]+/([^/?#]+)"))}',
      archivename = "%{namespace"    .. suffix .. "}-%{repo"          .. suffix .. "}-%{ref"         .. suffix .. "}",
      archiveurl  = "%{forgeurl"     .. suffix .. "}/archive/%{ref"   .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}" },
    pagure_fork = {
      archiveext  = "tar.gz",
      owner       = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "https://[^/]+/fork/([^/]+)/[^/?#]+"))}',
      repo        = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "https://[^/]+/fork/[^/]+/([^/?#]+)"))}',
      archivename = "%{owner"        .. suffix .. "}-%{repo"          .. suffix .. "}-%{ref"         .. suffix .. "}",
      archiveurl  = "%{forgeurl"     .. suffix .. "}/archive/%{ref"   .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}" },
    pagure_ns_fork = {
      owner       = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "https://[^/]+/fork/([^/]+)/[^/]+/[^/?#]+"))}',
      namespace   = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "https://[^/]+/fork/[^/]+/([^/]+)/[^/?#]+")}',
      repo        = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "https://[^/]+/fork/[^/]+/[^/]+/([^/?#]+)")}',
      archivename = "%{owner"        .. suffix .. "}-%{namespace"     .. suffix .. "}-%{repo"        .. suffix .. "}-%{ref"        .. suffix .. "}",
      archiveurl  = "%{forgeurl"     .. suffix .. "}/archive/%{ref"   .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}" },
    github = {
      archiveext  = "tar.gz",
      archivename = "%{repo"         .. suffix .. "}-%{fileref"       .. suffix .. "}",
      archiveurl  = "%{forgeurl"     .. suffix .. "}/archive/%{ref"   .. suffix .. "}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}" },
    ["code.googlesource.com"] = {
      archiveext  = "tar.gz",
      repo        = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "^[^:]+://.+/([^/?#]+)"))}',
      archiveurl  = "%{forgeurl"     .. suffix .. "}/+archive/%{ref"  .. suffix .. "}.%{archiveext"  .. suffix .. "}",
      topdir      = "" },
    ["bitbucket.org"] = {
      shortcommit = '%{lua:print(string.sub(rpm.expand("%{commit'     .. suffix .. '}"), 1, 12))}',
      owner       = '%{lua:print(string.match(rpm.expand("%{forgeurl' .. suffix .. '}"), "^[^:]+://[^/]+/([^/?#]+)"))}',
      archivename = "%{owner"        .. suffix .. "}-%{repo"          .. suffix .. "}-%{shortcommit" .. suffix .. "}",
      archiveurl  = "%{forgeurl"     .. suffix .. "}/get/%{ref"       .. suffix .. "}.%{archiveext"  .. suffix .. "}" } }
  -- Packaging a moving branch is quite a bad idea, but since at least Gitlab
  -- will treat branches and tags the same way better support branches explicitly
  -- than have packagers hijack %{tag} to download branch states
  local spec = {}
  for _, v in ipairs({'forgeurl','tag','commit','branch','version'}) do
    spec[v] = rpm.expand("%{?" .. v .. suffix .. "}")
  end
  -- Compute the reference of the object to fetch
  local isrelease = false
  if     (spec["tag"]     ~= "") then       ref = "%{?tag"     .. suffix .. "}"
  elseif (spec["commit"]  ~= "") then       ref = "%{?commit"  .. suffix .. "}"
  elseif (spec["branch"]  ~= "") then       ref = "%{?branch"  .. suffix .. "}"
  else                                      ref = "%{?version" .. suffix .. "}"
                                      isrelease = true
  end
  if (rpm.expand(ref) == "") then
    if (suffix == "") then
      rpm.expand("%{error:You need to define Version:, %{commit} or %{tag} before the macro invocation !}")
    else
      rpm.expand("%{error:You need to define %{version" .. suffix .. "}, %{commit" .. suffix .. "} or %{tag" .. suffix .. "} before the macro invocation !}")
    end
  end
  local    forgeurl = spec["forgeurl"]
  -- For backwards compatibility only
  local expliciturl = rpm.expand("%{?-u*}")
  if   (expliciturl ~= "") then
    rpm.expand("%{warn:-u use in %%forgemeta is deprecated, use -z instead to select a separate set of rpm variables!}")
           forgeurl = expliciturl
  end
  local forge
  forgeurl,   forge = idforge(forgeurl, silent)
  if (forge ~= nil) then
    mariner.explicitset("forgeurl" .. suffix, forgeurl, verbose)
    -- Custom processing of quirky forges that can not be handled with simple variables
    if (forge == "github") then
      -- Workaround the way GitHub injects "v"s before some version strings (but not all!)
      -- To package one of the minority of sane GitHub projects that do not munge their version
      -- strings set tag to %{version} in your spec
      local fileref = ref
      if (ref == "%{?version"  .. suffix .. "}") then
        ref = "v" .. ref
      elseif (fileref ~= "%{?commit" .. suffix .. "}") and
             string.match(rpm.expand(fileref), "^v[%d]") then
        fileref = string.gsub(rpm.expand(fileref), "^v", "")
      elseif (string.match(rpm.expand(fileref), "/")) then
        fileref = string.gsub(rpm.expand(fileref), "/", "-")
      end
      mariner.safeset("fileref" .. suffix, fileref, verbose)
    elseif (forge == "code.googlesource.com") then
      if (ref == "%{?version"  .. suffix .. "}") then
        ref = "v" .. ref
      end
    elseif (forge == "bitbucket.org") then
      if (spec["commit"] == "") then
        rpm.expand("%{error:All BitBucket URLs require commit value knowledge: you need to define %{commit}!}")
      end
    end
    mariner.safeset("ref" .. suffix, ref, verbose)
    -- Mass setting of the remaining variables
    for k,v in pairs(variables[forge]) do
      mariner.safeset(k .. suffix, variables[forge][k], verbose)
    end
    for k,v in pairs(variables["default"]) do
      if (variables[forge][k] == nil) then
        mariner.safeset(k .. suffix, variables["default"][k], verbose)
      end
    end
  end
  -- Generic rules
  for _, v in ipairs({'archiveurl','archivename','archiveext','topdir'}) do
    spec[v] = rpm.expand("%{?" .. v .. suffix .. "}")
  end
  -- Source URL processing (computing the forgesource spec variable)
  local forgesource = "%{archiveurl" .. suffix .. "}"
  if (string.match(spec["archiveurl"], "/([^/]+)$") ~= spec["archivename"] .. "." .. spec["archiveext"]) then
    forgesource     = "%{?archiveurl" .. suffix .. "}#/%{?archivename" .. suffix .. "}.%{archiveext" .. suffix .. "}"
  end
  mariner.safeset("forgesource" .. suffix, forgesource, verbose)
  -- Setup processing      (computing the forgesetup and extractdir variables)
  local forgesetupargs = "-n %{extractdir" .. suffix .. "}"
  local extractdir     = "%{topdir"        .. suffix .. "}"
  if (spec["topdir"] == "") then
    forgesetupargs     = "-c " .. forgesetupargs
    extractdir         = "%{archivename"   .. suffix .. "}"
  end
  if not ismain then
    if (spec["topdir"] ~= "") then
      forgesetupargs = "-T -D -b " .. suffix .. " " .. forgesetupargs
    else
      forgesetupargs = "-T -D -a " .. suffix .. " " .. forgesetupargs
    end
  end
  mariner.safeset("forgesetupargs" .. suffix, forgesetupargs, verbose)
  mariner.safeset("extractdir"     .. suffix, extractdir, verbose)
  -- dist processing       (computing the correct prefix for snapshots)
  local distprefix = ""
  if not isrelease then
    distprefix = string.lower(rpm.expand(ref))
    if     (ref == "%{?commit" .. suffix .. "}") then
      distprefix = string.sub(distprefix, 1, 7)
    elseif (ref ~= "%{?branch" .. suffix .. "}") then
      distprefix = string.gsub(distprefix,      "[%p%s]+", ".")
      distprefix = string.gsub(distprefix, "^" .. string.lower(rpm.expand("%{?repo}")) .. "%.?", "")
      local    v = string.gsub(rpm.expand("%{version}"), "[%p%s]+", ".")
      for _, p in ipairs({'','v','v.','version','version.','tags.v', 'tags.v.'}) do
        distprefix = getversionsuffix(distprefix, p .. v)
      end
      distprefix = string.gsub(distprefix, "^%.", "")
    end
    if (distprefix ~= "") then
      distprefix = "%{scm"     .. suffix .. "}" .. distprefix
      date = rpm.expand("%{?date" .. suffix .. "}")
      if (date ~= "") then
        distprefix = date .. distprefix
      else
        distprefix = "%([ -r %{_sourcedir}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "} ] && date +%Y%m%d -u -r %{_sourcedir}/%{archivename" .. suffix .. "}.%{archiveext" .. suffix .. "})" .. distprefix
      end
      distprefix = "." .. distprefix
    end
  end
  if (spec["version"] ~= "") and
     (spec["version"] ~= "0") and
     (spec["version"] ~= rpm.expand("%{?version}")) then
    distprefix = ".%{version" .. suffix .. "}" .. distprefix
  end
  if (rpm.expand(distprefix) ~= "") then
    if not ismain then
      distprefix = string.gsub(distprefix, "^%.", ".s")
    end
    mariner.safeset ("distprefix"    .. suffix, distprefix, verbose)
  end
  if ismain then
    mariner.zalias({"forgeurl", "forgesource", "forgesetupargs",
                      "archivename", "archiveext", "archiveurl",
                      "topdir", "extractdir", "repo", "owner", "namespace",
                      "scm", "shortcommit", "distprefix"}, verbose)
  end
  -- Final spec variable summary if the macro was called with -i
  if informative then
    rpm.expand("%{echo:Packaging variables read or set by %%forgemeta}")
    mariner.echovars({"forgeurl", "forgesource", "forgesetupargs",
                        "archivename", "archiveext", "archiveurl",
                        "topdir", "extractdir", "repo", "owner", "namespace",
                        "scm", "tag", "commit", "shortcommit", "branch", "version",
                        "date", "distprefix"}, suffix)
                        mariner.echovars({"dist"},"")
    rpm.expand("%{echo:  (snapshot date is either manually supplied or computed once %%{_sourcedir}/%%{archivename" .. suffix .. "}.%%{archiveext" .. suffix .. "} is available)}")
  end
end

return {
  meta = meta,
}

