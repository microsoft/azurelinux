-- Convenience Lua functions that can be used within rpm macros

-- Reads an rpm variable. Unlike a basic rpm.expand("{?foo}"), returns nil if
-- the variable is unset, which is convenient in lua tests and enables
-- differentiating unset variables from variables set to ""
local function read(rpmvar)
  if not rpmvar or
    (rpm.expand("%{" .. rpmvar .. "}") == "%{" .. rpmvar .. "}") then
    return nil
  else
    return rpm.expand("%{?" .. rpmvar .. "}")
  end
end

-- Returns true if the macro that called this function had flag set
--   – for example, hasflag("z") would give the following results:
--     %foo -z bar → true
--     %foo -z     → true
--     %foo        → false
local function hasflag(flag)
  return (rpm.expand("%{-" .. flag .. "}") ~= "")
end

-- Returns the argument passed to flag in the macro that called this function
--  – for example, readflag("z") would give the following results:
--      %foo -z bar → bar
--      %foo        → nil
--      %foo -z ""  → empty string
--      %foo -z ''  → empty string
local function readflag(flag)
  if not hasflag(flag) then
    return nil
  else
    local a = rpm.expand("%{-" .. flag .. "*}")
    -- Handle "" and '' as empty strings
    if (a == '""') or (a == "''") then
      a = ''
    end
    return a
  end
end

-- Sets a spec variable; echoes the result if verbose
local function explicitset(rpmvar, value, verbose)
  local value = value
  if (value == nil) or (value == "") then
    value = "%{nil}"
  end
  rpm.define(rpmvar .. " " .. value)
  if verbose then
    rpm.expand("%{warn:Setting %%{" .. rpmvar .. "} = " .. value .. "}")
  end
end

-- Unsets a spec variable if it is defined; echoes the result if verbose
local function explicitunset(rpmvar, verbose)
  if (rpm.expand("%{" .. rpmvar .. "}") ~= "%{" .. rpmvar .. "}") then
    rpm.define(rpmvar .. " %{nil}")
    if verbose then
      rpm.expand("%{warn:Unsetting %%{" .. rpmvar .. "}}")
    end
  end
end

-- Sets a spec variable, if not already set; echoes the result if verbose
local function safeset(rpmvar, value, verbose)
  if (rpm.expand("%{" .. rpmvar .. "}") == "%{" .. rpmvar .. "}") then
    explicitset(rpmvar,value,verbose)
  end
end

-- Aliases a list of rpm variables to the same variables suffixed with 0 (and
-- vice versa); echoes the result if verbose
local function zalias(rpmvars, verbose)
  for _, sfx in ipairs({{"","0"},{"0",""}}) do
    for _, rpmvar in ipairs(rpmvars) do
      local toalias = "%{?" .. rpmvar .. sfx[1] .. "}"
      if (rpm.expand(toalias) ~= "") then
        safeset(rpmvar .. sfx[2], toalias, verbose)
      end
    end
  end
end

-- Takes a list of rpm variable roots and a suffix and alias current<root> to
-- <root><suffix> if it resolves to something not empty
local function setcurrent(rpmvars, suffix, verbose)
  for _, rpmvar in ipairs(rpmvars) do
    if (rpm.expand("%{?" .. rpmvar .. suffix .. "}") ~= "") then
      explicitset(  "current" .. rpmvar, "%{" .. rpmvar .. suffix .. "}", verbose)
    else
      explicitunset("current" .. rpmvar,                                  verbose)
    end
  end
end

-- Echo the list of rpm variables, with suffix, if set
local function echovars(rpmvars, suffix)
  for _, rpmvar in ipairs(rpmvars) do
    rpmvar = rpmvar .. suffix
    local header = string.sub("  " .. rpmvar .. ":                                               ",1,21)
    rpm.expand("%{?" .. rpmvar .. ":%{echo:" .. header .. "%{?" .. rpmvar .. "}}}")
  end
end

-- Returns an array, indexed by suffix, containing the non-empy values of
-- <rpmvar><suffix>, with suffix an integer string or the empty string
local function getsuffixed(rpmvar)
  local suffixes = {}
  zalias({rpmvar})
  for suffix=0,9999 do
    local value = rpm.expand("%{?" .. rpmvar .. suffix .. "}")
    if (value ~= "") then
      suffixes[tostring(suffix)] = value
    end
  end
  -- rpm convention is to alias no suffix to zero suffix
  -- only add no suffix if zero suffix is different
  local value = rpm.expand("%{?" .. rpmvar .. "}")
  if (value ~= "") and (value ~= suffixes["0"]) then
     suffixes[""] = value
  end
  return suffixes
end

-- Returns the list of suffixes, including the empty string, for which
-- <rpmvar><suffix> is set to a non empty value
local function getsuffixes(rpmvar)
  suffixes = {}
  for suffix in pairs(getsuffixed(rpmvar)) do
    table.insert(suffixes,suffix)
  end
  table.sort(suffixes,
             function(a,b) return (tonumber(a) or 0) < (tonumber(b) or 0) end)
  return suffixes
end

-- Returns the suffix for which <rpmvar><suffix> has a non-empty value that
-- matches best the beginning of the value string
local function getbestsuffix(rpmvar, value)
  local best         = nil
  local currentmatch = ""
  for suffix, setvalue in pairs(getsuffixed(rpmvar)) do
  if (string.len(setvalue) > string.len(currentmatch)) and
     (string.find(value, "^" .. setvalue)) then
      currentmatch = setvalue
      best         = suffix
    end
  end
  return best
end

-- %writevars core
local function writevars(macrofile, rpmvars)
  for _, rpmvar in ipairs(rpmvars) do
    print("sed -i 's\029" .. string.upper("@@" .. rpmvar .. "@@") ..
                   "\029" .. rpm.expand(  "%{" .. rpmvar .. "}" ) ..
                   "\029g' " .. macrofile .. "\n")
  end
end

-- https://github.com/rpm-software-management/rpm/issues/566
-- Reformat a text intended to be used used in a package description, removing
-- rpm macro generation artefacts.
-- – remove leading and ending empty lines
-- – trim intermediary empty lines to a single line
-- – fold on spaces
-- Should really be a %%{wordwrap:…} verb
local function wordwrap(text)
  text = rpm.expand(text .. "\n")
  text = string.gsub(text, "\t",              "  ")
  text = string.gsub(text, "\r",              "\n")
  text = string.gsub(text, " +\n",            "\n")
  text = string.gsub(text, "\n+\n",           "\n\n")
  text = string.gsub(text, "^\n",             "")
  text = string.gsub(text, "\n( *)[-*—][  ]+", "\n%1– ")
  output = ""
  for line in string.gmatch(text, "[^\n]*\n") do
    local pos = 0
    local advance = ""
    for word in string.gmatch(line, "%s*[^%s]*\n?") do
      local wl, bad = utf8.len(word)
      if not wl then
        print("%{warn:Invalid UTF-8 sequence detected in:}" ..
              "%{warn:" .. word .. "}" ..
              "%{warn:It may produce unexpected results.}")
        wl = bad
      end
      if (pos == 0) then
        advance, n = string.gsub(word, "^(%s*– ).*", "%1")
        if (n == 0) then
          advance = string.gsub(word, "^(%s*).*", "%1")
        end
        advance = string.gsub(advance, "– ", "  ")
        pos = pos + wl
      elseif  (pos + wl  < 81) or
             ((pos + wl == 81) and string.match(word, "\n$")) then
        pos = pos + wl
      else
        word = advance .. string.gsub(word, "^%s*", "")
        output = output .. "\n"
        pos = utf8.len(word)
      end
      output = output .. word
      if pos > 80 then
        pos = 0
        if not string.match(word, "\n$") then
          output = output .. "\n"
        end
      end
    end
  end
  output = string.gsub(output, "\n*$", "\n")
  return output
end

-- Because rpmbuild will fail if a subpackage is declared before the source
-- package itself, provide a source package declaration shell as fallback.
local function srcpkg(verbose)
  if verbose then
    rpm.expand([[
%{echo:Creating a header for the SRPM from %%{source_name}, %%{source_summary} and}
%{echo:%%{source_description}. If that is not the intended result, please declare the}
%{echo:SRPM header and set %%{source_name} in your spec file before calling a macro}
%{echo:that creates other package headers.}
]])
  end
  print(rpm.expand([[
Name:           %{source_name}
Summary:        %{source_summary}
%description
%wordwrap -v source_description
]]))
  explicitset("currentname", "%{source_name}", verbose)
end

-- %new_package core
local function new_package(source_name, pkg_name, name_suffix, first, verbose)
  -- Safety net when the wrapper is used in conjunction with traditional syntax
  if (not first) and (not source_name) then
    rpm.expand([[
%{warn:Something already set a package name. However, %%{source_name} is not set.}
%{warn:Please set %%{source_name} to the SRPM name to ensure reliable processing.}
]])
    if name_suffix then
      print(rpm.expand("%package        " .. name_suffix))
    else
      print(rpm.expand("%package     -n " .. pkg_name))
    end
    return
  end
  -- New processing
  if not (pkg_name or name_suffix or source_name) then
    rpm.expand([[
%{error:You need to set %%{source_name} or provide explicit package naming!}
]])
  end
  if name_suffix then
    print(rpm.expand("%package        "  .. name_suffix))
    explicitset("currentname", "%{source_name}-" .. name_suffix, verbose)
  else
    if not source_name then
      source_name = pkg_name
    end
    if (pkg_name == source_name) then
      safeset("source_name", source_name, verbose)
      print(rpm.expand("Name:           %{source_name}"))
    else
      if source_name and first then
        srcpkg(verbose)
      end
      print(rpm.expand("%package     -n " .. pkg_name))
    end
    explicitset("currentname", pkg_name, verbose)
  end
end

return {
  read          = read,
  hasflag       = hasflag,
  readflag      = readflag,
  explicitset   = explicitset,
  explicitunset = explicitunset,
  safeset       = safeset,
  zalias        = zalias,
  setcurrent    = setcurrent,
  echovars      = echovars,
  getsuffixed   = getsuffixed,
  getsuffixes   = getsuffixes,
  getbestsuffix = getbestsuffix,
  writevars     = writevars,
  wordwrap      = wordwrap,
  new_package   = new_package,
}
