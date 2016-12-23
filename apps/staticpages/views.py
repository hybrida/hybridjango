from django.urls import resolve
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

pages = [
    ('about', "Om Hybrida"),
    ('contact_us', "Kontakt Oss"),
    ('board', "Styret"),
    ('committees', "Komitéer"),
    ('griff_orden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('lyrics', "Sangtekster"),
]

class AboutView(TemplateResponseMixin, ContextMixin, View):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        active_page = resolve(request.path_info).url_name
        before_pages = []
        after_pages = []
        page_found = False
        for page in pages:
            if page_found:
                after_pages.append(page)
            else:
                before_pages.append(page)
                if page[0] == active_page:
                    page_found = True

        context['before_pages'] = before_pages
        context['after_pages'] = after_pages
        return self.render_to_response(context)
