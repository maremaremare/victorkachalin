# coding: utf-8
from django.views.generic import TemplateView, FormView
from photologue.models import Photo
from shop.models import Order, Merchandise
from shop.forms import OrderForm


class OrderFormView(FormView):
    #current_url = self.request.get_full_path()
    #success_url = current_url+'/success/'
    form_class = OrderForm

    def get_success_url(self):

        return self.request.get_full_path() + 'success/'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk', None)
        item = self.kwargs.get('item', None)
        context = super(OrderFormView, self).get_context_data(**kwargs)
        for i in Merchandise.objects.all():
            if item == i.slug:
                context['item'] = i
                # Add in a QuerySet of all the books
            #context['sidebar_title'] = define_root_Cat(request)
        context['photo'] = Photo.objects.get(id=id)
        context['all_photos'] = Photo.objects.filter(is_public=True)
        context['id'] = id
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'done'
        data = form.cleaned_data
        Order.objects.create(name=data['name'], phone=data['phone'], address=data['address'], email=data['email'],
                             merchandise_id=data['merchandise_id'])
        #merchandise_id = data['id'], extra_field = data['extra'])
        return super(OrderFormView, self).form_valid(form)


class OrderView(TemplateView):
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(OrderView, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk', None)
        item = self.kwargs.get('item', None)
        for i in Merchandise.objects.all():
            if item == i.slug:
                context['item'] = i
        context['photo'] = Photo.objects.get(id=id)
        context['all_photos'] = Photo.objects.filter(is_public=True)
        context['id'] = id
        context['order'] = Order.objects.latest('created_at')

        return context