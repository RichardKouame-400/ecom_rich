from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Product, Order


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription avec choix du type d'utilisateur"""
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=20, required=False, label="Téléphone")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Adresse")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'phone', 'address', 'first_name', 'last_name']
        labels = {
            'username': "Nom d'utilisateur",
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'user_type': 'Type de compte'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limite les choix aux visiteurs et vendeurs (pas admin)
        self.fields['user_type'].choices = [
            ('visitor', 'Visiteur'),
            ('seller', 'Vendeur'),
        ]
        # Style Bootstrap pour tous les champs
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserLoginForm(AuthenticationForm):
    """Formulaire de connexion stylisé"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })


class ProductForm(forms.ModelForm):
    """Formulaire pour créer/modifier un produit"""
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category', 'tags', 'is_active']
        labels = {
            'name': 'Nom du produit',
            'description': 'Description',
            'price': 'Prix (CFA)',
            'stock': 'Stock disponible',
            'image': 'Image du produit',
            'category': 'Catégorie',
            'tags': 'Étiquettes',
            'is_active': 'Produit actif'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class OrderForm(forms.ModelForm):
    """Formulaire pour passer une commande"""
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'notes']
        labels = {
            'shipping_address': 'Adresse de livraison',
            'phone': 'Téléphone',
            'notes': 'Notes complémentaires'
        }
        widgets = {
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


