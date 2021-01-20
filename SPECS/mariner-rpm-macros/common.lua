-- Convenience Lua functions that can be used within rpm macros

-- Set a spec variable
-- Echo the result if verbose
local function explicitset(rpmvar, value, verbose)
  local value = value
  if (value == nil) or (value == "") then
    value = "%{nil}"
  end
  rpm.define(rpmvar .. " " .. value)
  if verbose then
    rpm.expand("%{echo:Setting %%{" .. rpmvar .. "} = " .. value .. "}")
  end
end

-- Unset a spec variable if it is defined
-- Echo the result if verbose
local function explicitunset(rpmvar, verbose)
  if (rpm.expand("%{" .. rpmvar .. "}") ~= "%{" .. rpmvar .. "}") then
    rpm.define(rpmvar .. " %{nil}")
    if verbose then
      rpm.expand("%{echo:Unsetting %%{" .. rpmvar .. "}}")
    end
  end
end

-- Set a spec variable, if not already set
-- Echo the result if verbose
local function safeset(rpmvar, value, verbose)
  if (rpm.expand("%{" .. rpmvar .. "}") == "%{" .. rpmvar .. "}") then
    explicitset(rpmvar,value,verbose)
  end
end

-- Alias a list of rpm variables to the same variables suffixed with 0 (and vice versa)
-- Echo the result if verbose
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

-- https://github.com/rpm-software-management/rpm/issues/581
-- Writes the content of a list of rpm variables to a macro spec file.
-- The target file must contain the corresponding anchors.
-- For example writevars("myfile", {"foo","bar"}) will replace:
--   @@FOO@@ with the rpm evaluation of %{foo} and
--   @@BAR@@ with the rpm evaluation of %{bar}
-- in myfile
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
        print("%{warn: Invalid UTF-8 sequence detected in:\n" ..
               word .. "\nIt may produce unexpected results.\n}")
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

return {
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
}
