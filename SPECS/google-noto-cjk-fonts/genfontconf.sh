#!/usr/bin/bash -x

# Generate for google-noto-sans-cjk-ttc-fonts
python3 genfontconf.py "ja" "monospace" "Noto Sans Mono CJK JP" \
        "ja" "sans-serif" "Noto Sans CJK JP" \
        "ko" "monospace" "Noto Sans Mono CJK KR" \
        "ko" "sans-serif" "Noto Sans CJK KR" \
        "zh-cn:zh-sg" "monospace" "Noto Sans Mono CJK SC" \
        "zh-cn:zh-sg" "sans-serif" "Noto Sans CJK SC" \
        "zh-tw:zh-mo" "monospace" "Noto Sans Mono CJK TC" \
        "zh-tw:zh-mo" "sans-serif" "Noto Sans CJK TC" \
        "zh-hk" "monospace" "Noto Sans Mono CJK HK" \
        "zh-hk" "sans-serif" "Noto Sans CJK HK" \
    | xmllint --format - |tee 65-0-google-noto-sans-cjk-ttc.conf

# Generate for google-noto-serif-cjk-ttc-fonts
python3 genfontconf.py "ja" "serif" "Noto Serif CJK JP" \
        "ko" "serif" "Noto Serif CJK KR" \
        "zh-cn:zh-sg" "serif" "Noto Serif CJK SC" \
        "zh-tw:zh-hk:zh-mo" "serif" "Noto Serif CJK TC" \
    | xmllint --format - |tee 65-0-google-noto-serif-cjk-ttc.conf

# Generate for google-noto-sans-cjk-jp-fonts, google-noto-serif-cjk-jp-fonts and google-noto-sans-mono-cjk-jp-fonts
python3 genfontconf.py "ja" "sans-serif" "Noto Sans CJK JP" | xmllint --format - |tee 66-google-noto-sans-cjk-jp.conf

python3 genfontconf.py "ja" "serif" "Noto Serif CJK JP" | xmllint --format - |tee 66-google-noto-serif-cjk-jp.conf

python3 genfontconf.py "ja" "monospace" "Noto Sans Mono CJK JP" | xmllint --format - |tee 66-google-noto-sans-mono-cjk-jp.conf

# Generate for google-noto-sans-cjk-kr-fonts, google-noto-serif-cjk-kr-fonts and google-noto-sans-mono-cjk-kr-fonts
python3 genfontconf.py "ko" "sans-serif" "Noto Sans CJK KR" | xmllint --format - |tee 66-google-noto-sans-cjk-kr.conf

python3 genfontconf.py "ko" "serif" "Noto Serif CJK KR" | xmllint --format - |tee 66-google-noto-serif-cjk-kr.conf

python3 genfontconf.py "ko" "monospace" "Noto Sans Mono CJK KR" | xmllint --format - |tee 66-google-noto-sans-mono-cjk-kr.conf

# Generate for google-noto-sans-cjk-sc-fonts, google-noto-serif-cjk-sc-fonts and google-noto-sans-mono-cjk-sc-fonts
python3 genfontconf.py "zh-cn:zh-sg" "sans-serif" "Noto Sans CJK SC" | xmllint --format - |tee 66-google-noto-sans-cjk-sc.conf

python3 genfontconf.py "zh-cn:zh-sg" "serif" "Noto Serif CJK SC" | xmllint --format - |tee 66-google-noto-serif-cjk-sc.conf

python3 genfontconf.py "zh-cn:zh-sg" "monospace" "Noto Sans Mono CJK SC" | xmllint --format - |tee 66-google-noto-sans-mono-cjk-sc.conf

# Generate for google-noto-sans-cjk-tc-fonts, google-noto-serif-cjk-tc-fonts and google-noto-sans-mono-cjk-tc-fonts
python3 genfontconf.py "zh-tw:zh-mo" "sans-serif" "Noto Sans CJK TC" | xmllint --format - |tee 66-google-noto-sans-cjk-tc.conf

python3 genfontconf.py "zh-tw:zh-hk:zh-mo" "serif" "Noto Serif CJK TC" | xmllint --format - |tee 66-google-noto-serif-cjk-tc.conf

python3 genfontconf.py "zh-tw:zh-mo" "monospace" "Noto Sans Mono CJK TC" | xmllint --format - |tee 66-google-noto-sans-mono-cjk-tc.conf

# Generate for google-noto-sans-cjk-hk-fonts and google-noto-sans-mono-cjk-hk-fonts
python3 genfontconf.py "zh-hk" "sans-serif" "Noto Sans CJK HK" | xmllint --format - |tee 66-google-noto-sans-cjk-hk.conf

python3 genfontconf.py "zh-hk" "monospace" "Noto Sans Mono CJK HK" | xmllint --format - |tee 66-google-noto-sans-mono-cjk-hk.conf

# Generate for google-noto-sans-jp-fonts and google-noto-serif-jp-fonts
python3 genfontconf.py "ja" "sans-serif" "Noto Sans JP" | xmllint --format - |tee 66-google-noto-sans-jp.conf

python3 genfontconf.py "ja" "serif" "Noto Serif JP" | xmllint --format - |tee 66-google-noto-serif-jp.conf

# Generate for google-noto-sans-kr-fonts and google-noto-serif-kr-fonts
python3 genfontconf.py "ko" "sans-serif" "Noto Sans KR" | xmllint --format - |tee 66-google-noto-sans-kr.conf

python3 genfontconf.py "ko" "serif" "Noto Serif KR" | xmllint --format - |tee 66-google-noto-serif-kr.conf

# Generate for google-noto-sans-sc-fonts and google-noto-serif-sc-fonts
python3 genfontconf.py "zh-cn:zh-sg" "sans-serif" "Noto Sans SC" | xmllint --format - |tee 66-google-noto-sans-sc.conf

python3 genfontconf.py "zh-cn:zh-sg" "serif" "Noto Serif SC" | xmllint --format - |tee 66-google-noto-serif-sc.conf

# Generate for google-noto-sans-tc-fonts and google-noto-serif-tc-fonts
python3 genfontconf.py "zh-tw:zh-mo" "sans-serif" "Noto Sans TC" | xmllint --format - |tee 66-google-noto-sans-tc.conf

python3 genfontconf.py "zh-tw:zh-hk:zh-mo" "serif" "Noto Serif TC" | xmllint --format - |tee 66-google-noto-serif-tc.conf

# Generate for google-noto-sans-hk-fonts
python3 genfontconf.py "zh-hk" "sans-serif" "Noto Sans HK" | xmllint --format - |tee 66-google-noto-sans-hk.conf
