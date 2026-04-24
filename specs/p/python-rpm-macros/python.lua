-- Convenience Lua functions that can be used within Python srpm/rpm macros

-- Determine alternate names provided from the given name.
-- Used in pythonname provides generator, python_provide and py_provides.
-- If only_3_to_3_X is false/nil/unused there are 2 rules:
--  python3-foo  -> python-foo, python3.X-foo
--  python3.X-foo -> python-foo, python3-foo
-- If only_3_to_3_X is true there is only 1 rule:
--  python3-foo  -> python3.X-foo
-- There is no python-foo -> rule, python-foo packages are version agnostic.
-- Returns a table/array with strings. Empty when no rule matched.
local function python_altnames(name, only_3_to_3_X)
  local xy = rpm.expand('%{__default_python3_pkgversion}')
  local altnames = {}
  local replaced
  -- NB: dash needs to be escaped!
  if name:match('^python3%-') then
    local prefixes = only_3_to_3_X and {} or {'python-'}
    for i, prefix in ipairs({'python' .. xy .. '-', table.unpack(prefixes)}) do
      replaced = name:gsub('^python3%-', prefix)
      table.insert(altnames, replaced)
    end
  elseif name:match('^python' .. xy .. '%-') and not only_3_to_3_X then
    for i, prefix in ipairs({'python-', 'python3-'}) do
      replaced = name:gsub('^python' .. xy .. '%-', prefix)
      table.insert(altnames, replaced)
    end
  end
  return altnames
end


local function __python_alttags(name, evr, tag_type)
  -- for the "provides" tag_type we want also unversioned provides
  local only_3_to_3_X = tag_type ~= "provides"
  local operator = tag_type == "provides" and ' = ' or ' < '

  -- global cache that tells what package NEVRs were already processed for the
  -- given tag type
  if __python_alttags_beenthere == nil then
    __python_alttags_beenthere = {}
  end
  if __python_alttags_beenthere[tag_type] == nil then
    __python_alttags_beenthere[tag_type] = {}
  end
  __python_alttags_beenthere[tag_type][name .. ' ' .. evr] = true
  local alttags = {}
  for i, altname in ipairs(python_altnames(name, only_3_to_3_X)) do
    table.insert(alttags, altname .. operator .. evr)
  end
  return alttags
end

-- For any given name and epoch-version-release, return provides except self.
-- Uses python_altnames under the hood
-- Returns a table/array with strings.
local function python_altprovides(name, evr)
  return __python_alttags(name, evr, "provides")
end

-- For any given name and epoch-version-release, return versioned obsoletes except self.
-- Uses python_altnames under the hood
-- Returns a table/array with strings.
local function python_altobsoletes(name, evr)
  return __python_alttags(name, evr, "obsoletes")
end


local function __python_alttags_once(name, evr, tag_type)
  -- global cache that tells what provides were already processed
  if __python_alttags_beenthere == nil
      or __python_alttags_beenthere[tag_type] == nil
      or __python_alttags_beenthere[tag_type][name .. ' ' .. evr] == nil then
    return __python_alttags(name, evr, tag_type)
  else
    return nil
  end
end

-- Like python_altprovides but only return something once.
-- For each argument can only be used once, returns nil otherwise.
-- Previous usage of python_altprovides counts as well.
local function python_altprovides_once(name, evr)
  return __python_alttags_once(name, evr, "provides")
end

-- Like python_altobsoletes but only return something once.
-- For each argument can only be used once, returns nil otherwise.
-- Previous usage of python_altobsoletes counts as well.
local function python_altobsoletes_once(name, evr)
  return __python_alttags_once(name, evr, "obsoletes")
end


return {
  python_altnames = python_altnames,
  python_altprovides = python_altprovides,
  python_altobsoletes = python_altobsoletes,
  python_altprovides_once = python_altprovides_once,
  python_altobsoletes_once = python_altobsoletes_once,
}
