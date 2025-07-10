from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import FAQ
from .forms import FAQForm


def about(request):
    faqs = FAQ.objects.all()
    is_admin = request.user.is_authenticated and request.user.is_staff
    context = {
        'faqs': faqs,
        'is_admin': is_admin,
    }
    return render(request, 'about/about.html', context)


@staff_member_required
def manage_faq(request):
    faqs = FAQ.objects.all()
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about')
    else:
        form = FAQForm()
        return render(
                request,
                'about/manage_faq.html',
                {'form': form, 'faqs': faqs}
        )


@staff_member_required
def delete_faq(request, faq_id):
    FAQ.objects.filter(id=faq_id).delete()
    return redirect('manage_faq')


@staff_member_required
def edit_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('manage_faq')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'about/edit_faq.html', {'form': form, 'faq': faq})