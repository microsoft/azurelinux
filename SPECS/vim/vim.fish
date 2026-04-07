# This will avoid user defined aliases and possibly stuff defined earlier in the PATH.
# Redirecting is for the case when the binary is missing.
set vim_cond (command -v vim)
set vi_cond (command -v vi)

switch "$vim_cond-$vi_cond"
  case /usr/bin/vim-/usr/bin/vi
      # apply only if founded vim and vi are in the expected dir from distro
      function vi
        command vim $argv
      end
end

# just in case remove the variables
set -e vim_cond
set -e vi_cond
