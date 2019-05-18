from typing import List

from bleach import clean, linkify
from flask import flash
from markdown import markdown


def flash_errors(form):
    for field, errors in form.errors:
        for error in errors:
            flash('错误:<%s>:%s' % (field, error))


def to_html(raw):
    allowed_tags = ['a', 'abbr', 'b', 'br', 'blockquote', 'code', 'del', 'div', 'em', 'img', 'p', 'pre', 'strong',
                    'span', 'ul', 'li', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    allowed_attributes: List[str] = ['src', 'title', 'alt', 'href', 'class']
    html = markdown(raw, output_format='html', extensions=['markdown.extensions.fenced_code',
                                                           'markdown.extensions.codehilite'])
    clean_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)
    return linkify(clean_html)
