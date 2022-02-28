#!/usr/bin/lua
-- rpm call
-- lua -- copy_jdk_configs.lua   --currentjvm "%{uniquesuffix %{nil}}" --jvmdir "%{_jvmdir %{nil}}" --origname "%{name}" --origjavaver "%{javaver}" --arch "%{_arch}" --debug true
--test call
--lua -- copy_jdk_configs.lua   --currentjvm "java-1.8.0-openjdk-1.8.0.65-3.b17.fc22.x86_64" --jvmdir "/usr/lib/jvm" --origname "java-1.8.0-openjdk" --origjavaver "1.8.0" --arch "x86_64" --debug true  --jvmDestdir /home/jvanek/Desktop

local caredFiles = {"jre/lib/calendars.properties",
              "jre/lib/content-types.properties",
              "jre/lib/flavormap.properties",
              "jre/lib/logging.properties",
              "jre/lib/net.properties",
              "jre/lib/psfontj2d.properties",
              "jre/lib/sound.properties",
              "jre/lib/deployment.properties",
              "jre/lib/deployment.config",
              "jre/lib/security/US_export_policy.jar",
              "jre/lib/security/unlimited/US_export_policy.jar",
              "jre/lib/security/limited/US_export_policy.jar",
              "jre/lib/security/policy/unlimited/US_export_policy.jar",
              "jre/lib/security/policy/limited/US_export_policy.jar",
              "jre/lib/security/java.policy",
              "jre/lib/security/java.security",
              "jre/lib/security/local_policy.jar",
              "jre/lib/security/unlimited/local_policy.jar",
              "jre/lib/security/limited/local_policy.jar",
              "jre/lib/security/policy/unlimited/local_policy.jar",
              "jre/lib/security/policy/limited/local_policy.jar",
              "jre/lib/security/nss.cfg",
              "jre/lib/security/cacerts",
              "jre/lib/security/blacklisted.certs",
              "jre/lib/security/jssecacerts",
              "jre/lib/security/trusted.certs",
              "jre/lib/security/trusted.jssecerts",
              "jre/lib/security/trusted.clientcerts",
              "jre/lib/ext",
              "jre/lib/security/blacklist",
              "jre/lib/security/javaws.policy",
              "lib/security",
              "conf",
              "lib/ext"}

-- before import to allow run from spec
if (arg[1] == "--list") then 
  for i,file in pairs(caredFiles) do
    print(file)
  end
  return 0;
end  

-- yum install lua-posix
local posix = require "posix"

-- the one we are installing
local currentjvm = nil
local jvmdir = nil
local jvmDestdir = nil
local origname = nil
local origjavaver = nil
local arch = nil
local debug = false;
local temp = nil;
local dry = false;

for i=1,#arg,2 do 
  if (arg[i] == "--help" or arg[i] == "-h") then 
    print("all but jvmDestdir and debug are mandatory")
    print("  --currentjvm")
    print("    NVRA of currently installed java")
    print("  --jvmdir") 
    print("    Directory where to find this kind of virtual machine. Generally /usr/lib/jvm")
    print("  --origname")
    print("    convinient switch to determine jdk. Generally java-1.X.0-vendor")
    print("  --origjavaver")
    print("    convinient switch to determine jdk's version. Generally 1.X.0")
    print("  --arch")
    print("    convinient switch to determine jdk's arch")
    print("  --jvmDestdir")
    print("    Migration/testing switch. Target Mostly same as jvmdir, but you may wont to copy ouside it.")
    print("  --debug")
    print("    Enables printing out whats going on. true/false. False by default")
    print("  --temp")
    print("    optional file to save intermediate result - directory configs were copied from")
    print("  --dry")
    print("    true/fase if true, then no changes will be written to disk except one tmp file. False by default")
    print("  **** specil parasm ****")
    print("  --list")
    print("    if present on cmdline, list all cared files and exists")
    os.exit(0)
  end
  if (arg[i] == "--currentjvm") then 
    currentjvm=arg[i+1]
  end
  if (arg[i] == "--jvmdir") then 
    jvmdir=arg[i+1]
  end
  if (arg[i] == "--origname") then 
    origname=arg[i+1]
  end
  if (arg[i] == "--origjavaver") then 
    origjavaver=arg[i+1]
  end
  if (arg[i] == "--arch") then 
    arch=arg[i+1]
  end
  if (arg[i] == "--jvmDestdir") then 
    jvmDestdir=arg[i+1]
  end
  if (arg[i] == "--debug") then 
--no string, boolean, workaround
    if (arg[i+1] == "true") then
     debug = true
    end
  end
  if (arg[i] == "--dry") then 
--no string, boolean, workaround
    if (arg[i+1] == "true") then
     dry = true
    end
  end
  if (arg[i] == "--temp") then 
    temp=arg[i+1]
  end
end

if (jvmDestdir == nil) then
jvmDestdir = jvmdir
end


if (debug) then
  print("--currentjvm:");
  print(currentjvm);
  print("--jvmdir:");
  print(jvmdir);
  print("--jvmDestdir:");
  print(jvmDestdir);
  print("--origname:");
  print(origname);
  print("--origjavaver:");
  print(origjavaver);
  print("--arch:");
  print(arch);
  print("--debug:");
  print(debug);
end

local function debugOneLinePrint(string)
  if (debug) then
    print(string)
  end;
end


--trasnform substitute names to lua patterns
local name = string.gsub(string.gsub(origname, "%-", "%%-"), "%.", "%%.")
local javaver = string.gsub(origjavaver, "%.", "%%.")

local jvms = { }

function getPath(str,sep)
    sep=sep or '/'
    return str:match("(.*"..sep..")")
end

function splitToTable(source, pattern)
  local i1 = string.gmatch(source, pattern) 
  local l1 = {}
  for i in i1 do
    table.insert(l1, i)
  end
  return l1
end

local function slurp(path)
    local f = io.open(path)
    local s = f:read("*a")
    f:close()
    return s
end

function trim(s)
  return (s:gsub("^%s*(.-)%s*$", "%1"))
end

local function dirWithParents(path)
  local s = ""
  local dirs = splitToTable(path, "[^/]+") 
  for i,d in pairs(dirs) do
    if (i == #dirs) then
      break
    end
    s = s.."/"..d
    local stat2 = posix.stat(s, "type");
    if (stat2 == nil) then
      debugOneLinePrint(s.." does not exists, creating")
      if (not dry) then
        posix.mkdir(s)
      end
    else
      debugOneLinePrint(s.." exists,not creating")
    end
  end
end


debugOneLinePrint("started")


foundJvms = posix.dir(jvmdir);
if (foundJvms == nil) then
  debugOneLinePrint("no, or nothing in "..jvmdir.." exit")
  return
end

debugOneLinePrint("found "..#foundJvms.."jvms")

for i,p in pairs(foundJvms) do
-- regex similar to %{_jvmdir}/%{name}-%{javaver}*%{_arch} bash command
  if (string.find(p, name.."%-"..javaver..".*"..arch) ~= nil ) then
    debugOneLinePrint("matched:  "..p)
    if (currentjvm ==  p) then
      debugOneLinePrint("this jdk is already installed. exiting lua script")
      return
    end ;
    if (string.match(p, ".*-debug$")) then
      print(p.." matched but seems to be debug variant. Skipping")
    else
      table.insert(jvms, p)
    end
  else
    debugOneLinePrint("NOT matched:  "..p)
  end
end

if (#jvms <=0) then 
  debugOneLinePrint("no matching jdk in "..jvmdir.." exit")
  return
end;

debugOneLinePrint("matched "..#jvms.." jdk in "..jvmdir)

--full names are like java-1.7.0-openjdk-1.7.0.60-2.4.5.1.fc20.x86_64
table.sort(jvms , function(a,b) 
-- version-sort
-- split on non word: . - 
  local l1 = splitToTable(a, "[^%.-]+") 
  local l2 = splitToTable(b, "[^%.-]+") 
  for x = 1, math.min(#l1, #l2) do
    local l1x = tonumber(l1[x])
    local l2x = tonumber(l2[x])
    if (l1x ~= nil and l2x ~= nil)then
--if hunks are numbers, go with them 
      if (l1x < l2x) then return true; end
      if (l1x > l2x) then return false; end
    else
      if (l1[x] < l2[x]) then return true; end
      if (l1[x] > l2[x]) then return false; end
    end
-- if hunks are equals then move to another pair of hunks
  end
return a<b

end)

if (debug) then
  print("sorted lsit of jvms")
  for i,file in pairs(jvms) do
    print(file)
  end
end

latestjvm = jvms[#jvms]

if ( temp ~= nil ) then
  src=jvmdir.."/"..latestjvm
  debugOneLinePrint("temp declared as "..temp.." saving used dir of "..src)
  file = io.open (temp, "w")
  file:write(src)
  file:close()
end 


local readlinkOutput=os.tmpname()

for i,file in pairs(caredFiles) do
  local SOURCE=jvmdir.."/"..latestjvm.."/"..file
  local DEST=jvmDestdir.."/"..currentjvm.."/"..file
  debugOneLinePrint("going to copy "..SOURCE)
  debugOneLinePrint("to  "..DEST)
  local stat1 = posix.stat(SOURCE, "type");
  if (stat1 ~= nil) then
  debugOneLinePrint(SOURCE.." exists")
  dirWithParents(DEST)
-- Copy with -a to keep everything intact
    local exe = "cp".." -ar "..SOURCE.." "..DEST
    local linkExe = "readlink".." -f "..SOURCE.." > "..readlinkOutput
    debugOneLinePrint("executing "..linkExe)
    os.remove(readlinkOutput)
    os.execute(linkExe)
    local link=trim(slurp(readlinkOutput))
    debugOneLinePrint("  ...link is "..link)
    if (not ((link) == (SOURCE))) then
      debugOneLinePrint("WARNING link "..link.." where file "..SOURCE.." expected!")
      debugOneLinePrint("Will try to copy link target rather then link itself!")
--replacing  any NVRA by future NVRA (still execting to have NVRA for any multiple-installable targets
-- lua stubbornly consider dash as inteval. Replacing by dot to match X-Y more correct as X.Y rather then not at all
      local linkDest=string.gsub(link, latestjvm:gsub("-", "."), currentjvm)
      debugOneLinePrint("attempting to copy "..link.." to "..linkDest)
      if (link == linkDest) then
        debugOneLinePrint("Those are identical files! Nothing to do!")
      else
        local exe2 = "cp".." -ar "..link.." "..linkDest
        dirWithParents(linkDest)
        debugOneLinePrint("executing "..exe2)
        if (not dry) then
          os.execute(exe2)
        end
      end
    else
      debugOneLinePrint("executing "..exe)
      if (not dry) then
        os.execute(exe)
      end
    end
  else
    debugOneLinePrint(SOURCE.." does not exists")
  end
end
