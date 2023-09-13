from django.http import HttpResponse
from django.shortcuts import render
from listings.models import Band
from listings.models import Listing
from django.shortcuts import get_object_or_404
from listings.forms import ContactUsForm, BandForm, ListingForm
from django.core.mail import send_mail
from django.shortcuts import redirect



def band_list(request):
    bands = Band.objects.all()
    return render(request,'listings/band_list.html',{'bands': bands})

def band_detail(request, id):
  get_object_or_404(Band, pk=id)
  band = Band.objects.get(pk=id)  # nous insérons cette ligne pour obtenir le Band avec cet id
  return render(request, 'listings/band_detail.html', {'band': band}) # nous mettons à jour cette ligne pour passer le groupe au gabarit

def listing_list(request):
    listings = Listing.objects.all()
    return render(request,'listings/listing_list.html',{'listings': listings})

def listing_list_band(request, id):
    get_object_or_404(Band, pk=id)
    band = Band.objects.get(pk=id)
    return render(request,'listings/listing_list_band.html',{'band': band})

def listing_detail(request, id):
    get_object_or_404(Listing, pk=id)
    listing = Listing.objects.get(pk=id)
    return render(request,'listings/listing_detail.html',{'listing': listing})

def about(request):
    return render(request,'listings/about.html')

def contact(request):

  # ajoutez ces instructions d'impression afin que nous puissions jeter un coup d'oeil à « request.method » et à « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['antoine.letellier90@gmail.com'],
            )
            return redirect('email-sent')
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
    # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request,
            'listings/contact.html',
            {'form': form})

def email_sent(request):
    return render(request,'listings/email_sent.html')

def about(request):
    return render(request,'listings/about.html')

def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            listing = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('listing-detail', listing.id)

    else:
        form = ListingForm()

    return render(request,
            'listings/listing_create.html',
            {'form': form})

def listing_CC(request, id=None):

    if id:
        listing = Listing.objects.get(id=id)

    if request.method == 'POST':
        if id:
            form = ListingForm(request.POST, instance=listing)
        else:
            form = ListingForm(request.POST)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            listing = form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('listing-detail', listing.id)
    else:
        if id:
            form = ListingForm(instance=listing)
        else:
            form = ListingForm()

    return render(request,
                'listings/band_CC.html',
                {'form': form,
                 'id': id,
                 'listing': listing if id else None})


def band_CC(request, id=None):

    if id:
        band = Band.objects.get(id=id)

    if request.method == 'POST':
        if id:
            form = BandForm(request.POST, instance=band)
        else:
            form = BandForm(request.POST)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            band = form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('band-detail', band.id)
    else:
        if id:
            form = BandForm(instance=band)
        else:
            form = BandForm()

    return render(request,
                'listings/band_CC.html',
                {'form': form,
                 'id': id,
                 'band': band if id else None})


def band_delete(request, id):
    band = Band.objects.get(id=id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        band.delete()
        # rediriger vers la liste des groupes
        return redirect('band-list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(request,
                    'listings/band_delete.html',
                    {'band': band})

def listing_delete(request, id):
    listing = Listing.objects.get(id=id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        listing.delete()
        # rediriger vers la liste des groupes
        return redirect('listing-list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(request,
                    'listings/listing_delete.html',
                    {'listing': listing})