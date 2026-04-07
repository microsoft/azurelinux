define(`colornormal', `setcolor(39;49)')dnl
define(`colorreset', `setcolor(0)')dnl
define(`colorvar', `when($1,setcolor(${$1}))')dnl
define(`setcolor', `\[\e[$1m\]')dnl
define(`when', `${$1:+$2}')dnl
