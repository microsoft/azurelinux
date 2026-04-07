;;; clhs.el --- Access the Common Lisp HyperSpec (CLHS)   -*- lexical-binding: t -*-
;; Version: 2
;; Homepage: https://gitlab.com/sam-s/clhs
;; Maintainer: Sam Steingold <sds@gnu.org>

;;; This works with both
;;; * the "long file name" version released by Harlequin and available
;;;   at the MIT web site as
;;;   http://www.ai.mit.edu/projects/iiip/doc/CommonLISP/HyperSpec/FrontMatter/
;;; * the "8.3 file name" version released later by Xanalys/LispWorks and
;;;   available at http://www.lispworks.com/documentation/common-lisp.html
;;; This is accomplished by not hard-wiring the symbol->file table
;;; but reading the Data/<map> file instead.

;;; Copyright (C) 2002-2008, 2017, 2019, 2021 Sam Steingold <sds@gnu.org>
;;; Keywords: lisp, common lisp, emacs, ANSI CL, hyperspec
;;; released under the GNU GPL <https://www.gnu.org/copyleft/gpl.html>
;;; as a part of GNU CLISP <https://www.clisp.org>

;;; Usage:

;; (autoload 'clhs-doc "clhs" "Get doc on ANSI CL" t)
;; (define-key help-map "\C-l" 'clhs-doc)
;; (custom-set-variables
;;  '(tags-apropos-additional-actions '(("Common Lisp" clhs-doc clhs-symbols))))

;;; Commentary:

;; Kent Pitman and the Harlequin Group (later Xanalys) have made the
;; text of the "American National Standard for Information Technology --
;; Programming Language -- Common Lisp", ANSI X3.226-1994 available on
;; the WWW, in the form of the Common Lisp HyperSpec.  This package
;; makes it convenient to peruse this documentation from within Emacs.

;; This is inspired by the Erik Naggum's version of 1997.

;;; Code:

(require 'browse-url)
(require 'thingatpt)
(require 'url)

(defvar clhs-symbols nil)

(defcustom clhs-root "http://clhs.lisp.se/"
  ;; "http://www.lispworks.com/documentation/HyperSpec/"
  ;; "http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/html/hyperspec/HyperSpec/"
  ;; "http://www.ai.mit.edu/projects/iiip/doc/CommonLISP/HyperSpec/"
  "*The root of the Common Lisp HyperSpec URL.
If you copy the HyperSpec to your local system, set this variable to
something like \"file:/usr/local/doc/HyperSpec/\"."
  :group 'lisp
  :set (lambda (s v)
         (setq clhs-symbols nil)
         (set-default s v))
  :type 'string)

(defvar clhs-history nil
  "History of symbols looked up in the Common Lisp HyperSpec so far.")

(defun clhs-table-buffer (&optional root)
  "Create a buffer containing the CLHS symbol table.
Optional argument ROOT specifies the CLHS root location
 and defaults to `clhs-root'."
  (unless root (setq root clhs-root))
  (if (string-match "^file:/" root)
      (with-current-buffer (get-buffer-create " *clhs-tmp-buf*")
        (insert-file-contents-literally
         (let* ((d (concat (substring root 6) "/Data/"))
                (f (concat d "Map_Sym.txt")))
           (if (file-exists-p f) f
             (setq f (concat d "Symbol-Table.text"))
             (if (file-exists-p f) f
               (error "No symbol table at %s" root))))
         nil nil nil t)
        (goto-char 0)
        (current-buffer))
    (let* ((d (concat root "/Data/"))
           (f (concat d "Map_Sym.txt")))
      (set-buffer (url-retrieve-synchronously f))
      (goto-char 0)
      (unless (looking-at "^HTTP/.*200 *OK$")
        (kill-buffer (current-buffer))
        (setq f (concat d "Symbol-Table.text"))
        (set-buffer (url-retrieve-synchronously f))
        (goto-char 0)
        (unless (looking-at "^HTTP/.*200 *OK$")
          (kill-buffer (current-buffer))
          (error "No symbol table at %s" root)))
      ;; skip to the first symbol
      (search-forward "\n\n")
      (current-buffer))))

(defun clhs-read-symbols ()
  "Read variable `clhs-symbols' from the current position in the current buffer."
  (while (not (eobp))
    (puthash (buffer-substring-no-properties ; symbol
              (line-beginning-position) (line-end-position))
             (progn (forward-line 1) ; file name
                    (buffer-substring-no-properties ; strip "../"
                     (+ 3 (line-beginning-position)) (line-end-position)))
             clhs-symbols)
    (forward-line 1)))

(defun clhs-symbols ()
  "Get variable `clhs-symbols' from `clhs-root'."
  (if (and clhs-symbols (not (= 0 (hash-table-count clhs-symbols))))
      clhs-symbols
    (with-current-buffer (clhs-table-buffer)
      (unless clhs-symbols
        (setq clhs-symbols (make-hash-table :test 'equal :size 1031)))
      (clhs-read-symbols)
      (kill-buffer (current-buffer))
      clhs-symbols)))

;;;###autoload
(defun clhs-doc (symbol-name &optional kill)
  "Browse the Common Lisp HyperSpec documentation for SYMBOL-NAME.
Finds the HyperSpec at `clhs-root'.
With prefix arg KILL, save the URL in the `kill-ring' instead."
  (interactive (list (let ((sym (thing-at-point 'symbol t))
                           (completion-ignore-case t))
                       (completing-read
                        "Look-up symbol in the Common Lisp HyperSpec: "
                        (clhs-symbols) nil t sym 'clhs-history))
                     current-prefix-arg))
  (unless (= ?/ (aref clhs-root (1- (length clhs-root))))
    (setq clhs-root (concat clhs-root "/")))
  (let ((url (concat clhs-root (gethash (upcase symbol-name) (clhs-symbols)))))
    (if kill
        (kill-new url)
      (browse-url url))))

(provide 'clhs)

;;; clhs.el ends here
