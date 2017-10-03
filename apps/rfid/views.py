from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import Context
from django.views import generic
from django.views.defaults import server_error
from django.contrib import messages


from apps.registration.models import Hybrid
from apps.rfid.models import Appearances


class AppearancesView(generic.DetailView):
    model = Appearances
    template_name = 'rfid/index.html'

@login_required
def rfid(request, pk):

    return render(request, 'rfid/index.html', context=Context({'pk': pk}))


@login_required
def add_appearance(request, pk):
    if 'rfid_key' not in request.POST:
        return server_error(request)
    input = request.POST.get('rfid_key')
    input = input.lower()
    if input.isdigit():
        rfid_key = int(request.POST['rfid_key'], 10)
        card_key = translate_rfid_key_to_printed_key(rfid_key)
        if Hybrid.objects.filter(card_key=card_key).exists():
            user = Hybrid.objects.get(card_key=card_key)
            appearances = Appearances.objects.get(pk=pk)
            if user in appearances.users.all():
                messages.warning(request, user.get_full_name()+' er allerede lagt til!')
                return redirect('rfid:rfid', pk)
            else:
                appearances.add_appearance(user)
                appearances.save()
                messages.success(request, user.get_full_name()+' lagt til')
                return redirect('rfid:rfid', pk)
        else:
            messages.error(request, 'Ugylig RFID')
            return redirect('rfid:rfid', pk)
    else:
        if Hybrid.objects.filter(username=input).exists():
            user = Hybrid.objects.get(username=input)
            appearances = Appearances.objects.get(pk=pk)
            if user in appearances.users.all():
                messages.warning(request, user.get_full_name()+' er allerede lagt til!')
                return redirect('rfid:rfid', pk)
            else:
                appearances.add_appearance(user)
                appearances.save()
                messages.success(request, user.get_full_name()+' lagt til')
                return redirect('rfid:rfid', pk)
        else:
            messages.error(request, 'Ugylig brukernavn')
            return redirect('rfid:rfid', pk)


def translate_rfid_key_to_printed_key(key_int, bits=32):
    key_bin = bin(key_int).split('b')[1][:bits]
    while len(key_bin) < bits:
        key_bin = '0' + key_bin

    print(key_bin)

    if key_int < 0:
        key_bin_flipped = '0'
        for i in range(1, len(key_bin)):
            key_bin_flipped += '0' if key_bin[i] == '1' else '1'
            rfid_int_flipped = int(key_bin_flipped, 2)
            key_bin = '1' + bin(rfid_int_flipped + 1).split('b')[1][1:]

    key_bin_fixed = '0b'
    for i in range(bits // 8):
        for j in range(8):
            key_bin_fixed += key_bin[8 * i + 7 - j]
    return int(key_bin_fixed, 2)
