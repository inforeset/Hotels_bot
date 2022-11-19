import lxml.html


def remove_span(html: str) -> str:
    '''
    Just clear html string from all tags
    :param html: str
    :return: str
    '''
    return lxml.html.fromstring(html).text_content()
