;; Activate autoconf-mode

;; Uncomment the following code if you feel that autoconf-mode.el does better
;; job than Emacs's default autoconf.el.

;; (autoload 'autoconf-mode "autoconf-mode"
;;           "Major mode for editing autoconf files." t)
;; (setq auto-mode-alist
;;       (cons '("\.ac\'\|configure\.in\'" . autoconf-mode)
;;             auto-mode-alist))

;; Activate autotest-mode
(autoload 'autotest-mode "autotest-mode"
         "Major mode for editing autotest files." t)
(setq auto-mode-alist
      (cons '("\.at\'" . autotest-mode) auto-mode-alist))
