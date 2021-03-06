from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.template import Context
from django.views import generic
from django.views.defaults import server_error
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin


from apps.registration.models import Hybrid
from apps.events.models import Participation
from apps.rfid.models import Appearances, GeneralAssembly


class AppearancesView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'rfid.change_appearances'
    model = Appearances
    template_name = 'rfid/index.html'


class GeneralAssemblyView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'rfid.change_generalassembly'
    model = GeneralAssembly
    template_name = 'rfid/generalassembly.html'


@permission_required(['rfid.change_appearances'])
def add_appearance(request, pk):
    if 'rfid_key' not in request.POST:
        return server_error(request)
    id_input = request.POST.get('rfid_key')
    id_input = id_input.lower()
    if id_input.isdigit():
        rfid_key = int(request.POST['rfid_key'], 10)
        card_key = translate_rfid_key_to_printed_key(rfid_key)
        if Hybrid.objects.filter(card_key=card_key).exists():
            user = Hybrid.objects.get(card_key=card_key)
            appearances = Appearances.objects.get(pk=pk)
            if get_registered(user, appearances.event):
                if user in appearances.users.all():
                    messages.warning(request, user.get_full_name()+' er allerede lagt til!')
                    return redirect('rfid:rfid', pk)
                else:
                    appearances.add_appearance(user)
                    appearances.save()
                    messages.success(request, user.get_full_name()+' lagt til')
                    return redirect('rfid:rfid', pk)
            else:
                if  get_waiting(user, appearances.event):
                    messages.error(request, user.get_full_name() + ' er på ventelisten!')
                    return redirect('rfid:rfid', pk)
                else:
                    messages.error(request, user.get_full_name() + ' er ikke påmeldt!')
                    return redirect('rfid:rfid', pk)
        else:
            messages.error(request, 'Ugylig RFID')
            return redirect('rfid:rfid', pk)
    else:
        if Hybrid.objects.filter(username=id_input).exists():
            user = Hybrid.objects.get(username=id_input)
            appearances = Appearances.objects.get(pk=pk)
            if get_registered(user, appearances.event):
                if user in appearances.users.all():
                    messages.warning(request, user.get_full_name()+' er allerede lagt til!')
                    return redirect('rfid:rfid', pk)
                else:
                    appearances.add_appearance(user)
                    appearances.save()
                    messages.success(request, user.get_full_name()+' lagt til')
                    return redirect('rfid:rfid', pk)
            else:
                if get_waiting(user, appearances.event):
                    messages.error(request, user.get_full_name() + ' er på ventelisten!')
                    return redirect('rfid:rfid', pk)
                else:
                    messages.error(request, user.get_full_name() + ' er ikke påmeldt!')
                    return redirect('rfid:rfid', pk)
        else:
            messages.error(request, 'Ugylig brukernavn')
            return redirect('rfid:rfid', pk)


def get_registered(user, event):
    this_event = Participation.objects.filter(attendance__event=event) # Gets the participants from correct event
    registered_users = this_event.values_list('hybrid', flat=True) # Gets a list of all the users on the event
    if user.pk in registered_users: # If user is in list
        signed = False
        for attendance in event.attendance_set.all(): # For each attendance, check if the user is signed (not waiting)
            if attendance.is_signed(user):
                signed = True
        return signed
    else:
        return False


def get_waiting(user, event):
    this_event = Participation.objects.filter(attendance__event=event)  # Gets the participants from correct event
    registered_users = this_event.values_list('hybrid', flat=True)  # Gets a list of all the users on the event
    if user.pk in registered_users:  # If user is in list
        waiting = False
        for attendance in event.attendance_set.all():  # For each attendance, check if the user is on wait list.
            if attendance.is_waiting(user):
                waiting = True
        return waiting
    else:
        return False



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


def add_appearance_gen(request, pk):
    if 'rfid_key' not in request.POST:
        return server_error(request)
    id_input = request.POST.get('rfid_key')
    id_input = id_input.lower()
    if id_input.isdigit():
        rfid_key = int(request.POST['rfid_key'], 10)
        card_key = translate_rfid_key_to_printed_key(rfid_key)
        if Hybrid.objects.filter(card_key=card_key).exists():
            user = Hybrid.objects.get(card_key=card_key)
            genfors = GeneralAssembly.objects.get(pk=pk)
            if user in genfors.users.all():
                genfors.remove_genfors_appearance(user)
                genfors.save()
                messages.warning(request, user.get_full_name() + ' ute av generalforsamling')
                return redirect('rfid:genfors', pk)
            else:
                print("jeg kommer helt hit!")
                genfors.add_genfors_appearance(user)
                genfors.save()
                messages.success(request, user.get_full_name() + ' inne på generalforsamling')
                return redirect('rfid:genfors', pk)
        else:
            messages.error(request, 'Ugylig RFID')
            return redirect('rfid:genfors', pk)
    else:
        if Hybrid.objects.filter(username=id_input).exists():
            user = Hybrid.objects.get(username=id_input)
            genfors = GeneralAssembly.objects.get(pk=pk)
            if user in genfors.users.all():
                genfors.remove_genfors_appearance(user)
                genfors.save()
                messages.warning(request, user.get_full_name()+' ute av generalforsamling')
                return redirect('rfid:genfors', pk)
            else:
                print("jeg kommer helt hit!")
                genfors.add_genfors_appearance(user)
                genfors.save()
                messages.success(request, user.get_full_name()+' inne på generalforsamling')
                return redirect('rfid:genfors', pk)
        else:
            messages.error(request, 'Ugylig brukernavn')
            return redirect('rfid:genfors', pk)