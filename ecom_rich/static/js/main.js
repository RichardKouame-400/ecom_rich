// ================================================
// E-COMMERCE - INTERACTIONS JAVASCRIPT
// ================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== ANIMATIONS AU SCROLL =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observer tous les éléments avec animation retardée
    document.querySelectorAll('.card, .stat-card, .jumbotron').forEach(el => {
        if (!el.classList.contains('fade-in')) {
            observer.observe(el);
        }
    });

    // ===== EFFET DE TYPING DANS LE HERO =====
    const heroTitle = document.querySelector('.jumbotron h1');
    if (heroTitle && !sessionStorage.getItem('animationPlayed')) {
        const originalText = heroTitle.textContent;
        heroTitle.textContent = '';
        let i = 0;
        
        const typeWriter = () => {
            if (i < originalText.length) {
                heroTitle.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        };
        
        setTimeout(typeWriter, 300);
        sessionStorage.setItem('animationPlayed', 'true');
    }

    // ===== SMOOTH SCROLL POUR LES ANCRES =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== COMPTEUR ANIMÉ POUR LES STATISTIQUES =====
    const animateCounter = (element, target) => {
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 20);
    };

    // Observer les cartes de statistiques
    const statObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const h2 = entry.target.querySelector('h2');
                if (h2 && !h2.dataset.animated) {
                    const value = parseInt(h2.textContent);
                    if (!isNaN(value)) {
                        h2.textContent = '0';
                        animateCounter(h2, value);
                        h2.dataset.animated = 'true';
                    }
                }
                statObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-card').forEach(card => {
        statObserver.observe(card);
    });

    // ===== EFFET PARALLAX SUR LE HERO =====
    const jumbotron = document.querySelector('.jumbotron');
    if (jumbotron) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxSpeed = 0.5;
            jumbotron.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
        });
    }

    // ===== AUTO-DISMISS DES ALERTS APRÈS 5 SECONDES =====
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // ===== CONFIRMATION AVANT SUPPRESSION =====
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm || 'Êtes-vous sûr ?')) {
                e.preventDefault();
            }
        });
    });

    // ===== PRÉVISUALISATION D'IMAGE AVANT UPLOAD =====
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Créer ou mettre à jour la prévisualisation
                    let preview = document.getElementById('imagePreview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.id = 'imagePreview';
                        preview.className = 'mt-3';
                        input.parentElement.appendChild(preview);
                    }
                    preview.innerHTML = `
                        <p class="text-muted small">Aperçu :</p>
                        <img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px; animation: fadeInScale 0.3s;">
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // ===== EFFET DE CHARGEMENT SUR LES FORMULAIRES =====
    const forms = document.querySelectorAll('form:not(.quick-action-form)');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            // Ignorer les petits boutons de confirmation rapide
            if (submitBtn && !submitBtn.disabled && !submitBtn.classList.contains('btn-sm')) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Chargement...';
            }
        });
    });

    // ===== TOOLTIP BOOTSTRAP =====
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ===== ANIMATION DES CARTES PRODUITS AU SURVOL =====
    const productCards = document.querySelectorAll('.card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // ===== COMPTEUR PANIER ANIMÉ =====
    const updateCartBadge = (count) => {
        const badge = document.querySelector('.cart-badge');
        if (badge) {
            badge.textContent = count;
            badge.classList.add('pulse');
            setTimeout(() => badge.classList.remove('pulse'), 600);
        }
    };

    // ===== EFFET DE RECHERCHE EN TEMPS RÉEL (OPTIONNEL) =====
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchIcon = this.parentElement.querySelector('.fa-search');
            if (searchIcon) {
                searchIcon.classList.add('fa-spin');
            }
            
            searchTimeout = setTimeout(() => {
                if (searchIcon) {
                    searchIcon.classList.remove('fa-spin');
                }
            }, 500);
        });
    }

    // ===== MISE À JOUR DYNAMIQUE DES QUANTITÉS DANS LE PANIER =====
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const price = parseFloat(this.dataset.price);
            const quantity = parseInt(this.value);
            if (!isNaN(price) && !isNaN(quantity)) {
                const subtotalEl = this.closest('tr')?.querySelector('.subtotal');
                if (subtotalEl) {
                    const newSubtotal = (price * quantity).toFixed(2);
                    subtotalEl.textContent = `${newSubtotal} €`;
                    subtotalEl.classList.add('pulse');
                    setTimeout(() => subtotalEl.classList.remove('pulse'), 600);
                }
            }
        });
    });

    // ===== SCROLL TO TOP BUTTON =====
    const createScrollTopButton = () => {
        const button = document.createElement('button');
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.className = 'btn btn-primary rounded-circle position-fixed';
        button.style.cssText = `
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            display: none;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        
        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                button.style.display = 'block';
                button.style.animation = 'fadeInScale 0.3s';
            } else {
                button.style.display = 'none';
            }
        });

        document.body.appendChild(button);
    };

    createScrollTopButton();

    // ===== EFFET DE BRILLANCE SUR LES BOUTONS =====
    document.querySelectorAll('.shine').forEach(el => {
        el.addEventListener('mouseenter', function() {
            this.style.overflow = 'hidden';
        });
    });

    // ===== LOG DE DÉMARRAGE =====
    console.log('%c🛒 E-Commerce Platform ', 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; border-radius: 5px; font-size: 16px; font-weight: bold;');
    console.log('%cApplication chargée avec succès ! ✨', 'color: #10b981; font-size: 14px;');
});

// ===== HELPER FUNCTIONS =====

// Fonction pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Fonction pour animer un élément
function animateElement(element, animationClass = 'pulse') {
    element.classList.add(animationClass);
    element.addEventListener('animationend', () => {
        element.classList.remove(animationClass);
    }, { once: true });
}

// Fonction pour afficher une notification toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInDown 0.3s reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

