from doing.models import Category

def categories(request):
    """
    Define categories for all navigation links.
    :param request:
    :return:
    """
    return {
        'category_list': list(Category.objects.all())
    }
