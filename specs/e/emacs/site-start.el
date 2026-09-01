;;; site-start.el --- loaded before user's ".emacs" file and default.el -*- lexical-binding: t -*-

;;; Commentary:
;;
;; Load *.el and *.elc in /usr/share/emacs/site-lisp/site-start.d on startup

;;; Code:

(mapc
 'load
 (delete-dups
  (mapcar 'file-name-sans-extension
          (directory-files
           "/usr/share/emacs/site-lisp/site-start.d" t "\\.elc?\\'"))))

;;; site-start.el ends here
