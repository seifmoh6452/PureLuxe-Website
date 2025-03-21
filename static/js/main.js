// Initialize Stripe
const stripe = Stripe(STRIPE_PUBLIC_KEY);

// DOM Elements
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');
const themeToggle = document.querySelector('.theme-toggle');
const quantityInputs = document.querySelectorAll('.quantity-input');
const addToCartForms = document.querySelectorAll('.add-to-cart-form');
const cartUpdateForms = document.querySelectorAll('.cart-update-form');
const checkoutForm = document.querySelector('#checkout-form');
const alertCloseButtons = document.querySelectorAll('.alert-close');

// Mobile Menu Toggle
if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
            mobileMenuToggle.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });

    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuToggle.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.classList.remove('menu-open');
        });
    });
}

// Touch device optimizations
if ('ontouchstart' in window) {
    document.documentElement.classList.add('touch-device');
    
    // Add touch feedback to buttons
    document.querySelectorAll('.btn, .nav-link').forEach(element => {
        element.addEventListener('touchstart', function() {
            this.classList.add('touch-active');
        });
        
        element.addEventListener('touchend', function() {
            this.classList.remove('touch-active');
        });
    });
}

// Prevent zoom on input focus for iOS
const viewportMeta = document.querySelector('meta[name="viewport"]');
if (viewportMeta) {
    if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
        viewportMeta.content = 'width=device-width, initial-scale=1, maximum-scale=1';
    }
}

// Theme handling
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    document.body.style.backgroundColor = theme === 'dark' ? '#1A1A1A' : '#FFFFFF';
    
    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        if (theme === 'dark') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
}

// Initialize theme
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Remove animation observer code
    const scrollHandler = () => {
        const scrolled = window.scrollY > 50;
        document.querySelector('.header')?.classList.toggle('scrolled', scrolled);
    };

    window.addEventListener('scroll', scrollHandler);

    // Optimized cart updates
    const updateCartCount = async () => {
        try {
            const response = await fetch('/cart/count');
            const data = await response.json();
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                cartCount.textContent = data.count;
            }
        } catch (error) {
            console.error('Error updating cart count:', error);
        }
    };

    // Simple notification without animations
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Remove product card animations
    document.querySelector('.products-grid')?.addEventListener('click', (e) => {
        const productCard = e.target.closest('.product-card');
        if (productCard) {
            // Handle click without animations
        }
    });

    // Cache DOM elements
    const header = document.querySelector('.header');
    const themeToggle = document.querySelector('.theme-toggle');
    
    // Theme toggle with smooth transition
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.documentElement.style.setProperty('--transition-speed', '0.3s');
            document.documentElement.setAttribute('data-theme',
                document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
            );
            localStorage.setItem('theme',
                document.documentElement.getAttribute('data-theme')
            );
            setTimeout(() => {
                document.documentElement.style.removeProperty('--transition-speed');
            }, 300);
        });
    }

    // Optimize quantity input handlers
    quantityInputs.forEach(input => {
        const minusBtn = input.parentElement.querySelector('.quantity-minus');
        const plusBtn = input.parentElement.querySelector('.quantity-plus');
        
        if (minusBtn) {
            minusBtn.addEventListener('click', throttle(() => {
                const currentValue = parseInt(input.value);
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    triggerUpdateCart(input);
                }
            }, 200));
        }
        
        if (plusBtn) {
            plusBtn.addEventListener('click', throttle(() => {
                const currentValue = parseInt(input.value);
                input.value = currentValue + 1;
                triggerUpdateCart(input);
            }, 200));
        }
    });

    // Cache DOM elements
    const productCards = document.querySelectorAll('.product-card');
    const cartItems = document.querySelectorAll('.cart-item');

    // Add smooth transitions for product cards
    productCards.forEach(card => {
        card.style.willChange = 'transform, opacity';
    });

    // Add to Cart Form Handler
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            
            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok && data.status === 'success') {
                    // Update cart count in header
                    const cartCount = document.querySelector('.cart-count');
                    if (cartCount) {
                        cartCount.textContent = data.cart_count;
                    }
                    
                    showNotification('Product added to cart successfully!', 'success');
                } else {
                    throw new Error(data.message || 'Failed to add product to cart');
                }
            } catch (error) {
                showNotification(error.message, 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
            }
        });
    });

    // Cart Update Form Handler
    document.querySelectorAll('.cart-update-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
            }
            
            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok && data.status === 'success') {
                    // Update cart count and totals
                    updateCartDisplay(data);
                    showNotification('Cart updated successfully!', 'success');
                } else {
                    throw new Error(data.message || 'Failed to update cart');
                }
            } catch (error) {
                showNotification(error.message, 'error');
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('loading');
                }
            }
        });
    });

    // Remove item form handler
    document.querySelectorAll('.remove-item-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            
            try {
                const formData = new FormData(form);
                const response = await fetch('/update_cart', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const cartItem = form.closest('.cart-item');
                    if (cartItem) {
                        cartItem.remove();
                        
                        // Update cart count in header
                        const cartCount = document.querySelector('.cart-count');
                        if (cartCount) {
                            cartCount.textContent = data.cart_count;
                        }
                        
                        // Reload if cart is empty
                        if (data.cart_count === 0) {
                            location.reload();
                        } else {
                            // Update totals
                            const cartTotal = document.querySelector('.cart-total');
                            if (cartTotal) {
                                cartTotal.textContent = `$${data.cart_total.toFixed(2)}`;
                            }
                            
                            const shippingCost = data.cart_total >= 50 ? 0 : 5;
                            const shippingElement = document.querySelector('.shipping-cost');
                            if (shippingElement) {
                                shippingElement.textContent = shippingCost === 0 ? 'Free' : `$${shippingCost.toFixed(2)}`;
                            }
                            
                            const finalTotal = document.querySelector('.final-total');
                            if (finalTotal) {
                                finalTotal.textContent = `$${(data.cart_total + shippingCost).toFixed(2)}`;
                            }
                        }
                        
                        showNotification('Item removed from cart', 'success');
                    }
                } else {
                    throw new Error(data.message || 'Failed to remove item');
                }
            } catch (error) {
                showNotification(error.message, 'error');
            } finally {
                submitBtn.disabled = false;
            }
        });
    });
});

// Quantity Selector Handlers
document.querySelectorAll('.quantity-selector').forEach(selector => {
    const input = selector.querySelector('.quantity-input');
    const minusBtn = selector.querySelector('.quantity-minus');
    const plusBtn = selector.querySelector('.quantity-plus');
    
    if (input && minusBtn && plusBtn) {
        minusBtn.addEventListener('click', () => {
            const currentValue = parseInt(input.value);
            if (currentValue > 1) {
                input.value = currentValue - 1;
                const form = selector.closest('form');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
        });
        
        plusBtn.addEventListener('click', () => {
            const currentValue = parseInt(input.value);
            input.value = currentValue + 1;
            const form = selector.closest('form');
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        });
        
        input.addEventListener('change', () => {
            const form = selector.closest('form');
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        });
    }
});

// Checkout Form Handler
if (checkoutForm) {
    checkoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = checkoutForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        
        try {
            const formData = new FormData(checkoutForm);
            const response = await fetch(checkoutForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                // Redirect to order success page
                window.location.href = data.redirect_url;
            } else {
                throw new Error(data.message || 'Failed to process order');
            }
        } catch (error) {
            showNotification(error.message, 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    });
}

// Alert Close Buttons
alertCloseButtons.forEach(button => {
    button.addEventListener('click', () => {
        const alert = button.closest('.alert');
        alert.remove();
    });
});

// Helper Functions
function triggerUpdateCart(input) {
    const form = input.closest('form');
    if (form) {
        const event = new Event('submit', { cancelable: true });
        form.dispatchEvent(event);
    }
}

// Product Image Gallery
const productThumbnails = document.querySelectorAll('.product-thumbnail');
const mainProductImage = document.querySelector('.main-product-image');

if (productThumbnails.length && mainProductImage) {
    productThumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', () => {
            const newImageSrc = thumbnail.getAttribute('data-image');
            mainProductImage.src = newImageSrc;
            
            // Update active state
            productThumbnails.forEach(thumb => thumb.classList.remove('active'));
            thumbnail.classList.add('active');
        });
    });
}

// Smooth Scroll for Anchor Links
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

// Newsletter Form
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = newsletterForm.querySelector('button[type="submit"]');
        const emailInput = newsletterForm.querySelector('input[type="email"]');
        
        submitBtn.classList.add('loading');
        
        try {
            const response = await fetch('/newsletter/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: emailInput.value
                })
            });
            
            if (response.ok) {
                showNotification('Successfully subscribed to newsletter!', 'success');
                emailInput.value = '';
            } else {
                throw new Error('Failed to subscribe to newsletter');
            }
        } catch (error) {
            showNotification(error.message, 'error');
        } finally {
            submitBtn.classList.remove('loading');
        }
    });
}

// Helper function to update cart display
function updateCartDisplay(data) {
    // Update cart count
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = data.cart_count;
    }
    
    // Update cart total
    const cartTotal = document.querySelector('.cart-total');
    if (cartTotal && data.cart_total) {
        cartTotal.textContent = `${data.cart_total.toFixed(2)} EGP`;
    }
    
    // Update shipping cost if available
    if (data.shipping_cost !== undefined) {
        const shippingCost = document.querySelector('.shipping-cost');
        if (shippingCost) {
            shippingCost.textContent = data.shipping_cost === 0 ? 'Free' : `${data.shipping_cost.toFixed(2)} EGP`;
        }
    }
    
    // Update final total if available
    if (data.final_total !== undefined) {
        const finalTotal = document.querySelector('.final-total');
        if (finalTotal) {
            finalTotal.textContent = `${data.final_total.toFixed(2)} EGP`;
        }
    }
} 