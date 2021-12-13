#!/usr/bin/python3


import argparse


'''
Generate the font config file for Noto CJK fonts

genfontconf.py "lang list" "common font name" "font name" "fallback font name" "prepend latin font" ...

like

genfontconf.py --fallback-font --prepend-latin-font "zh-cn:zh-sg" "monospace" "Source Han Sans CN" "Source Han Sans TW" "DejaVu Sans Mono" "zh-cn:zh-sg" "serif" "Source Han Sans CN" "Source Han Sans TW" "" "zh-cn:zh-sg" "sans-serif" "Source Han Sans CN" "Source Han Sans TW" ""

genfontconf.py "zh-cn:zh-sg" "monospace" "Noto Sans Mono CJK SC" "zh-cn:zh-sg" "serif" "Noto Serif CJK SC" "zh-cn:zh-sg" "sans-serif" "Noto Sans CJK SC"

The above information is in variable length array.
'''

'''
Some Noto CJK fonts may not need "fallback font name"

Skip the "fallback font name" argument if not needed.
'''

fallback_font_name = False

'''
Noto CJK may not need "prepend latin font".

Skip the "prepend latin font" argument if not needed.
'''

prepend_latin_font = False


class FontConfRecord:

    @staticmethod
    def renderRecord(langlist, common, font, fallback=None, latin=None):
        for lang in langlist.split(":"):
            FontConfRecord.renderMatch(lang, common, font, fallback, latin)
            print()

        FontConfRecord.renderAlias(font, common)
        print()

    @staticmethod
    def renderMatch(lang, common, font, fallback, latin):
        print('<match>')
        FontConfRecord.renderTestLang(lang)
        FontConfRecord.renderTestFamily(common)
        FontConfRecord.renderEditFamily(font, fallback)
        FontConfRecord.renderEditLatinFamily(latin)
        print('</match>')

    @staticmethod
    def renderTestLang(lang):
        print('<test name="lang">')
        print('<string>{0}</string>'.format(lang))
        print('</test>')

    @staticmethod
    def renderTestFamily(common):
        print('<test name="family">')
        print('<string>{0}</string>'.format(common))
        print('</test>')

    @staticmethod
    def renderEditFamily(font, fallback):
        print('<edit name="family" mode="prepend">')
        print('<string>{0}</string>'.format(font))
        if fallback:
            print('<string>{0}</string>'.format(fallback))
        print('</edit>')

    @staticmethod
    def renderEditLatinFamily(latin):
        if not latin:
            return
        print('<edit name="family" mode="prepend" binding="strong">')
        print('<string>{0}</string>'.format(latin))
        print('</edit>')

    @staticmethod
    def renderAlias(font, common):
        print('<alias>')
        print('<family>{0}</family>'.format(font))
        print('<default>')
        print('<family>{0}</family>'.format(common))
        print('</default>')
        print('</alias>')


class FontConfFile:

    @staticmethod
    def renderFile(strings):
        FontConfFile.renderHeader()
        FontConfFile.renderBody(strings)
        FontConfFile.renderFooter()

    @staticmethod
    def renderHeader():
        print('<?xml version="1.0"?>')
        print('<!DOCTYPE fontconfig SYSTEM "fonts.dtd">')
        print('<fontconfig>')

    @staticmethod
    def renderBody(strings):
        num = 3
        if fallback_font_name:
            num += 1
        if prepend_latin_font:
            num += 1

        while len(strings):
            items = strings[0:num]
            strings = strings[num:]

            if num == 3:
                FontConfRecord.renderRecord(items[0], items[1], items[2])

            if num == 4:
                if fallback_font_name:
                    FontConfRecord.renderRecord \
                        (items[0], items[1], items[2], items[3])
                if prepend_latin_font:
                    FontConfRecord.renderRecord \
                        (items[0], items[1], items[2], None, items[3])

            if num == 5:
                FontConfRecord.renderRecord \
                    (items[0], items[1], items[2], items[3], items[4])

    @staticmethod
    def renderFooter():
        print('</fontconfig>')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate font config.')
    parser.add_argument('strings', metavar='string', type=str, nargs='+',
                        help='strings')

    parser.add_argument('--fallback-font', dest='fallback_font', action='store_true')
    parser.add_argument('--disable-fallback-font', dest='fallback_font', action='store_false')
    parser.set_defaults(fallback_font=False)

    parser.add_argument('--prepend-latin-font', dest='prepend_latin_font', action='store_true')
    parser.add_argument('--disable-prepend-latin-font', dest='prepend_latin_font', action='store_false')
    parser.set_defaults(prepend_latin_font=False)

    args = parser.parse_args()
    #print(args)

    fallback_font_name = args.fallback_font
    prepend_latin_font = args.prepend_latin_font

    FontConfFile.renderFile(args.strings)
