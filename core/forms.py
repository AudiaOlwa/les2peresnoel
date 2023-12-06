from django import forms

USER_TYPE_CHOICES = [
   ('P', 'Particulier'),
   ('R', 'Professionnel'),
]

SECTOR_CHOICES = [
   ('A', 'Investisseur'),
   ('B', 'Fournisseur'),
   ('C', 'Vendeur'),
   # Ajoutez ici les autres secteurs
]

SECTOR_DETAIL_CHOICES = [
   ('ACCESSOIRES', 'Accessoires'),
   ('ALIMENTATION_BOISSON', 'Alimentation/Boisson'),
   ('MODE', 'Industrie de la mode'),
   ('TEXTILE', 'Industrie du textile'),
   ('DECORATION', 'Décoration'),
   ('EDITION', 'Édition'),
   ('EMBALLAGE', 'Emballage'),
   ('ECLAIRAGE', 'Éclairage'),
   ('EDITION', 'Edition'),
   ('EMBALLAGE', 'Emballage'),
   ('ECLAIRAGE', 'Éclairage'),
   ('POSTAL_OPERATOR', 'Opérateur services postaux (création bureau de poste PNS – timbres – enveloppe – etc.)'),
   ('AMUSEMENT_PARK', 'Parc d’attractions (Construction village PNS)'),
   ('CINEMATOGRAPHY_PRODUCTION', 'Production cinématographique'),
   ('VIDEO_GAMES_PRODUCTION', 'Production jeux vidéos'),
   ('ADVERTISING', 'Publicité'),
   ('TV', 'TV'),
   ('OTHER', 'Autre'),
   # Ajoutez ici les autres détails de secteur
]



class SignUpForm(forms.Form):

 # Ajoutez ici les autres champs de formulaire
 utilisateur = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
 secteur = forms.ChoiceField(choices=SECTOR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
 detail_secteur = forms.ChoiceField(choices=SECTOR_DETAIL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
 nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
 email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))










