from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Tag, Product, Cart, CartItem, Order, OrderItem


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administration des utilisateurs"""
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_type', 'phone', 'address')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_type', 'phone', 'address', 'email')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration des catégories"""
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Administration des étiquettes"""
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


class ProductImageInline(admin.TabularInline):
    """Inline pour les images de produits (peut être étendu plus tard)"""
    model = Product
    extra = 0
    max_num = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administration des produits"""
    list_display = ['name', 'price', 'stock', 'category', 'seller', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at', 'seller']
    search_fields = ['name', 'description', 'seller__username']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'description', 'price', 'stock', 'image')
        }),
        ('Catégorisation', {
            'fields': ('category', 'tags')
        }),
        ('Vendeur et statut', {
            'fields': ('seller', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filtre les produits pour les vendeurs"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'user_type') and request.user.user_type == 'seller':
            return qs.filter(seller=request.user)
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        """Assigne automatiquement le vendeur si c'est un nouveau produit"""
        if not change and not obj.seller_id:
            obj.seller = request.user
        super().save_model(request, obj, form, change)


class CartItemInline(admin.TabularInline):
    """Inline pour les articles du panier"""
    model = CartItem
    extra = 0
    readonly_fields = ['get_subtotal']
    
    def get_subtotal(self, obj):
        return f"{obj.get_subtotal()} CFA"
    get_subtotal.short_description = "Sous-total"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Administration des paniers"""
    list_display = ['user', 'get_item_count', 'get_total', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = "Nombre d'articles"
    
    def get_total(self, obj):
        return f"{obj.get_total()} CFA"
    get_total.short_description = "Total"


class OrderItemInline(admin.TabularInline):
    """Inline pour les articles de commande"""
    model = OrderItem
    extra = 0
    readonly_fields = ['get_subtotal']
    
    def get_subtotal(self, obj):
        return f"{obj.get_subtotal()} CFA"
    get_subtotal.short_description = "Sous-total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Administration des commandes"""
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations client', {
            'fields': ('user', 'shipping_address', 'phone')
        }),
        ('Commande', {
            'fields': ('status', 'total_amount', 'notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
