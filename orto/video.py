import markdown


class ImageVideoExtension(markdown.Extension):
    def __init__(self, configs):
        self.config = {
            'video-class':
            'responsive-video' if not configs or 'video-class' not in configs
            else configs['video-class'],
            'image-class':
            'responsive-img materialboxed center-align' if not configs
            or 'image-class' not in configs else configs['image-class']
        }

    def extendMarkdown(self, md, md_globals):
        pattern = ImageVideoInlineProcessor(r'\!\[', md)
        pattern.ext = self
        md.inlinePatterns.register(pattern, 'image_link', 150)


class ImageVideoInlineProcessor(markdown.inlinepatterns.LinkInlineProcessor):
    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None
        src, title, index, handled = self.getLink(data, index)
        if not src.startswith('/'):
            src = '{{ dirname }}/' + src
        if src.startswith('./'):
            src = '{{ dirname }}/' + src[2:]
        if not handled:
            return None, None, None
        if src.split('.')[-1] in ('mp4', 'webm'):
            el = markdown.util.etree.Element('video')
            el.set('class', self.ext.config['video-class'])
            el.set('controls', '')
            for attr in self.unescape(text).split():
                el.set(attr, '')
            src_mp4 = markdown.util.etree.SubElement(el, 'source')
            src_mp4.set('src', '.'.join(src.split('.')[:-1]) + '.mp4')
            src_mp4.set('type', 'video/mp4')
            src_webm = markdown.util.etree.SubElement(el, 'source')
            src_webm.set('src', '.'.join(src.split('.')[:-1]) + '.webm')
            src_webm.set('type', 'video/webm')
        elif src.split('.')[-1] in ('mp3', 'wav'):
            pass
        else:
            el = markdown.util.etree.Element('img')
            el.set('class', self.ext.config['image-class'])
            el.set("src", src)
            if title is not None:
                el.set("style", title)
            el.set("alt", self.unescape(text))
        return el, m.start(0), index


def makeExtension(configs=None):
    return ImageVideoExtension(configs=configs)
