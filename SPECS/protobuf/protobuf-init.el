; Protobuf major mode, init file by Tim Niemueller [www.niemueller.de], BSD
; Add mode to automatically recognized modes
(setq auto-mode-alist (cons '("\\.proto$" . protobuf-mode) auto-mode-alist))
(autoload 'protobuf-mode "protobuf-mode" "Google protobuf editing mode." t)
; Turn on colorization by default
(add-hook 'protobuf-mode-hook 'turn-on-font-lock)
