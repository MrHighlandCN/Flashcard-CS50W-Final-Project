from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *



# Create your views here.
def index(request):
    if request.user.is_authenticated:
        folders = Folder.objects.filter(owner=request.user)
        sets = Set.objects.filter(owner=request.user)

        return render(request, 'flashcard/index.html', {
            "folders": folders,
            "sets": sets
        })
    else:
        return HttpResponseRedirect(reverse('login'))
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flashcard/login.html", {
                "message": "Invalid username and/or password.",
                "status": "failed"
            })
    else:
        return render(request, "flashcard/login.html")
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["password-confirmation"]
        if password != confirmation:
            return render(request, "flashcard/register.html", {
                "message": "Passwords must match.",
                "status": "failed"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "flashcard/register.html", {
                "message": "Username already taken.",
                "status": "failed"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flashcard/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def create_folder(request):
    
    if request.method == "POST":
        title = request.POST["title"]

        try:
            folder = Folder(title=title, owner=request.user)
            folder.save()
        except IntegrityError as e:
            print(e)
            return render(request, "flashcard/index.html", {
                "message": "Folder already exists.",
                "status": "failed"
            })
        folders = Folder.objects.filter(owner=request.user)
        sets = Set.objects.filter(owner=request.user)
        return render(request, "flashcard/index.html", {
                    "message": "Create folder successfully",
                    "status": "succeeded",
                    "folders": folders,
                    "sets": sets
                    })
    else:
        pass

def create_set(request):
    if request.method == "POST":
        # GET SET INPUT
        set_title = request.POST.get('set-title').strip()
        set_description = request.POST.get('set-description').strip()
        # VALIDATE SET DATA 
        if not set_title: 
            error_message = "Title cannot be empty."
            return render(request, "flashcard/create_set.html", {
                "error": error_message
            })
        #CREATE SET 
        new_set = Set(title=set_title, description=set_description, owner=request.user)
        new_set.save()


        # GET CARDS INPUT
        card_contents = request.POST.getlist('content[]')
        card_meanings = request.POST.getlist('meaning[]')
        card_imgs = request.FILES.getlist('card-image[]')
        print(f"Content: {len(card_contents)}")
        print(f"Meaning: {len(card_meanings)}")
        print(f"Image: {len(card_imgs)}")
        for content, meaning in zip(card_contents, card_meanings):
            image = None
            if card_imgs:
                image = card_imgs.pop(0)
            
            if content.strip() and meaning.strip():
                card = Card(content=content, meaning=meaning, image=image, owner=request.user, set=new_set)
                card.save()
            else:
                print("Content or meaning is empty, skipping this card.")
        
        return HttpResponseRedirect(reverse('index'))
    else: 
        return render(request, "flashcard/create_set.html")

def folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    sets = Set.objects.filter(owner=request.user, folder=None)

    return render(request, "flashcard/folder.html", {
        "folder": folder,
        "sets": sets
    })
    
def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        folders = []
        sets = []
        if query: 
            folders = Folder.objects.filter(title__icontains=query, owner=request.user)
            sets = Set.objects.filter(title__icontains=query, owner=request.user)       
            return render(request, 'flashcard/index.html', {
                'query': query,
                'folders': folders,
                'sets': sets
            })
        else:
            return HttpResponseRedirect(reverse('index'))
        
def add_set_to_folder(request):
    if request.method == "POST":
        set_ids = request.POST.getlist('add-set[]')
        folder_id = request.POST.get('folder_id')
        folder = get_object_or_404(Folder, id=folder_id)
        if set_ids:
            for id in set_ids:
                set = get_object_or_404(Set, id=id)
                print(f"Set ID: {id}, Current Folder: {set.folder}")
                set.folder = folder
                set.save()
                print(f"Updated Folder: {set.folder}")
                
        return HttpResponseRedirect(reverse('folder', args=[folder_id]))
    
@login_required
@csrf_exempt
def remove_set_from_folder(request, set_id):
    if request.method == "POST":
        try: 
            set = Set.objects.get(id=set_id)
            set.folder = None
            set.save()
            return JsonResponse({"message": "Set removed from folder successfully"}, status=200)
        except Set.DoesNotExist:
            return JsonResponse({"error": "Set not found"}, status=404)   

def delete_folder(request, folder_id):
    if request.method == "POST":
        folder = get_object_or_404(Folder, id=folder_id)
        folder.delete()
        return HttpResponseRedirect(reverse('index'))

def delete_set(request, set_id):
    if request.method == "POST":
        set = get_object_or_404(Set, id=set_id)
        set.delete()
        return HttpResponseRedirect(reverse('index'))


def set(request, set_id):
    set = get_object_or_404(Set, id=set_id)
    cards = set.cards.all
    return render(request, "flashcard/set.html",{
        "set": set,
        "cards": cards
    })

def get_cards(request, set_id):
    set = get_object_or_404(Set, id=set_id)
    cards = Card.objects.filter(set=set)
    return JsonResponse([card.serialize() for card in cards], safe=False)


def about(request):
    return render(request, "flashcard/about.html")