;; anthy-unicode-init.el
;;
(if (featurep 'xemacs)
    (setq load-path (cons "/usr/share/xemacs/xemacs-packages/lisp/anthy-unicode" load-path))
  (setq load-path (cons "/usr/share/emacs/site-lisp/anthy-unicode" load-path)))
(autoload 'anthy-unicode-leim-activate "anthy-unicode" nil t)
(register-input-method "japanese-anthy-unicode" "Japanese"
		       'anthy-unicode-leim-activate "[anthy-unicode]"
		       "Anthy Unicode Kana Kanji conversion system")

