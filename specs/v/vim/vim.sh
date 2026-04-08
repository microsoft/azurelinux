if [ -n "${BASH_VERSION-}" -o -n "${KSH_VERSION-}" -o -n "${ZSH_VERSION-}" ]; then
  # This will avoid user defined aliases and possibly stuff defined earlier in the PATH.
  case "$(command -v vim)-$(command -v vi)" in
    /usr/bin/vim-/usr/bin/vi)
        # apply only when founded vim and vi are in expected dirs from distro
        alias vi=vim
        ;;
  esac
fi
