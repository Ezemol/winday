import requests
from django.contrib.auth.decorators import login_required  # Decorador para requerir inicio de sesión
from django.views.decorators.csrf import csrf_exempt  # Decorador para permitir solicitudes POST sin CSRF
from django.contrib.auth import authenticate, login, logout  # Funciones para autenticar y manejar sesiones de usuario
from django.db import IntegrityError  # Manejo de errores de integridad en la base de datos
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404  # Respuestas HTTP
from django.shortcuts import render, redirect, get_object_or_404  # Funciones para renderizar vistas y obtener objetos
from django.urls import reverse  # Función para generar URLs
import json  # Módulo para manejar JSON
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # Crear páginas en el front
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .models import User, Profile, Place, Favorite

""" Main page """
def index(request):
    return render(request, "winday/index.html")

def login_view(request):
    if request.method == "POST":
        # Intentar iniciar sesión
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Verificar si la autenticación fue exitosa
        if user is not None:
            login(request, user)  # Aquí se pasa el usuario autenticado correctamente
            return HttpResponseRedirect(reverse('winday:index'))  # Redirigir al índice
        else:
            return render(request, "winday/login.html", {
                "message": "Nombre de usuario y/o contraseña inválidas."  # Mensaje de error
            })
    else:
        return render(request, "winday/login.html")  # Renderizar la vista de inicio de sesión


@login_required
def logout_view(request):
    logout(request)  # Cerrar sesión
    return render(request, "winday/index.html")  # Redirigir al índice


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Asegurarse de que la contraseña coincide con la confirmación
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "winday/register.html", {
                "message": "Las contraseñas deben coincidir."  # Mensaje de error
            })

        if not username or not email or not password or not confirmation:
            return render(request, "winday/register.html", {
                "message": "Debes completar todos los campos"
            })
        
        if len(password) < 8:
            return render(request, "winday/register.html", {
                "message": "La contraseña debe tener al menos 8 caracteres."
            })
        
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, "winday/register.html", {
                "message": e.messages  # Mostrará las razones del error de validación
            })

        # Intentar crear un nuevo usuario
        try:
            user = User.objects.create_user(username, email, password)
            user.save()  # Guardar el usuario en la base de datos
        except IntegrityError:
            return render(request, "winday/register.html", {
                "message": "Nombre de usuario ya tomado."  # Mensaje de error
            })
        login(request, user)  # Iniciar sesión con el nuevo usuario
        return HttpResponseRedirect(reverse('winday:index'))  # Redirigir al índice
    else:
        return render(request, "winday/register.html")  # Renderizar la vista de registro
    

def profile(request, username):
    # Intentar obtener el usuario en la base de datos
    try:
        user = get_object_or_404(User, username=username)
    # If user was not found mensaje de error.
    except Http404:
        return render(request, "winday/profile.html", {
            "message": "El usuario no fue encontrado"
        })
    
    # Buscar el perfil del usuario
    profile, created = Profile.objects.get_or_create(user=user)

    # Inicializar variables
    is_following = False
    is_profile = False
    num_followers = profile.followers.count()  # Contar seguidores
    num_following = user.following.count()  # Contar seguidos

    # Si es el perfil del usuario, no mostrar la opción de seguir
    if request.user == user:
        is_profile = True 

    # Verificar si el usuario está siguiendo al dueño del perfil
    if request.user.is_authenticated and not is_profile:
        is_following = request.user in profile.followers.all()
        
    return render(request, "winday/profile.html", {
            "profile_user": user,
            "profile": profile,
            "is_following": is_following,
            "num_followers": num_followers,
            "num_following": num_following,
            "is_profile": is_profile,
        })

# Página de los perfiles que sigue el user
def profile_connections(request, profile_id):

     # Obtener el usuario cuyo perfil se está consultando
    user = get_object_or_404(User, pk=profile_id)

    # Determinar si se va a mostrar la lista de seguidores o seguidos
    view_type = request.GET.get('view', 'followers')  # Valor por defecto: 'followers'

    if view_type == 'following': 
        profiles = user.following.all()
        title = 'Seguidos'
    else:
        profiles = user.profile.followers.all()
        title = 'Seguidores'

    return render(request, 'winday/profile_connections.html', {
        "username": user,
        "profiles": profiles,
        "title": title,
        "view_type": view_type,
    })

@csrf_exempt
@login_required
def follow_user(request, profile_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                user_to_follow = get_object_or_404(User, pk=profile_id) # Obtiene el usuario a seguir

                profile = user_to_follow.profile # Obtiene el perfil del usuario

                # If el usuario ya está siguiendo dejar de seguir. Else empezar a seguir
                if request.user in profile.followers.all():
                    profile.followers.remove(request.user)  # Dejar de seguir
                    is_following = False
                else:
                    profile.followers.add(request.user) # Seguir
                    is_following = True

                return JsonResponse({
                    "message": "success",
                    "is_following": is_following, # Devuelve el estado de seguimiento
                })
            except User.DoesNotExist:
                return JsonResponse({"error":"Usuario no encontrado."}, status=404)  # Manejar usuario no encontrado
        else:
            return JsonResponse({"error":  "El usuario no está autenticado."}, status=403)  # Manejar usuario no autenticado
    return JsonResponse({"error": "Post request requerida."}, status=400) # Manejar método incorrecto

# Vista para manejar la consulta del viento y verificar favoritos
def find_wind(request):
    location = request.GET.get('location')  # Obtener la ubicación desde el formulario
    
    if location:
        cache_key = f'wind_data_{location}'
        cached_data = cache.get(cache_key)
    
        if cached_data:
            context = cached_data
        else:
            # Lógica para hacer la solicitud a la API
            api_key = 'fbe62aefbaa8f42f0dd5f00177975542'
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {'q': location, 'appid': api_key, 'units': 'metric'}
            
            try:
                response = requests.get(base_url, params=params)
                data = response.json()
                if response.status_code == 200:
                    wind_speed = data['wind']['speed']
                    wind_direction = data['wind']['deg']
                    is_fav = is_favorite(request, location)  # Devuelve True o False
                    
                    context = {
                        'location': location, 
                        'wind_speed': wind_speed, 
                        'wind_direction': wind_direction,
                        'is_fav': is_fav,  # Me dice si está o no en favoritos
                    }
                    # Almacenar en caché por 10 minutos
                    cache.set(cache_key, context, timeout=600)
                else:
                    context = {'error': 'No se pudo obtener la información del viento.'}
            except Exception as e:
                context = {'error': f'Ocurrió un error: {e}'}
    else:
        context = {'error': 'Por favor, ingrese una ubicación válida.'}

    return render(request, 'winday/wind_data.html', context)


# Vista para manejar los favoritos de cada usuario
def favorite(request, location):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                user = request.user
                place, created = Place.objects.get_or_create(name=location)
                favorite, is_fav = Favorite.objects.get_or_create(user=user, place=place)
                
                is_fav = is_favorite(request, location) # Llama a la función que determina si es fav o no

                if not is_fav:
                    favorite.add_location(place)
                    is_fav = True
                    favorite.save()
                    return JsonResponse({
                        "success" : "Lugar agregado a favoritos.",
                        "is_fav" : is_fav
                    })
                else:
                    favorite.remove_location(place)
                    is_fav = False
                    favorite.save()
                    return JsonResponse({
                        "success" : "Lugar quitado de favoritos.",
                        "is_fav" : is_fav
                    })

            except User.DoesNotExist:
                return JsonResponse({"error":"Usuario no encontrado."}, status=404)  # Manejar usuario no encontrado
        else:
            return JsonResponse({"error":"El usuario no está autenticado."}, status=403)
    else:
        return JsonResponse({"error":"Solicitud post requerida."}, status=400)


# Vista para decir si un usuario tiene o no un lugar en favoritos
def is_favorite(request, location):
    user = request.user
    if user.is_authenticated:
        # Intenta obtener el lugar; si no existe, se crea un objeto vacío
        place = Place.objects.filter(name=location).first()
        if place:
            # Devuelve True si existe un favorito para el usuario y el lugar específico
            return Favorite.objects.filter(user=user, place=place).exists()
    return False  # Devuelve False si el usuario no está autenticado o el lugar no existe