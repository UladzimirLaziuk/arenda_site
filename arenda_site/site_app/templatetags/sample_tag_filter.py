import logging
import math

from django import template

register = template.Library()
logger = logging.getLogger(__name__)

@register.simple_tag
def join_buck(dict_order_list):
    return ', '.join((str(el.get('width')) for el in dict_order_list))



@register.simple_tag
def range_page(num_pages, page_size):
    return range(1, int(num_pages) + 1, page_size)


@register.simple_tag
def range_page_pagination(num_pages, total_page, page_size=5):
    total_page = math.ceil(total_page / 10)
    logger.info(f'Total page -{total_page}')

    if num_pages + page_size >= total_page:
        return range(max(1, total_page - page_size + 1), total_page + 1)
    if total_page <= page_size:
        max_range_page = int(total_page) + 1
        return range(1, max_range_page)
    else:
        max_range_page = int(num_pages) + int(page_size)
        return range(int(num_pages), max_range_page)