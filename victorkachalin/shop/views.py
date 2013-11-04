# coding: utf-8

import urllib
import httplib
import re
import urllib
import urllib2

from pyDes import *
import hashlib
import base64
 
from xml.dom.minidom import parse, parseString

import uuid
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import SingleObjectMixin
from photologue.models import Photo
from shop.models import Order, Item
from shop.forms import OrderForm, EditOrderForm
from django.core.mail import send_mail
from victorkachalin.settings.secrets import QIWI_PASS as q_pass, QIWI_ID as q_id

def make_options(item):
    result = []
    str = item.options
    biglist = str.split('#')
    for j in range(len(biglist)):
        result.append(biglist[j].split(', '))
    return result    

class OrderFormView(FormView):
    #current_url = self.request.get_full_path()
    #success_url = current_url+'/success/'
    form_class = OrderForm
 
    def get_success_url(self):

        return 'http://www.victorkachalin.ru/shop/orders/'+ str(self.order_id)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('id', None)
        item = self.kwargs.get('item', None)
        context = super(OrderFormView, self).get_context_data(**kwargs)
        for i in Item.objects.all():
            if item == i.slug:
                context['item'] = i
                if i.options:
                    context['opt']=make_options(i)
                # Add in a QuerySet of all the books
            #context['sidebar_title'] = define_root_Cat(request)

        context['photo'] = Photo.objects.get(title_slug=id)
        context['all_photos'] = Photo.objects.filter(is_public=True)
        context['id'] = id

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'done'
        data = form.cleaned_data
        order_id = hash(str(uuid.uuid1())) % 100000
        self.order_id = order_id
        Order.objects.create(name=data['name'], phone=data['phone'], address=data['address'], email=data['email'],
                             merchandise_id=data['merchandise_id'], photo_id=data['photo_id'], order_id=order_id, extra_field=data['extra_field'])
        #order_id = str(Order.objects.latest('created_at').id)
        text = u'Здравствуйте, '+data['name']+u'!\n\nБольшое спасибо за заказ!\n\nВы можете приступить к оплате через qiwi-кошелек, просмотреть статус заказа или отменить его по ссылке http://www.victorkachalin.ru/shop/orders/'+str(order_id)+u'\n\nКак только заказ будет оплачен, я свяжусь с Вами лично для дальнейшей встречи или пересылки заказа почтой.\nЕсли мы не свяжемся в течение недели, Вы получите Ваши деньги обратно.\n \nЕсли у Вас есть вопросы, свяжитесь со службой поддержки сайта (support@victorkachalin.ru).\n\nНе нужно отвечать на это письмо, оно высылается автоматически.\n\nИскренне Ваш,\n\nВ.К.'
        send_mail('Ваш заказ #'+str(order_id)+' на сайте victorkachalin.ru', text, 'robot@victorkachalin.ru',
        [data['email']], fail_silently=False)
        #merchandise_id = data['id'], extra_field = data['extra'])
        return super(OrderFormView, self).form_valid(form)


class OrderView(TemplateView):
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(OrderView, self).get_context_data(**kwargs)
        id = self.kwargs.get('id', None)
        item = self.kwargs.get('item', None)
        for i in Item.objects.all():
            if item == i.slug:
                context['item'] = i
        context['photo'] = Photo.objects.get(title_slug=id)
        context['all_photos'] = Photo.objects.filter(is_public=True)
        context['id'] = id
        context['order'] = Order.objects.latest('created_at')

        return context

 
 
def send_xml(target_url, xml_request):
    ''' sends xml request to url with parameter request '''
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    data = xml_request#urllib.urlencode({'xml': xml_request})
    req = urllib2.Request(target_url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    dom = parseString(the_page)
    return dom


  # result = urllib.urlopen( target_url, urllib.urlencode( {'request':xml_request} ) )
  # #parse results and print the xml or do whatever with it
  # res = result
  # dom = parse( result )
  # result.close()
  # return dom
    
def get_xml(type, id):

    if type == 'get_status':
        xml =  ('<?xml version="1.0" encoding="utf-8"?>'
    '<request>'
    '<protocol-version>4.00</protocol-version>'
    '<request-type>33</request-type>'
    '<terminal-id>{0}</terminal-id>'
    '<extra name="password">{1}</extra>'
    '<bills-list>'
    '<bill txn-id="{2}"/>'
    '</bills-list>'
    '</request>').format(q_id, q_pass, id) 

    elif type == 'cancel':
        xml = ('<?xml version="1.0" encoding="utf-8"?>'
    '<request>'
    '<protocol-version>4.00</protocol-version>'
    '<request-type>29</request-type>'
    '<terminal-id>{0}</terminal-id>'
    '<extra name="password">{1}</extra>'
    '<extra name="txn-id">{2}</extra>'
    '<extra name="status">reject</extra>'
    '</request>').format(q_id, q_pass, id) 

    l = len(xml)
    n = 8 - l % 8
    xml += ' '*n 
    return xml      

def get_key():
    
    first = hashlib.md5(q_pass).hexdigest()
    second = hashlib.md5(q_id + first).hexdigest()
    third = first+'0000000000000000'
    fourth = '0000000000000000'+second
    fifth = hex(long(third, 16) ^ long(fourth, 16))
    sixth = str(fifth)[2:-1]
    result = str(bytearray.fromhex(sixth))    
    return result
    
    
def encrypt(data):

    key = get_key()
    k = triple_des(key, ECB, padmode=PAD_NORMAL)
    d = k.encrypt(data)
    hex = ''.join( [ "%02X" % ord( x ) for x in d ] ).strip()
    b64 = base64.encodestring(hex.decode('hex'))
    return b64

def generate_request(type, id):
    
    data = get_xml(type,id)
    return 'qiwi0000'+q_id+'\n'+encrypt(data)



def generate_status(resp, order, item):
    link = ''
    status_dictionary = {'1':u'счет не выставлен', '50':u'выставлен, не оплачен', '52':'проводится', '60':'оплачен', '150':'отменен', '151':'отменен', '160':'отменен', '161':'отменен, истекло время'}
    generated_link =  u'<a href="http://w.qiwi.ru/setInetBill_utf.do?from=240077&to={0}&summ={1}&com={2} {3}&lifetime=48&check_agt=false&txn_id={4}">(перейти к оплате)</a>'.format(str(order.phone), str(item.price),item.name, order.photo_id, str(order.order_id)) 
    if resp.getElementsByTagName('bill'):
        code = resp.getElementsByTagName('bill')[0].attributes['status'].value
        if code == '50':
            link = generated_link
    else:
        #code_debug = resp.getElementsByTagName('result-code')[0].nodeValue 
        code = '1'
        link = generated_link

    return status_dictionary[code]+' '+link   

def check_active(resp, edit):

    if resp.getElementsByTagName('bill'):
        code = resp.getElementsByTagName('bill')[0].attributes['status'].value
        if code != '150':
            return True
    else:
        if edit:
            return True
        else:        
            return False        

  
class NewOrderView(TemplateView):

    def get_item(self):
        id = self.request.GET.get('order')
        return id

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(NewOrderView, self).get_context_data(**kwargs)

        id = self.kwargs.get('id', None)

        if self.get_item():
            id = self.get_item()

        action = self.kwargs.get('action', None)

        if action:
            send_xml("http://ishop.qiwi.ru/xml", generate_request('cancel', id)) 
        
        order = Order.objects.get(order_id=id)
        item = Item.objects.get(name=order.merchandise_id)

        resp = send_xml("http://ishop.qiwi.ru/xml", generate_request('get_status', id))
        context['cancel_button'] = check_active(resp, False)
        context['edit_button'] = check_active(resp, True)
        context['status'] =  generate_status(resp, order, item)
        context['item'] = item
        context['photo'] = Photo.objects.get(title_slug=order.photo_id)
        context['all_photos'] = Photo.objects.filter(is_public=True)
        context['id'] = id
        context['order'] = order   
  
        return context        


class UpdateOrderView(UpdateView):

    form_class = EditOrderForm
    model = Order
    fields = ['name']
    slug_field = 'order_id'
    slug_url_kwarg = 'id'  

    def get_success_url(self):

        return 'http://www.victorkachalin.ru/shop/orders/'+ self.kwargs.get('id', None)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('id', None)
        order = Order.objects.get(order_id=id)
        context = super(UpdateOrderView, self).get_context_data(**kwargs)
        context['item'] = Item.objects.get(id=order.merchandise_id)
        context['photo'] = Photo.objects.get(title_slug=order.photo_id)
        context['all_photos'] = Photo.objects.filter(is_public=True)
        context['id'] = id
        context['edit'] = True

        return context
