from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.db.models import Q
from .forms import UserForm,SongForm,AlbumForm,LoginForm
from .models import song_album,song
from django.http import JsonResponse

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

class DetailView(generic.DetailView):
    model = song_album
    template_name = 'Login/details.html'

class AlbumCreate(CreateView):
    model = song_album
    fields = ['artist','albub_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model = song_album
    fields = ['artist','albub_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model = song_album
    success_url = reverse_lazy('Login:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'Login/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('Login:index')

        return render(request,self.template_name,{'form':form})


class UserLogin(View):
    form_class = LoginForm
    template_name = 'Login/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = song_album.objects.filter(user=request.user)
                return render(request, 'Login/index.html', {'albums': albums})
            else:
                return render(request, 'Login/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Login/login.html', {'error_message': 'Invalid login'})

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'Login/login.html')
    else:
        albums = song_album.objects.filter(user=request.user)
        song_results = song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(albub_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'Login/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'Login/index.html', {'albums': albums})




def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'Login/login.html', {'form':form})

def create_song(request, pk):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(song_album, pk=pk)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'Login/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'Login/create_song.html', context)

        song.save()
        return render(request, 'Login/details.html', {'object': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'Login/create_song.html', context)

def favorite(request, song_id):
    Song = get_object_or_404(song, pk=song_id)
    try:
        if Song.is_favorite:
            Song.is_favorite = False
        else:
            Song.is_favorite = True
        Song.save()
    except (KeyError, song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def favorite_album(request, pk):
    album = get_object_or_404(song_album, pk=pk)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, song_album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def delete_song(request, pk, song_id):
    album = get_object_or_404(song_album, pk=pk)
    Song = song.objects.get(pk=song_id)
    Song.delete()
    return render(request, 'Login/details.html', {'object': album})

def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'Login/login.html')
    else:
        try:
            Song_ids = []
            for album in song_album.objects.filter(user=request.user):
                for s in album.song_set.all():
                    Song_ids.append(s.pk)
            users_songs = song.objects.filter(pk__in=Song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except song_album.DoesNotExist:
            users_songs = []
        return render(request, 'Login/allsongs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })