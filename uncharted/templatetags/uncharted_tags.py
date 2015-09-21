# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag("uncharted/dummy.html")
def render_chart(chart, write_to=None, template_name="uncharted/chart.html"):
    return {
        'chart': chart,
        'output': chart.render(chart.name),
        'write_to': write_to,
        'template': template_name,
    }
