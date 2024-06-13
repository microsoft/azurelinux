;;; loaded before user's ".emacs" file and default.el
 
;; load *.el and *.elc in /usr/share/emacs/site-lisp/site-start.d on startup
(mapc
 'load
 (delete-dups
  (mapcar 'file-name-sans-extension
          (directory-files
           "/usr/share/emacs/site-lisp/site-start.d" t "\\.elc?\\'"))))
