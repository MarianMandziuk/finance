from django.shortcuts import render, redirect, get_object_or_404
from ..models import Category
from django.views.generic import ListView
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

CATEGORIES_SHOW = 10


class CategoryList(ListView):
    template_name = 'finance/category/list.html'
    context_object_name = 'categories'
    queryset = Category.objects.order_by('-created')[:CATEGORIES_SHOW]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryList, self).dispatch(request, *args, **kwargs)


# def category_list(request):
#     categories = Category.objects.all()
#     context = {'categories': categories,
#                'message': None}
#     return render(request, 'finance/category/list.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
        except KeyError:
            raise Http404
        category = Category(name=name, description=description)
        category.save()
        messages.success(request, 'Category "{}" was successfully created'
                         .format(category.name))
        return redirect("finance:category_list")
    return render(request, 'finance/category/create_update.html')


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category "{}" was successfully deleted'
                     .format(category.name))
    return redirect("finance:category_list")


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', "")
        description = request.POST.get('description', "")
        old_name = category.name
        category.name = name
        category.description = description
        category.save()
        messages.success(request, 'Category "{}" was successfully updated on {}'
                         .format(old_name, category.name))
        return redirect("finance:category_list")
    update = True
    return render(request, "finance/category/create_update.html", {
        'category': category,
        'update': update,
    })
