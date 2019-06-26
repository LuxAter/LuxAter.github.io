import markdown
import re


class TabExtension(markdown.Extension):
    def __init__(self, configs):
        self.config = {
            'container':
            '<div class="row"><div class="col s12"><ul class="tabs">{}</ul></div>{}</div>',
            'tab_container':
            '<li class="tab"><a href="#{}" class="{}">{}</a></li>',
            'block_container': '<div id="{}" class="col s12 {}">{}</div>',
            'tab_class': 'blue-text',
            'block_class': ''
        }

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        preprocessor = TabBlockPreprocessor(md)
        preprocessor.ext = self
        md.preprocessors.register(preprocessor, 'tab_block', 15)


class TabBlockPreprocessor(markdown.preprocessors.Preprocessor):
    TAB_BLOCK_RE = re.compile(
        r'(?P<fence>^(?:%{3,}))[ ]*(?P<code>.*?)(?<=\n)(?P=fence)[ ]*$',
        re.MULTILINE | re.DOTALL | re.VERBOSE)

    def __init__(self, md):
        super(TabBlockPreprocessor, self).__init__(md)

    def run(self, lines):
        text = "\n".join(lines)
        while True:
            m = self.TAB_BLOCK_RE.search(text)
            if m:
                raw = m.group('code').split('\n\n')
                tabs = [
                    self.ext.config['tab_container'].format(
                        par.split('\n')[0].lower(),
                        self.ext.config['tab_class'],
                        par.split('\n')[0]) for par in raw if len(par)
                ]
                divs = [
                    self.ext.config['block_container'].format(
                        par.split('\n')[0].lower(),
                        self.ext.config['block_class'],
                        '\n'.join(par.split('\n')[1:])) for par in raw
                    if len(par)
                ]
                block = self.ext.config['container'].format(
                    '\n'.join(tabs), '\n'.join(divs))
                text = '{}\n{}\n{}'.format(text[:m.start()], block,
                                           text[m.end():])
            else:
                break
        return text.split('\n')

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(configs=None):
    return TabExtension(configs=configs)
