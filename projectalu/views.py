from django.shortcuts import render,HttpResponse
import math
from django.http import JsonResponse
import itertools

def awal(request):
    return HttpResponse('Berhasil diinstall')

def estimate_time_to_crack(password):
    # Asumsikan karakter yang digunakan dalam password adalah huruf dan angka
    possible_characters = 36  # (26 huruf + 10 angka)

    password_length = len(password)
    combinations = math.pow(possible_characters, password_length)

    # Anggap komputer dapat memproses sekitar 10 juta percobaan per detik
    attempts_per_second = 10000000

    # Estimasi waktu dalam detik
    time_to_crack = combinations / attempts_per_second

    # Ubah ke bentuk yang lebih mudah dibaca (hari, jam, menit, detik)
    seconds = time_to_crack % 60
    minutes = (time_to_crack // 60) % 60
    hours = (time_to_crack // 3600) % 24
    days = time_to_crack // (3600 * 24)

    return f"{int(days)} hari, {int(hours)} jam, {int(minutes)} menit, {int(seconds)} detik"


def evaluate_password_strength(password):
    if len(password) < 8:
        return 'Weak'
    elif len(password) < 12:
        return 'Moderate'
    else:
        return 'Strong'


def password(request):
    if request.method == 'POST':
        user_password = request.POST.get('password')

        # Evaluasi kekuatan password
        password_strength = evaluate_password_strength(user_password)

        # Estimasi waktu untuk meretas password
        time_to_crack = estimate_time_to_crack(user_password)

        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  
        password_length = len(user_password)  

        attempts = []  # Inisialisasi daftar untuk menyimpan semua percobaan
        found_at_attempt = None  # Untuk menyimpan nomor percobaan di mana password ditemukan

        found = False
        attempt_count = 0  # Inisialisasi variabel untuk nomor percobaan
        for attempt in itertools.product(characters, repeat=password_length):
            attempt_count += 1  # Increment nomor percobaan
            attempt_password = ''.join(attempt)
            attempts.append(attempt_password)  # Menyimpan percobaan saat ini
            if attempt_password == user_password:
                found = True
                found_at_attempt = attempt_count  # Menyimpan nomor percobaan di mana password ditemukan
                break

        if found:
            progress = f"Password ditemukan pada percobaan ke-{found_at_attempt}"
        else:
            progress = "Password tidak ditemukan"

        context = {
            'strength': password_strength,
            'password': user_password,
            'time_to_crack': time_to_crack,  
            'progress': progress,  
            'attempts': attempts, 
            'found_at_attempt': found_at_attempt  
        }
        return render(request, 'password.html', context) 

    return render(request, 'password.html')
