-- LuaRocks configuration

rocks_trees = {
   { name = "user", root = home .. "/.luarocks" };
   { name = "system", root = "/usr" };
}
lua_interpreter = "lua-5.1";
variables = {
   LUA_DIR = "/usr";
   LUA_BINDIR = "/usr/bin";
}
