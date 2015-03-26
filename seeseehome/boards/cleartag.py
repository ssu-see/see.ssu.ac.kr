import re


class ClearTag:
    step1 = re.compile(r'(&#*\w+)[\x00-\x20]+;', re.U | re.I)
    step2 = re.compile(r'(&#x*[0-9A-F]+);*', re.U | re.I)
    step3 = re.compile(r'(<[^>]+?[\x00-\x20"\'])(?:on|xmlns)[^>]*>', re.U | re.I)
    step4 = re.compile(
        r'([a-z]*)[\x00-\x20]*=[\x00-\x20]*([`\'"]*)[\x00-\x20]*j[\x00-\x20]*a[\x00-\x20]*v[\x00-\x20]*a[\x00-\x20]*s[\x00-\x20]*c[\x00-\x20]*r[\x00-\x20]*i[\x00-\x20]*p[\x00-\x20]*t[\x00-\x20]*:',
        re.U | re.I)
    step5 = re.compile(r'([a-z]*)[\x00-\x20]*=([\'"]*)[\x00-\x20]*-moz-binding[\x00-\x20]*:', re.U | re.I)
    step6 = re.compile(r'(<[^>]+?)style[\x00-\x20]*=[\x00-\x20]*[`\'"]*.*?expression[\x00-\x20]*\([^>]*>', re.U | re.I)
    step7 = re.compile(r'(<[^>]+?)style[\x00-\x20]*=[\x00-\x20]*[`\'"]*.*?behaviour[\x00-\x20]*\([^>]*>', re.U | re.I)
    step8 = re.compile(
        r'(<[^>]+?)style[\x00-\x20]*=[\x00-\x20]*[`\'"]*.*?s[\x00-\x20]*c[\x00-\x20]*r[\x00-\x20]*i[\x00-\x20]*p[\x00-\x20]*t[\x00-\x20]*:*[^>]*>',
        re.U | re.I)
    step9 = re.compile(r'</*\w+:\w[^>]*>', re.U | re.I)
    step10 = re.compile(
        r'<(/*)?(applet|input|form|b(?:ase|gsound|link)|embed|frame(?:set)?|i(?:frame|layer)|l(?:ayer|ink)|meta|object|s(?:cript|tyle)|title|xml)[^>]*>',
        re.U | re.I)

    def clear_tag(self, data):
        data = ClearTag.step1.sub(r'\1;', data)
        data = ClearTag.step2.sub(r'\1;', data)
        data = ClearTag.step3.sub(r'\1>', data)
        data = ClearTag.step4.sub(r'$1=$2novbscript...', data)
        data = ClearTag.step5.sub(r'\1=\2nomozbinding...', data)
        data = ClearTag.step6.sub(r'\1>', data)
        data = ClearTag.step7.sub(r'\1>', data)
        data = ClearTag.step8.sub(r'\1>', data)
        data = ClearTag.step9.sub('', data)

        old_data = data
        data = ClearTag.step10.sub(
            lambda m: '&lt;' +
            m.group(2) +
            '&gt;' if len(
                m.group(1)) == 0 else '&lt;/' +
            m.group(2) +
            '&gt;',
            data)

        while(old_data != data):
            old_data = data
            data = ClearTag.step10.sub(
                lambda m: '&lt;' +
                m.group(2) +
                '&gt;' if len(
                    m.group(1)) == 0 else '&lt;/' +
                m.group(2) +
                '&gt;',
                data)

        return data
