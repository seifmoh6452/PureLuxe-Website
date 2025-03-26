import os
import psutil
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import atexit
import re
import sys
from functools import wraps
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, generate_csrf
from itsdangerous import URLSafeTimedSerializer
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from flask import url_for, redirect, session, flash
import oauthlib.oauth2.rfc6749.errors
from flask.sessions import SecureCookieSessionInterface
import secrets
import time

# Allow OAuth over HTTP for development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Load environment variables
load_dotenv()

# Create Flask app instance first
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection

# Load configurations
app.config.from_object('config.Config')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Add CSRF token to all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=lambda: csrf._get_token())

# Configure logging
log_dir = 'logs'
log_file = os.path.join(log_dir, 'pureluxe.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Remove any existing handlers to avoid duplicates
for handler in logging.getLogger().handlers[:]:
    logging.getLogger().removeHandler(handler)

# Configure console handler for stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))
console_handler.setLevel(logging.INFO)

# Configure root logger first with just console logging
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

try:
    # Configure file handler with proper permissions
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10,
        delay=True,  # Delay file creation until first write
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    # Add file handler to root logger
    logging.getLogger().addHandler(file_handler)

    # Configure Flask app logger
    app.logger.handlers = []  # Remove any existing handlers
    app.logger.propagate = True  # Use root logger handlers
    
except Exception as e:
    logging.warning(f"Could not set up file logging: {e}")

# Register cleanup function
def cleanup_handlers():
    for handler in logging.getLogger().handlers[:]:
        try:
            handler.close()
        except:
            pass
        logging.getLogger().removeHandler(handler)

atexit.register(cleanup_handlers)

app.logger.info('PureLuxe startup')

# Production configurations
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Security configurations
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'

# Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

# Language support
LANGUAGES = {
    'en': 'English',
    'ar': 'العربية'
}

# Dictionary of translations
TRANSLATIONS = {
    'en': {
        # Navigation
        'Home': 'Home',
        'Shop': 'Shop',
        'About': 'About',
        'Contact': 'Contact',
        'Login': 'Login',
        'Cart': 'Cart',
        'Search': 'Search',
        
        # Ramadan Theme
        'Welcome to Our Ramadan Collection': 'Welcome to Our Ramadan Collection',
        'Discover our special Ramadan collection of natural care products, perfect for your self-care routine during the blessed month': 'Discover our special Ramadan collection of natural care products, perfect for your self-care routine during the blessed month',
        'Shop Ramadan Collection': 'Shop Ramadan Collection',
        'Special Offers': 'Special Offers',
        'Days': 'Days',
        'Hours': 'Hours',
        'Minutes': 'Minutes',
        'Seconds': 'Seconds',
        'Just 4 Days Until The Blessed Month!': 'Just 4 Days Until The Blessed Month!',
        'Prepare for your spiritual journey with our special Ramadan collection': 'Prepare for your spiritual journey with our special Ramadan collection',
        
        # Special Offers Section
        'Special Ramadan Offers': 'Special Ramadan Offers',
        'Celebrate this blessed month with our exclusive Ramadan deals and packages': 'Celebrate this blessed month with our exclusive Ramadan deals and packages',
        'Ramadan Gift Sets': 'Ramadan Gift Sets',
        'Special gift packages perfect for Iftar gatherings and Eid celebrations': 'Special gift packages perfect for Iftar gatherings and Eid celebrations',
        'Special Discounts': 'Special Discounts',
        'Enjoy up to 30% off on selected products throughout Ramadan': 'Enjoy up to 30% off on selected products throughout Ramadan',
        'Free Gift Wrapping': 'Free Gift Wrapping',
        'Complimentary luxury gift wrapping service for all orders': 'Complimentary luxury gift wrapping service for all orders',
        
        # Features Section
        'Why Choose PureLuxe?': 'Why Choose PureLuxe?',
        '100% Natural': '100% Natural',
        'Made with carefully selected natural ingredients that nourish both hair and skin': 'Made with carefully selected natural ingredients that nourish both hair and skin',
        'Eco-Friendly': 'Eco-Friendly',
        'Sustainable packaging and biodegradable formula for minimal environmental impact': 'Sustainable packaging and biodegradable formula for minimal environmental impact',
        'Science-Backed': 'Science-Backed',
        'Formulated with proven scientific principles for optimal pH balance': 'Formulated with proven scientific principles for optimal pH balance',

        # About Page
        'Our Story': 'Our Story',
        'Crafting pure, luxurious solutions for hair and skin care': 'Crafting pure, luxurious solutions for hair and skin care',
        'Our Mission': 'Our Mission',
        'At PureLuxe, we believe in the power of pure, natural ingredients combined with scientific innovation': 'At PureLuxe, we believe in the power of pure, natural ingredients combined with scientific innovation',
        'Our Journey': 'Our Journey',
        'Our Team': 'Our Team',
        'Our Commitment': 'Our Commitment',

        # Team Titles and Descriptions
        'CEO & Founder': 'CEO & Founder',
        'Co-Founder and Chemist': 'Co-Founder and Chemist',
        'Marketing Director': 'Marketing Director',
        'Creating compelling strategies to share our vision': 'Creating compelling strategies to share our vision',
        'Technical Director': 'Technical Director',
        'Driving technological innovation in our processes': 'Driving technological innovation in our processes',
        'Head of Operations': 'Head of Operations',
        'Ensuring smooth operations and quality standards': 'Ensuring smooth operations and quality standards',
        'Strategic Advisor': 'Strategic Advisor',
        'Providing strategic guidance and industry expertise': 'Providing strategic guidance and industry expertise',

        # Product Pages
        'Add to Cart': 'Add to Cart',
        'View Details': 'View Details',
        'Out of Stock': 'Out of Stock',
        'Price': 'Price',
        'Quantity': 'Quantity',
        'Total': 'Total',
        'Size': 'Size',
        'Description': 'Description',
        'Related Products': 'Related Products',

        # Shopping Cart
        'Shopping Cart': 'Shopping Cart',
        'Your cart is empty': 'Your cart is empty',
        'Continue Shopping': 'Continue Shopping',
        'Proceed to Checkout': 'Proceed to Checkout',
        'Subtotal': 'Subtotal',
        'Shipping': 'Shipping',
        'Free Shipping Applied': 'Free Shipping Applied',
        'Order Summary': 'Order Summary',

        # Authentication
        'Welcome Back': 'Welcome Back',
        'Sign in to your account': 'Sign in to your account',
        'Email Address': 'Email Address',
        'Password': 'Password',
        'Remember me': 'Remember me',
        'Forgot password?': 'Forgot password?',
        'Don\'t have an account?': 'Don\'t have an account?',
        'Sign Up': 'Sign Up',
        'Register': 'Register',
        'My Profile': 'My Profile',
        'My Orders': 'My Orders',
        'Logout': 'Logout',

        # Footer
        'About PureLuxe': 'About PureLuxe',
        'Quick Links': 'Quick Links',
        'Contact Us': 'Contact Us',
        'Newsletter': 'Newsletter',
        'Subscribe': 'Subscribe',
        'Enter your email': 'Enter your email',
        'Privacy Policy': 'Privacy Policy',
        'Terms of Service': 'Terms of Service',
        'All rights reserved': 'All rights reserved',

        # Values
        'Natural Ingredients': 'Natural Ingredients',
        'Scientific Innovation': 'Scientific Innovation',
        'Customer Care': 'Customer Care',
        'Sustainability': 'Sustainability',
        'Quality': 'Quality',
        'Transparency': 'Transparency',
        'Global Impact': 'Global Impact',

        # Additional About Page Content
        'We meticulously select the finest natural ingredients, sourcing from sustainable suppliers to create products that nourish and enhance your natural beauty.': 'We meticulously select the finest natural ingredients, sourcing from sustainable suppliers to create products that nourish and enhance your natural beauty.',
        'Our advanced formulations are backed by extensive research and developed using cutting-edge technology to ensure optimal effectiveness.': 'Our advanced formulations are backed by extensive research and developed using cutting-edge technology to ensure optimal effectiveness.',
        'Your satisfaction and well-being are our top priorities. We are committed to providing exceptional products and personalized support.': 'Your satisfaction and well-being are our top priorities. We are committed to providing exceptional products and personalized support.',
        'Embark on our journey of innovation and excellence in natural beauty care, where each milestone represents our commitment to quality and sustainability.': 'Embark on our journey of innovation and excellence in natural beauty care, where each milestone represents our commitment to quality and sustainability.',
        'PureLuxe was founded with a vision to revolutionize natural beauty care through innovative formulations and sustainable practices.': 'PureLuxe was founded with a vision to revolutionize natural beauty care through innovative formulations and sustainable practices.',
        'Introduced our signature cleanser, combining pure ingredients with scientific excellence for exceptional results.': 'Introduced our signature cleanser, combining pure ingredients with scientific excellence for exceptional results.',
        'Pioneered sustainable packaging solutions and launched our comprehensive eco-conscious product line.': 'Pioneered sustainable packaging solutions and launched our comprehensive eco-conscious product line.',
        'Expanded our presence across international markets while maintaining our commitment to quality and sustainability.': 'Expanded our presence across international markets while maintaining our commitment to quality and sustainability.',
        'Global Expansion': 'Global Expansion',
        'We\'re committed to minimizing our environmental impact through sustainable practices and eco-friendly packaging solutions.': 'We\'re committed to minimizing our environmental impact through sustainable practices and eco-friendly packaging solutions.',
        'Every product undergoes rigorous testing to ensure it meets our high standards of excellence and purity.': 'Every product undergoes rigorous testing to ensure it meets our high standards of excellence and purity.',
        'We believe in complete transparency about our ingredients and processes, building lasting trust with our customers.': 'We believe in complete transparency about our ingredients and processes, building lasting trust with our customers.',
        'At PureLuxe, we believe in the power of pure, natural ingredients combined with scientific innovation to create exceptional beauty care products that enhance your natural radiance.': 'At PureLuxe, we believe in the power of pure, natural ingredients combined with scientific innovation to create exceptional beauty care products that enhance your natural radiance.',

        # Timeline Events
        'The Beginning': 'The Beginning',
        'First Product Launch': 'First Product Launch',
        'Eco-Friendly Initiative': 'Eco-Friendly Initiative',
        'Team Formation': 'Team Formation',

        # Benefits Section
        'One Product, Double Benefits': 'One Product, Double Benefits',
        'For Your Hair': 'For Your Hair',
        'For Your Skin': 'For Your Skin',
        'Deep cleansing without stripping natural oils': 'Deep cleansing without stripping natural oils',
        'Promotes healthy scalp environment': 'Promotes healthy scalp environment',
        'Enhances natural shine and volume': 'Enhances natural shine and volume',
        'Reduces frizz and improves manageability': 'Reduces frizz and improves manageability',
        'Gentle cleansing for all skin types': 'Gentle cleansing for all skin types',
        'Maintains skin\'s natural moisture barrier': 'Maintains skin\'s natural moisture barrier',
        'Helps balance skin pH levels': 'Helps balance skin pH levels',
        'Suitable for sensitive skin': 'Suitable for sensitive skin',

        # Ingredients Section
        'Aloe Vera': 'Aloe Vera',
        'Hydration & Soothing': 'Hydration & Soothing',
        'Natural moisturizer that helps maintain skin and scalp health': 'Natural moisturizer that helps maintain skin and scalp health',
        'Coconut Oil': 'Coconut Oil',
        'Nourishment': 'Nourishment',
        'Rich in fatty acids that protect and nourish both hair and skin': 'Rich in fatty acids that protect and nourish both hair and skin',
        'Chamomile': 'Chamomile',
        'Calming': 'Calming',
        'Soothes sensitive skin and provides anti-inflammatory benefits': 'Soothes sensitive skin and provides anti-inflammatory benefits',
        'Tea Tree Oil': 'Tea Tree Oil',
        'Purifying': 'Purifying',
        'Natural antimicrobial properties for a healthy scalp and skin': 'Natural antimicrobial properties for a healthy scalp and skin',

        # Testimonials Section
        'What Our Customers Say': 'What Our Customers Say',
        'Verified Customer': 'Verified Customer',
        'Loyal Customer': 'Loyal Customer',
        'Beauty Enthusiast': 'Beauty Enthusiast',
        'Amazing product! My hair and skin have never felt better. Love that it\'s all natural!': 'Amazing product! My hair and skin have never felt better. Love that it\'s all natural!',
        'Finally, a product that works for both my hair and body. Simplified my routine!': 'Finally, a product that works for both my hair and body. Simplified my routine!',
        'The eco-friendly packaging and natural ingredients make me feel good about my purchase.': 'The eco-friendly packaging and natural ingredients make me feel good about my purchase.',

        # CTA Section
        'Ready to Transform Your Hair & Skin Care Routine?': 'Ready to Transform Your Hair & Skin Care Routine?',
        'Join thousands of satisfied customers who have simplified their routine with PureLuxe.': 'Join thousands of satisfied customers who have simplified their routine with PureLuxe.',

        # FAQ Section
        'Frequently Asked Questions': 'Frequently Asked Questions',
        'Is it suitable for all hair types?': 'Is it suitable for all hair types?',
        'Yes! Our formula is designed to work effectively for all hair types while being gentle enough for daily use.': 'Yes! Our formula is designed to work effectively for all hair types while being gentle enough for daily use.',
        'How often should I use it?': 'How often should I use it?',
        'You can use it daily or as needed. The gentle formula won\'t strip your natural oils.': 'You can use it daily or as needed. The gentle formula won\'t strip your natural oils.',
        'Is it really eco-friendly?': 'Is it really eco-friendly?',
        'Absolutely! Our packaging is recyclable and the formula is biodegradable.': 'Absolutely! Our packaging is recyclable and the formula is biodegradable.',
        'What makes it different?': 'What makes it different?',
        'Our unique blend of natural ingredients and scientific formulation makes it perfect for both hair and skin.': 'Our unique blend of natural ingredients and scientific formulation makes it perfect for both hair and skin.',

        # Admin Panel
        'Total Orders': 'Total Orders',
        'Total Revenue (EGP)': 'Total Revenue (EGP)',
        'Pending Orders': 'Pending Orders',
        'Completed Orders': 'Completed Orders',
        'Orders Management': 'Orders Management',
        'Clear All Orders': 'Clear All Orders',
        'Order #': 'Order #',
        'Shipping Address:': 'Shipping Address:',
        'Size:': 'Size:',
        'Quantity:': 'Quantity:',
        'Total:': 'Total:',
        'Order status updated successfully': 'Order status updated successfully',
        'Failed to update order status': 'Failed to update order status',
        'Are you sure you want to clear all orders? This action cannot be undone.': 'Are you sure you want to clear all orders? This action cannot be undone.',
        'pending': 'pending',
        'completed': 'completed',
        'Pending': 'Pending',
        'Completed': 'Completed',

        # Contact Page
        'Contact Us - PureLuxe': 'Contact Us - PureLuxe',
        'Get in Touch': 'Get in Touch',
        'We\'d love to hear from you. Our team is always here to help.': 'We\'d love to hear from you. Our team is always here to help.',
        'Experience exceptional customer service with PureLuxe. Whether you have questions about our products, need assistance with an order, or want to learn more about our natural ingredients, our dedicated team is ready to assist you.': 'Experience exceptional customer service with PureLuxe. Whether you have questions about our products, need assistance with an order, or want to learn more about our natural ingredients, our dedicated team is ready to assist you.',
        '24/7 Customer Support': '24/7 Customer Support',
        'Fast Response Time': 'Fast Response Time',
        'Dedicated Care Team': 'Dedicated Care Team',
        'Visit Us': 'Visit Us',
        'Call Us': 'Call Us',
        'Mon-Fri: 9AM-6PM': 'Mon-Fri: 9AM-6PM',
        'Email Us': 'Email Us',
        'We\'ll respond within 24 hours': 'We\'ll respond within 24 hours',
        'Follow Us': 'Follow Us',
        'Send Us a Message': 'Send Us a Message',
        'Fill out the form below and we\'ll get back to you as soon as possible.': 'Fill out the form below and we\'ll get back to you as soon as possible.',
        'Your Name': 'Your Name',
        'Enter your full name': 'Enter your full name',
        'Your Email': 'Your Email',
        'Enter your email address': 'Enter your email address',
        'Subject': 'Subject',
        'What is your message about?': 'What is your message about?',
        'Message': 'Message',
        'Type your message here...': 'Type your message here...',
        'Send Message': 'Send Message',
        'Sending...': 'Sending...',
        'Common Questions': 'Common Questions',
        'What are your shipping times?': 'What are your shipping times?',
        'We typically process orders within 1-2 business days. Shipping times vary by location, usually 3-5 business days domestically.': 'We typically process orders within 1-2 business days. Shipping times vary by location, usually 3-5 business days domestically.',
        'Do you offer international shipping?': 'Do you offer international shipping?',
        'Yes, we ship to most countries worldwide. International shipping times typically range from 7-14 business days.': 'Yes, we ship to most countries worldwide. International shipping times typically range from 7-14 business days.',
        'What is your return policy?': 'What is your return policy?',
        'We offer a 30-day satisfaction guarantee. If you\'re not completely satisfied, you can return unused products for a full refund.': 'We offer a 30-day satisfaction guarantee. If you\'re not completely satisfied, you can return unused products for a full refund.',

        # Profile Page
        'Recent Orders': 'Recent Orders',
        'Shipping Addresses': 'Shipping Addresses',
        'No shipping addresses found.': 'No shipping addresses found.',
        'Points': 'Points',
        'Orders': 'Orders',
        'Home': 'Home',
        'Billing': 'Billing',
        'Office': 'Office',
        'Thank You for Your Order!': 'Thank You for Your Order!',
        'Order': 'Order',
        "We've received your order and will begin processing it right away.": "We've received your order and will begin processing it right away.",
        "You'll receive an email confirmation shortly with your order details.": "You'll receive an email confirmation shortly with your order details.",
        'Order Details': 'Order Details',
        'Shipping Address': 'Shipping Address',
        'Payment Method': 'Payment Method',
        'Cash on Delivery': 'Cash on Delivery',
        'Please prepare exact change for the delivery person.': 'Please prepare exact change for the delivery person.',
        'Shipping Method': 'Shipping Method',
        'Express Shipping': 'Express Shipping',
        'Standard Shipping': 'Standard Shipping',
        'Estimated delivery:': 'Estimated delivery:',
        'Same day delivery': 'Same day delivery',
        '2-3 business days': '2-3 business days',
        'View Order History': 'View Order History',
    },
    'ar': {
        # Navigation
        'Home': 'الرئيسية',
        'Shop': 'المتجر',
        'About': 'عن الشركة',
        'Contact': 'اتصل بنا',
        'Login': 'تسجيل الدخول',
        'Cart': 'عربة التسوق',
        'Search': 'بحث',
        
        # Ramadan Theme
        'Welcome to Our Ramadan Collection': 'مرحباً بكم في مجموعة رمضان',
        'Discover our special Ramadan collection of natural care products, perfect for your self-care routine during the blessed month': 'اكتشف مجموعتنا الخاصة من منتجات العناية الطبيعية لرمضان، مثالية لروتين العناية الخاص بك خلال الشهر الفضيل',
        'Shop Ramadan Collection': 'تسوق مجموعة رمضان',
        'Special Offers': 'عروض خاصة',
        'Days': 'أيام',
        'Hours': 'ساعات',
        'Minutes': 'دقائق',
        'Seconds': 'ثواني',
        'Just 4 Days Until The Blessed Month!': 'باقي ٤ أيام على الشهر الفضيل!',
        'Prepare for your spiritual journey with our special Ramadan collection': 'استعد لرحلتك الروحانية مع مجموعتنا الخاصة لرمضان',
        
        # Special Offers Section
        'Special Ramadan Offers': 'عروض رمضان المميزة',
        'Celebrate this blessed month with our exclusive Ramadan deals and packages': 'احتفل بهذا الشهر المبارك مع عروضنا وباقاتنا الحصرية لرمضان',
        'Ramadan Gift Sets': 'أطقم هدايا رمضان',
        'Special gift packages perfect for Iftar gatherings and Eid celebrations': 'باقات هدايا مميزة مثالية لتجمعات الإفطار واحتفالات العيد',
        'Special Discounts': 'خصومات خاصة',
        'Enjoy up to 30% off on selected products throughout Ramadan': 'استمتع بخصم يصل إلى ٣٠٪ على منتجات مختارة طوال شهر رمضان',
        'Free Gift Wrapping': 'تغليف هدايا مجاني',
        'Complimentary luxury gift wrapping service for all orders': 'خدمة تغليف هدايا فاخرة مجانية لجميع الطلبات',
        
        # Features Section
        'Why Choose PureLuxe?': 'لماذا تختار بيور لوكس؟',
        '100% Natural': '١٠٠٪ طبيعي',
        'Made with carefully selected natural ingredients that nourish both hair and skin': 'مصنوع من مكونات طبيعية مختارة بعناية تغذي الشعر والبشرة',
        'Eco-Friendly': 'صديق للبيئة',
        'Sustainable packaging and biodegradable formula for minimal environmental impact': 'عبوات مستدامة وتركيبة قابلة للتحلل لتأثير بيئي أدنى',
        'Science-Backed': 'مدعوم علمياً',
        'Formulated with proven scientific principles for optimal pH balance': 'تم تركيبه وفقاً لمبادئ علمية مثبتة للتوازن الأمثل للحموضة',

        # About Page
        'Our Story': 'قصتنا',
        'Crafting pure, luxurious solutions for hair and skin care': 'نصنع حلولاً نقية وفاخرة للعناية بالشعر والبشرة',
        'Our Mission': 'مهمتنا',
        'At PureLuxe, we believe in the power of pure, natural ingredients combined with scientific innovation': 'في بيور لوكس، نؤمن بقوة المكونات الطبيعية النقية مع الابتكار العلمي',
        'Our Journey': 'رحلتنا',
        'Our Team': 'فريقنا',
        'Our Commitment': 'التزامنا',

        # Team Titles and Descriptions
        'CEO & Founder': 'الرئيس التنفيذي والمؤسس',
        'Co-Founder and Chemist': 'المؤسس المشارك والكيميائي',
        'Marketing Director': 'مدير التسويق',
        'Creating compelling strategies to share our vision': 'يبتكر استراتيجيات مقنعة لمشاركة رؤيتنا',
        'Technical Director': 'المدير التقني',
        'Driving technological innovation in our processes': 'يقود الابتكار التكنولوجي في عملياتنا',
        'Head of Operations': 'رئيس العمليات',
        'Ensuring smooth operations and quality standards': 'يضمن سير العمليات وجودة المعايير',
        'Strategic Advisor': 'المستشار الاستراتيجي',
        'Providing strategic guidance and industry expertise': 'يقدم التوجيه الاستراتيجي وخبرة الصناعة',

        # Product Pages
        'Add to Cart': 'أضف إلى السلة',
        'View Details': 'عرض التفاصيل',
        'Out of Stock': 'نفذ من المخزون',
        'Price': 'السعر',
        'Quantity': 'الكمية',
        'Total': 'المجموع',
        'Size': 'الحجم',
        'Description': 'الوصف',
        'Related Products': 'منتجات ذات صلة',

        # Shopping Cart
        'Shopping Cart': 'عربة التسوق',
        'Your cart is empty': 'عربة التسوق فارغة',
        'Continue Shopping': 'مواصلة التسوق',
        'Proceed to Checkout': 'المتابعة للدفع',
        'Subtotal': 'المجموع الفرعي',
        'Shipping': 'الشحن',
        'Free Shipping Applied': 'تم تطبيق الشحن المجاني',
        'Order Summary': 'ملخص الطلب',

        # Authentication
        'Welcome Back': 'مرحباً بعودتك',
        'Sign in to your account': 'تسجيل الدخول إلى حسابك',
        'Email Address': 'البريد الإلكتروني',
        'Password': 'كلمة المرور',
        'Remember me': 'تذكرني',
        'Forgot password?': 'نسيت كلمة المرور؟',
        'Don\'t have an account?': 'ليس لديك حساب؟',
        'Sign Up': 'تسجيل جديد',
        'Register': 'تسجيل',
        'My Profile': 'ملفي الشخصي',
        'My Orders': 'طلباتي',
        'Logout': 'تسجيل الخروج',

        # Footer
        'About PureLuxe': 'عن بيور لوكس',
        'Quick Links': 'روابط سريعة',
        'Contact Us': 'اتصل بنا',
        'Newsletter': 'النشرة الإخبارية',
        'Subscribe': 'اشترك',
        'Enter your email': 'أدخل بريدك الإلكتروني',
        'Privacy Policy': 'سياسة الخصوصية',
        'Terms of Service': 'شروط الخدمة',
        'All rights reserved': 'جميع الحقوق محفوظة',

        # Values
        'Natural Ingredients': 'مكونات طبيعية',
        'Scientific Innovation': 'ابتكار علمي',
        'Customer Care': 'خدمة العملاء',
        'Sustainability': 'الاستدامة',
        'Quality': 'الجودة',
        'Transparency': 'الشفافية',
        'Global Impact': 'التأثير العالمي',

        # Additional About Page Content
        'We meticulously select the finest natural ingredients, sourcing from sustainable suppliers to create products that nourish and enhance your natural beauty.': 'نختار بعناية أفضل المكونات الطبيعية، ونحصل عليها من موردين مستدامين لإنشاء منتجات تغذي وتعزز جمالك الطبيعي.',
        'Our advanced formulations are backed by extensive research and developed using cutting-edge technology to ensure optimal effectiveness.': 'تركيباتنا المتقدمة مدعومة بأبحاث مكثفة وتم تطويرها باستخدام أحدث التقنيات لضمان الفعالية المثلى.',
        'Your satisfaction and well-being are our top priorities. We are committed to providing exceptional products and personalized support.': 'رضاك وراحتك هما أولوياتنا القصوى. نحن ملتزمون بتقديم منتجات استثنائية ودعم شخصي.',
        'Embark on our journey of innovation and excellence in natural beauty care, where each milestone represents our commitment to quality and sustainability.': 'انطلق في رحلتنا من الابتكار والتميز في العناية بالجمال الطبيعي، حيث يمثل كل إنجاز التزامنا بالجودة والاستدامة.',
        'PureLuxe was founded with a vision to revolutionize natural beauty care through innovative formulations and sustainable practices.': 'تأسست بيور لوكس برؤية لإحداث ثورة في العناية بالجمال الطبيعي من خلال تركيبات مبتكرة وممارسات مستدامة.',
        'Introduced our signature cleanser, combining pure ingredients with scientific excellence for exceptional results.': 'قدمنا منظفنا المميز، الذي يجمع بين المكونات النقية والتميز العلمي لنتائج استثنائية.',
        'Pioneered sustainable packaging solutions and launched our comprehensive eco-conscious product line.': 'رائدة في حلول التعبئة المستدامة وأطلقت مجموعة منتجاتنا الشاملة الصديقة للبيئة.',
        'Expanded our presence across international markets while maintaining our commitment to quality and sustainability.': 'وسعنا تواجدنا في الأسواق الدولية مع الحفاظ على التزامنا بالجودة والاستدامة.',
        'Global Expansion': 'التوسع العالمي',
        'We\'re committed to minimizing our environmental impact through sustainable practices and eco-friendly packaging solutions.': 'نحن ملتزمون بتقليل تأثيرنا البيئي من خلال الممارسات المستدامة وحلول التعبئة والتغليف الصديقة للبيئة.',
        'Every product undergoes rigorous testing to ensure it meets our high standards of excellence and purity.': 'يخضع كل منتج لاختبارات صارمة لضمان تلبيته لمعاييرنا العالية من التميز والنقاء.',
        'We believe in complete transparency about our ingredients and processes, building lasting trust with our customers.': 'نؤمن بالشفافية الكاملة حول مكوناتنا وعملياتنا، مما يبني ثقة دائمة مع عملائنا.',
        'At PureLuxe, we believe in the power of pure, natural ingredients combined with scientific innovation to create exceptional beauty care products that enhance your natural radiance.': 'في بيور لوكس، نؤمن بقوة المكونات الطبيعية النقية مع الابتكار العلمي لإنشاء منتجات عناية بالجمال استثنائية تعزز إشراقتك الطبيعية.',

        # Timeline Events
        'The Beginning': 'البداية',
        'First Product Launch': 'إطلاق أول منتج',
        'Eco-Friendly Initiative': 'مبادرة صديقة للبيئة',
        'Team Formation': 'تشكيل الفريق',

        # Benefits Section
        'One Product, Double Benefits': 'منتج واحد، فوائد مضاعفة',
        'For Your Hair': 'لشعرك',
        'For Your Skin': 'لبشرتك',
        'Deep cleansing without stripping natural oils': 'تنظيف عميق دون إزالة الزيوت الطبيعية',
        'Promotes healthy scalp environment': 'يعزز بيئة صحية لفروة الرأس',
        'Enhances natural shine and volume': 'يعزز اللمعان والحجم الطبيعي',
        'Reduces frizz and improves manageability': 'يقلل من التجعد ويحسن قابلية التصفيف',
        'Gentle cleansing for all skin types': 'تنظيف لطيف لجميع أنواع البشرة',
        'Maintains skin\'s natural moisture barrier': 'يحافظ على حاجز الرطوبة الطبيعي للبشرة',
        'Helps balance skin pH levels': 'يساعد في توازن مستويات الحموضة في البشرة',
        'Suitable for sensitive skin': 'مناسب للبشرة الحساسة',

        # Ingredients Section
        'Aloe Vera': 'الصبار',
        'Hydration & Soothing': 'ترطيب وتهدئة',
        'Natural moisturizer that helps maintain skin and scalp health': 'مرطب طبيعي يساعد في الحفاظ على صحة البشرة وفروة الرأس',
        'Coconut Oil': 'زيت جوز الهند',
        'Nourishment': 'تغذية',
        'Rich in fatty acids that protect and nourish both hair and skin': 'غني بالأحماض الدهنية التي تحمي وتغذي الشعر والبشرة',
        'Chamomile': 'البابونج',
        'Calming': 'تهدئة',
        'Soothes sensitive skin and provides anti-inflammatory benefits': 'يهدئ البشرة الحساسة ويوفر فوائد مضادة للالتهابات',
        'Tea Tree Oil': 'زيت شجرة الشاي',
        'Purifying': 'تنقية',
        'Natural antimicrobial properties for a healthy scalp and skin': 'خصائص طبيعية مضادة للميكروبات لفروة رأس وبشرة صحية',

        # Testimonials Section
        'What Our Customers Say': 'ماذا يقول عملاؤنا',
        'Verified Customer': 'عميل موثق',
        'Loyal Customer': 'عميل دائم',
        'Beauty Enthusiast': 'خبير تجميل',
        'Amazing product! My hair and skin have never felt better. Love that it\'s all natural!': 'منتج رائع! لم يشعر شعري وبشرتي بهذا التحسن من قبل. أحب أنه طبيعي بالكامل!',
        'Finally, a product that works for both my hair and body. Simplified my routine!': 'أخيراً، منتج يعمل لكل من شعري وجسمي. بسّط روتيني اليومي!',
        'The eco-friendly packaging and natural ingredients make me feel good about my purchase.': 'العبوات الصديقة للبيئة والمكونات الطبيعية تجعلني أشعر بالرضا عن مشترياتي.',

        # CTA Section
        'Ready to Transform Your Hair & Skin Care Routine?': 'هل أنت مستعد لتغيير روتين العناية بشعرك وبشرتك؟',
        'Join thousands of satisfied customers who have simplified their routine with PureLuxe.': 'انضم إلى آلاف العملاء الراضين الذين بسطوا روتينهم مع بيور لوكس',

        # FAQ Section
        'Frequently Asked Questions': 'الأسئلة الشائعة',
        'Is it suitable for all hair types?': 'هل هو مناسب لجميع أنواع الشعر؟',
        'Yes! Our formula is designed to work effectively for all hair types while being gentle enough for daily use.': 'نعم! تم تصميم تركيبتنا لتعمل بفعالية مع جميع أنواع الشعر مع كونها لطيفة بما يكفي للاستخدام اليومي.',
        'How often should I use it?': 'كم مرة يجب أن أستخدمه؟',
        'You can use it daily or as needed. The gentle formula won\'t strip your natural oils.': 'يمكنك استخدامه يومياً أو حسب الحاجة. التركيبة اللطيفة لن تزيل زيوتك الطبيعية.',
        'Is it really eco-friendly?': 'هل هو حقاً صديق للبيئة؟',
        'Absolutely! Our packaging is recyclable and the formula is biodegradable.': 'بالتأكيد! عبواتنا قابلة لإعادة التدوير والتركيبة قابلة للتحلل.',
        'What makes it different?': 'ما الذي يجعله مختلفاً؟',
        'Our unique blend of natural ingredients and scientific formulation makes it perfect for both hair and skin.': 'مزيجنا الفريد من المكونات الطبيعية والتركيبة العلمية يجعله مثالياً لكل من الشعر والبشرة.',

        # Admin Panel
        'Total Orders': 'إجمالي الطلبات',
        'Total Revenue (EGP)': 'إجمالي الإيرادات (ج.م)',
        'Pending Orders': 'الطلبات المعلقة',
        'Completed Orders': 'الطلبات المكتملة',
        'Orders Management': 'إدارة الطلبات',
        'Clear All Orders': 'مسح جميع الطلبات',
        'Order #': 'طلب رقم #',
        'Shipping Address:': 'عنوان الشحن:',
        'Size:': 'الحجم:',
        'Quantity:': 'الكمية:',
        'Total:': 'المجموع:',
        'Order status updated successfully': 'تم تحديث حالة الطلب بنجاح',
        'Failed to update order status': 'فشل تحديث حالة الطلب',
        'Are you sure you want to clear all orders? This action cannot be undone.': 'هل أنت متأكد من أنك تريد مسح جميع الطلبات؟ لا يمكن التراجع عن هذا الإجراء.',
        'pending': 'معلق',
        'completed': 'مكتمل',
        'Pending': 'معلق',
        'Completed': 'مكتمل',

        # Contact Page
        'Contact Us - PureLuxe': 'اتصل بنا - بيور لوكس',
        'Get in Touch': 'تواصل معنا',
        'We\'d love to hear from you. Our team is always here to help.': 'نود أن نسمع منك. فريقنا متواجد دائماً للمساعدة.',
        'Experience exceptional customer service with PureLuxe. Whether you have questions about our products, need assistance with an order, or want to learn more about our natural ingredients, our dedicated team is ready to assist you.': 'استمتع بخدمة عملاء استثنائية مع بيور لوكس. سواء كان لديك أسئلة حول منتجاتنا، أو تحتاج إلى مساعدة في طلبك، أو تريد معرفة المزيد عن مكوناتنا الطبيعية، فريقنا المتخصص جاهز لمساعدتك.',
        '24/7 Customer Support': 'دعم العملاء على مدار الساعة',
        'Fast Response Time': 'وقت استجابة سريع',
        'Dedicated Care Team': 'فريق رعاية متخصص',
        'Visit Us': 'زورونا',
        'Call Us': 'اتصل بنا',
        'Mon-Fri: 9AM-6PM': 'الاثنين-الجمعة: ٩ص-٦م',
        'Email Us': 'راسلنا',
        'We\'ll respond within 24 hours': 'سنرد خلال ٢٤ ساعة',
        'Follow Us': 'تابعنا',
        'Send Us a Message': 'أرسل لنا رسالة',
        'Fill out the form below and we\'ll get back to you as soon as possible.': 'املأ النموذج أدناه وسنعود إليك في أقرب وقت ممكن.',
        'Your Name': 'اسمك',
        'Enter your full name': 'أدخل اسمك الكامل',
        'Your Email': 'بريدك الإلكتروني',
        'Enter your email address': 'أدخل عنوان بريدك الإلكتروني',
        'Subject': 'الموضوع',
        'What is your message about?': 'عن ماذا تتحدث رسالتك؟',
        'Message': 'الرسالة',
        'Type your message here...': 'اكتب رسالتك هنا...',
        'Send Message': 'إرسال الرسالة',
        'Sending...': 'جاري الإرسال...',
        'Common Questions': 'الأسئلة الشائعة',
        'What are your shipping times?': 'ما هي أوقات الشحن؟',
        'We typically process orders within 1-2 business days. Shipping times vary by location, usually 3-5 business days domestically.': 'نقوم عادةً بمعالجة الطلبات خلال ١-٢ يوم عمل. تختلف أوقات الشحن حسب الموقع، عادةً ٣-٥ أيام عمل داخل البلاد.',
        'Do you offer international shipping?': 'هل تقدمون الشحن الدولي؟',
        'Yes, we ship to most countries worldwide. International shipping times typically range from 7-14 business days.': 'نعم، نقوم بالشحن إلى معظم دول العالم. تتراوح أوقات الشحن الدولي عادةً من ٧-١٤ يوم عمل.',
        'What is your return policy?': 'ما هي سياسة الإرجاع؟',
        'We offer a 30-day satisfaction guarantee. If you\'re not completely satisfied, you can return unused products for a full refund.': 'نقدم ضمان رضا لمدة ٣٠ يوماً. إذا لم تكن راضياً تماماً، يمكنك إرجاع المنتجات غير المستخدمة واسترداد كامل المبلغ.',

        # Shop Page
        'Ramadan Collection': 'مجموعة رمضان',
        'Discover our special range of natural, premium products perfect for your self-care routine during the blessed month': 'اكتشف مجموعتنا الخاصة من المنتجات الطبيعية الفاخرة المثالية لروتين العناية الذاتية خلال الشهر الفضيل',
        'reviews': 'تقييمات',
        'Size': 'الحجم',

        # Product Details Page
        'Key Features': 'المميزات الرئيسية',
        '100% Natural Ingredients': 'مكونات طبيعية ١٠٠٪',
        'Eco-Friendly Packaging': 'عبوات صديقة للبيئة',
        'Dermatologically Tested': 'مختبر من قبل أطباء الجلد',
        'Cruelty-Free': 'خالٍ من التجارب على الحيوانات',
        'Shipping & Returns': 'الشحن والإرجاع',
        'Free shipping on orders over 1000 EGP': 'شحن مجاني للطلبات التي تزيد عن ١٠٠٠ جنيه',
        '30-day return policy': 'سياسة إرجاع لمدة ٣٠ يوماً',
        'Same-day dispatch': 'شحن في نفس اليوم',
        'You May Also Like': 'قد يعجبك أيضاً',
        'View Details': 'عرض التفاصيل',
        'Items Ordered': 'المنتجات المطلوبة',
        'Subtotal': 'المجموع الفرعي',

        # Product Ratings
        'reviews': 'تقييمات',
        'rating': 'تقييم',
        'ratings': 'تقييمات',
        
        # Quick View Modal
        'Quick View': 'نظرة سريعة',
        'Close': 'إغلاق',
        'Select Size': 'اختر الحجم',
        'Select Quantity': 'اختر الكمية',
        'In Stock': 'متوفر',
        'Low Stock': 'الكمية محدودة',
        'Out of Stock': 'نفذ من المخزون',

        # Product Sorting
        'Sort By': 'ترتيب حسب',
        'Price: Low to High': 'السعر: من الأقل إلى الأعلى',
        'Price: High to Low': 'السعر: من الأعلى إلى الأقل',
        'Newest First': 'الأحدث أولاً',
        'Most Popular': 'الأكثر شعبية',

        # Product Filters
        'Filter Products': 'تصفية المنتجات',
        'Price Range': 'نطاق السعر',
        'Categories': 'الفئات',
        'Apply Filters': 'تطبيق التصفية',
        'Clear Filters': 'مسح التصفية',
        'No products found': 'لم يتم العثور على منتجات',

        # Profile Page
        'Recent Orders': 'الطلبات الأخيرة',
        'Shipping Addresses': 'عناوين الشحن',
        'No shipping addresses found.': 'لم يتم العثور على عناوين شحن.',
        'Points': 'النقاط',
        'Orders': 'الطلبات',
        'Home': 'المنزل',
        'Billing': 'الفواتير',
        'Office': 'المكتب',
        'Thank You for Your Order!': 'شكراً لطلبك!',
        'Order': 'طلب',
        "We've received your order and will begin processing it right away.": "لقد استلمنا طلبك وسنبدأ في معالجته على الفور.",
        "You'll receive an email confirmation shortly with your order details.": "ستتلقى تأكيداً عبر البريد الإلكتروني قريباً مع تفاصيل طلبك.",
        'Order Details': 'تفاصيل الطلب',
        'Shipping Address': 'عنوان الشحن',
        'Payment Method': 'طريقة الدفع',
        'Cash on Delivery': 'الدفع عند الاستلام',
        'Please prepare exact change for the delivery person.': 'يرجى تجهيز المبلغ المضبوط لمندوب التوصيل.',
        'Shipping Method': 'طريقة الشحن',
        'Express Shipping': 'شحن سريع',
        'Standard Shipping': 'شحن قياسي',
        'Estimated delivery:': 'موعد التسليم المتوقع:',
        'Same day delivery': 'توصيل في نفس اليوم',
        '2-3 business days': '٢-٣ أيام عمل',
        'View Order History': 'عرض سجل الطلبات',
    }
}

def log_memory_usage():
    process = psutil.Process(os.getpid())
    app.logger.info(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if diff > 0.5:  # Log slow requests (>500ms)
        log_memory_usage()
        app.logger.warning(f"Slow request: {request.path} took {diff:.2f}s")
    return response

@app.before_request
def before_request():
    # Get language from URL parameter or session or default to English
    g.lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = g.lang
    
    # Set text direction based on language
    g.dir = 'rtl' if g.lang == 'ar' else 'ltr'

@app.context_processor
def utility_processor():
    def translate(text):
        if g.lang == 'en' or text not in TRANSLATIONS.get(g.lang, {}):
            return text
        return TRANSLATIONS[g.lang][text]
    return {'translate': translate, 'csrf_token': generate_csrf}

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return render_template('500.html'), 500

# Add OAuth error handler
@app.errorhandler(oauthlib.oauth2.rfc6749.errors.OAuth2Error)
def handle_oauth2_error(error):
    app.logger.error(f"OAuth2 error: {str(error)}")
    flash("An error occurred during authentication. Please try again.", "error")
    return redirect(url_for('login'))

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    verified = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_verification_token(self):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt='email-verification')

    @staticmethod
    def verify_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='email-verification', max_age=expiration)
            return email
        except:
            return None

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    size = db.Column(db.String(20))
    stock = db.Column(db.Integer, default=0)
    product_type = db.Column(db.String(50))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)
    total = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    try:
        cart_items = []
        total = 0
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(int(product_id))
                if product:
                    subtotal = product.price * quantity
                    total += subtotal
                    cart_items.append({
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'quantity': quantity,
                        'subtotal': subtotal,
                        'image_url': product.image_url,
                        'size': product.size
                    })
        
        return render_template('cart.html', 
                             cart_items=cart_items, 
                             total=total,
                             shipping_cost=0 if total >= 50 else 5)
                             
    except Exception as e:
        app.logger.error(f'Error displaying cart: {str(e)}')
        flash('Error displaying cart', 'error')
        return redirect(url_for('home'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        
        if not product_id:
            return jsonify({
                'status': 'error',
                'message': 'Product ID is required'
            }), 400
            
        if quantity <= 0:
            return jsonify({
                'status': 'error',
                'message': 'Please select a valid quantity'
            }), 400
        
        # Initialize cart if it doesn't exist
        if 'cart' not in session:
            session['cart'] = {}
        
        # Get product to verify it exists
        product = Product.query.get_or_404(int(product_id))
        
        # Add to cart
        current_cart = dict(session['cart'])  # Create a copy of the cart
        if str(product_id) in current_cart:
            current_cart[str(product_id)] += quantity
        else:
            current_cart[str(product_id)] = quantity
        
        # Update session
        session['cart'] = current_cart
        session.modified = True
        
        # Calculate cart total
        cart_total = sum(
            Product.query.get(int(pid)).price * qty 
            for pid, qty in session['cart'].items()
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Product added to cart successfully',
            'cart_count': sum(session['cart'].values()),
            'cart_total': cart_total
        })
        
    except Exception as e:
        app.logger.error(f'Error adding to cart: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Error adding product to cart'
        }), 500

@app.route('/update_cart', methods=['POST'])
def update_cart():
    try:
        product_id = str(request.form.get('product_id'))
        quantity = int(request.form.get('quantity', 0))
        
        app.logger.info(f'Updating cart - Product ID: {product_id}, New Quantity: {quantity}')
        
        if 'cart' not in session:
            session['cart'] = {}
            
        # Create a copy of the cart to modify
        cart = dict(session['cart'])
            
        if quantity > 0:
            cart[product_id] = quantity
            app.logger.info(f'Updated quantity to: {quantity}')
        else:
            cart.pop(product_id, None)
            app.logger.info('Removed product from cart')
            
        # Update the session with the modified cart
        session['cart'] = cart
        session.modified = True
        
        # Calculate new cart total
        cart_total = sum(
            Product.query.get(int(pid)).price * qty 
            for pid, qty in cart.items()
        )
        
        # For remove actions (quantity = 0), always redirect
        if quantity == 0:
            flash('Item removed from cart', 'success')
            return redirect(url_for('cart'))
            
        # For AJAX requests (quantity updates)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'success',
                'cart_count': sum(cart.values()),
                'cart_total': cart_total
            })
            
        # For non-AJAX requests
        flash('Cart updated successfully', 'success')
        return redirect(url_for('cart'))
            
    except Exception as e:
        app.logger.error(f'Error updating cart: {str(e)}')
        flash('Error updating cart', 'error')
        return redirect(url_for('cart'))

def send_order_confirmation(order):
    try:
        # Get order items and their details
        order_items = []
        for item in order.items:
            product = Product.query.get(item.product_id)
            order_items.append({
                'name': product.name,
                'quantity': item.quantity,
                'price': item.price / 30.90,
                'subtotal': (item.price * item.quantity) / 30.90
            })

        # Create the email message
        msg = Message(
            subject=f'Order Confirmation - Order #{order.id}',
            recipients=[current_user.email]
        )
        
        # Render the email template
        msg.html = render_template(
            'email/order_confirmation.html',
            order=order,
            items=order_items,
            user=current_user,
            shipping_address=order.shipping_address.split('\n')
        )
        
        # Send the email
        mail.send(msg)
        app.logger.info(f'Order confirmation email sent for order {order.id}')
        
    except Exception as e:
        app.logger.error(f'Error sending order confirmation email: {str(e)}')

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))

    cart_items = []
    total = 0
    for product_id, quantity in session['cart'].items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': subtotal,
                'image_url': product.image_url,
                'size': product.size
            })

    if request.method == 'POST':
        try:
            # Get form data
            shipping_data = {
                'firstName': request.form.get('firstName'),
                'lastName': request.form.get('lastName'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'address': request.form.get('address'),
                'apartment': request.form.get('apartment'),
                'city': request.form.get('city'),
                'landmark': request.form.get('landmark'),
                'shipping': request.form.get('shipping', 'standard')
            }

            # Calculate final total with shipping
            shipping_cost = 70 if shipping_data['shipping'] == 'express' else (0 if total * 30.90 >= 1000 else 50)
            final_total = (total * 30.90) + shipping_cost

            # Create order
            order = Order(
                user_id=current_user.id,
                total=final_total,
                status='pending',
                shipping_address=f"{shipping_data['firstName']} {shipping_data['lastName']}\n"
                               f"{shipping_data['address']}\n"
                               f"{shipping_data['apartment']}\n"
                               f"{shipping_data['city']}\n"
                               f"Landmark: {shipping_data['landmark']}\n"
                               f"Phone: {shipping_data['phone']}"
            )
            db.session.add(order)
            db.session.flush()  # Get the order ID

            # Create order items
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['id'],
                    quantity=item['quantity'],
                    price=item['price'] * 30.90
                )
                db.session.add(order_item)

            # Clear the cart
            session.pop('cart', None)
            
            # Commit the transaction
            try:
                db.session.commit()
                app.logger.info(f'Order {order.id} created successfully')
                
                # Send order confirmation email
                send_order_confirmation(order)
                
                return jsonify({
                    'status': 'success',
                    'redirect_url': url_for('order_success', order_id=order.id)
                })
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error committing order transaction: {str(e)}')
                return jsonify({'status': 'error', 'error': 'Failed to process order'}), 500

        except Exception as e:
            app.logger.error(f'Error processing checkout: {str(e)}')
            return jsonify({'status': 'error', 'error': 'Failed to process checkout'}), 500

    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/order_success')
@login_required
def order_success():
    order_id = request.args.get('order_id')
    if not order_id:
        flash('Invalid order', 'error')
        return redirect(url_for('home'))

    order = Order.query.get_or_404(order_id)
    
    # Verify the order belongs to the current user
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('home'))
    
    return render_template('order_success.html', order=order, Product=Product)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.verified:
                flash('Please verify your email address before logging in. Check your inbox for the verification link.', 'error')
                return redirect(url_for('login'))
            
            login_user(user)
            return redirect(url_for('home'))
        
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Here you would typically:
            # 1. Generate a reset token
            # 2. Send a password reset email
            # For now, we'll just show a success message
            flash('If an account exists with this email, you will receive password reset instructions.', 'success')
            return redirect(url_for('login'))
            
    return render_template('forgot_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirmPassword')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            terms = request.form.get('terms')
            
            app.logger.info(f'Registration attempt for email: {email}')
            
            # Validate form data
            if not all([email, password, confirm_password, first_name, last_name, terms]):
                missing_fields = [field for field, value in {
                    'email': email,
                    'password': password,
                    'confirmPassword': confirm_password,
                    'firstName': first_name,
                    'lastName': last_name,
                    'terms': terms
                }.items() if not value]
                app.logger.warning(f'Missing required fields: {", ".join(missing_fields)}')
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('register'))
            
            if password != confirm_password:
                app.logger.warning('Password mismatch during registration')
                flash('Passwords do not match', 'error')
                return redirect(url_for('register'))
            
            if len(password) < 8:
                app.logger.warning('Password too short during registration')
                flash('Password must be at least 8 characters long', 'error')
                return redirect(url_for('register'))
            
            if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
                app.logger.warning('Password does not meet complexity requirements')
                flash('Password must contain at least one letter and one number', 'error')
                return redirect(url_for('register'))
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                app.logger.warning(f'Registration attempt with existing email: {email}')
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            # Create new user
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                verified=False
            )
            user.set_password(password)
            
            # Generate verification token
            token = user.generate_verification_token()
            verification_url = url_for('verify_email', token=token, _external=True)
            
            try:
                # Send verification email
                msg = Message(
                    subject='Verify Your PureLuxe Account',
                    recipients=[email],
                    sender='support@pure-luxe.shop'
                )
                msg.html = render_template(
                    'email/verify_email.html',
                    user=user,
                    verification_url=verification_url,
                    now=datetime.now()
                )
                mail.send(msg)
                
                # Now add user to database
                db.session.add(user)
                db.session.commit()
                
                app.logger.info(f'New user registered successfully: {email}')
                # Store email in session for verification page
                session['verification_email'] = email
                return redirect(url_for('verification_pending'))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error sending verification email: {str(e)}')
                flash('An error occurred while sending the verification email. Please try again.', 'error')
                return redirect(url_for('register'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error during registration: {str(e)}')
            flash('An error occurred while creating your account. Please try again.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/verification_pending')
def verification_pending():
    email = session.get('verification_email')
    if not email:
        return redirect(url_for('register'))
    return render_template('verification_pending.html', email=email)

@app.route('/verify_email/<token>')
def verify_email(token):
    try:
        email = User.verify_token(token)
        if email is None:
            flash('Invalid or expired verification link', 'error')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('User not found', 'error')
            return redirect(url_for('login'))
        
        if user.verified:
            flash('Email already verified. Please login.', 'info')
            return redirect(url_for('login'))
        
        user.verified = True
        db.session.commit()
        
        # Store email in session for verification pending page
        session['verification_email'] = email
        
        # Redirect to verification success page
        return render_template('verification_success.html')
        
    except Exception as e:
        app.logger.error(f'Error during email verification: {str(e)}')
        flash('An error occurred during verification. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/resend_verification', methods=['POST'])
@login_required
def resend_verification():
    try:
        user = current_user
        if user.verified:
            return jsonify({'status': 'error', 'message': 'Email already verified'})

        # Generate new verification token
        token = user.generate_verification_token()
        verification_url = url_for('verify_email', token=token, _external=True)

        # Send verification email
        msg = Message(
            subject='Verify Your PureLuxe Account',
            recipients=[user.email],
            sender='support@pure-luxe.shop'
        )
        msg.html = render_template(
            'email/verify_email.html',
            user=user,
            verification_url=verification_url,
            now=datetime.now()
        )
        mail.send(msg)

        return jsonify({
            'status': 'success',
            'message': 'Verification email resent successfully'
        })

    except Exception as e:
        app.logger.error(f'Error resending verification email: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Error resending verification email'
        }), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    # Get user's orders
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_ordered.desc()).all()
    
    # Get user's addresses
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile.html', orders=orders, addresses=addresses)

@app.route('/add-address', methods=['POST'])
@login_required
def add_address():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['type', 'street', 'city', 'postal_code', 'country']
        if not all(field in data for field in required_fields):
            return jsonify({'error': translate('All fields are required')}), 400
            
        # Create new address
        address = Address(
            user_id=current_user.id,
            type=data['type'],
            street=data['street'],
            city=data['city'],
            postal_code=data['postal_code'],
            country=data['country']
        )
        
        # If this is the user's first address, make it default
        if not Address.query.filter_by(user_id=current_user.id).first():
            address.is_default = True
        
        db.session.add(address)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': translate('Address added successfully')
        })
        
    except Exception as e:
        app.logger.error(f'Error adding address: {str(e)}')
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'error': translate('An error occurred while adding the address')
        }), 500

@app.context_processor
def cart_count():
    if 'cart' in session:
        return {'cart_count': sum(session['cart'].values())}
    return {'cart_count': 0}

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
        'size': product.size
    })

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            
            if not all([name, email, subject, message]):
                flash('Please fill in all fields', 'error')
                return redirect(url_for('contact'))
            
            # Create email message to support
            support_msg = Message(
                subject=f'New Contact Form Submission: {subject}',
                sender=app.config['MAIL_USERNAME'],
                recipients=['support@pure-luxe.shop'],  # Your support email
                body=f'''New contact form submission:
                
From: {name}
Email: {email}
Subject: {subject}

Message:
{message}
'''
            )
            mail.send(support_msg)
            
            # Send confirmation email to user
            confirmation = Message(
                subject='Thank you for contacting PureLuxe',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                html=render_template(
                    'email/contact_confirmation.html',
                    name=name,
                    message=message
                )
            )
            mail.send(confirmation)
            
            
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            app.logger.error(f'Error sending contact form email: {str(e)}')
            flash('There was an error sending your message. Please try again later.', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # Verify current password
    if not check_password_hash(current_user.password_hash, current_password):
        return jsonify({
            'error': 'current_password',
            'message': translate('Current password is incorrect')
        }), 400

    # Update password
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    # Log the password change
    app.logger.info(f'Password changed for user {current_user.email}')

    return jsonify({'message': translate('Password updated successfully')}), 200

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == "ADMIN456" and password == "ADMIN45678":
            session['is_admin'] = True
            return redirect(url_for('admin_orders'))
        else:
            flash('Invalid credentials', 'error')
            
    return render_template('admin/login.html')

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.date_ordered.desc()).all()
    
    # Calculate statistics
    total_revenue = sum(order.total for order in orders)
    pending_orders = sum(1 for order in orders if order.status == 'pending')
    completed_orders = sum(1 for order in orders if order.status == 'completed')
    
    return render_template('admin/orders.html', 
                         orders=orders, 
                         Product=Product,
                         total_revenue=total_revenue,
                         pending_orders=pending_orders,
                         completed_orders=completed_orders)

def send_order_status_update(order, new_status):
    try:
        # Get order items and their details
        order_items = []
        for item in order.items:
            product = Product.query.get(item.product_id)
            order_items.append({
                'name': product.name,
                'quantity': item.quantity,
                'price': item.price / 30.90,
                'subtotal': (item.price * item.quantity) / 30.90
            })

        # Get the user
        user = User.query.get(order.user_id)
        
        status_messages = {
            'pending': 'Your order is being processed',
            'completed': 'Your order has been completed and is out for delivery',
            'cancelled': 'Your order has been cancelled'
        }

        # Create the email message
        msg = Message(
            subject=f'Order #{order.id} Status Update - {status_messages.get(new_status, "Status Updated")}',
            recipients=[user.email],
            sender='support@pure-luxe.shop'
        )
        
        # Render the email template
        msg.html = render_template(
            'email/order_status_update.html',
            order=order,
            items=order_items,
            user=user,
            new_status=new_status,
            status_message=status_messages.get(new_status, "Status Updated"),
            shipping_address=order.shipping_address.split('\n')
        )
        
        # Send the email
        mail.send(msg)
        app.logger.info(f'Order status update email sent for order {order.id}')
        
    except Exception as e:
        app.logger.error(f'Error sending order status update email: {str(e)}')

@app.route('/admin/update_order_status', methods=['POST'])
@admin_required
def update_order_status():
    try:
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        
        if not order_id or not new_status:
            return jsonify({'status': 'error', 'message': 'Missing required data'})
        
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'status': 'error', 'message': 'Order not found'})
        
        old_status = order.status
        order.status = new_status
        db.session.commit()
        
        # Send status update email
        if old_status != new_status:  # Only send email if status actually changed
            send_order_status_update(order, new_status)
        
        # Calculate updated statistics
        total_revenue = sum([order.total for order in Order.query.all()])
        pending_orders = Order.query.filter_by(status='pending').count()
        completed_orders = Order.query.filter_by(status='completed').count()
        
        app.logger.info(f'Successfully updated order {order_id} status to {new_status}')
        
        return jsonify({
            'status': 'success',
            'message': 'Order status updated successfully',
            'stats': {
                'total_revenue': "%.2f" % (total_revenue / 30.90),
                'pending_orders': pending_orders,
                'completed_orders': completed_orders
            }
        })
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating order status: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/clear_orders', methods=['POST'])
@admin_required
def clear_orders():
    try:
        # First delete all order items
        OrderItem.query.delete()
        
        # Then delete all orders
        Order.query.delete()
        
        # Commit the changes
        db.session.commit()
        
        flash('All orders have been cleared successfully', 'success')
        return redirect(url_for('admin_orders'))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error clearing orders: {str(e)}')
        flash('Error clearing orders', 'error')
        return redirect(url_for('admin_orders'))

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/test_email')
@login_required
def test_email():
    try:
        msg = Message(
            subject='Test - Verify Your PureLuxe Account',
            recipients=[current_user.email],
            sender='support@pure-luxe.shop'
        )
        msg.html = render_template(
            'email/verify_email.html',
            user=current_user,
            verification_url='http://example.com/verify',
            now=datetime.now()
        )
        
        mail.send(msg)
        return 'Verification email sent successfully!'
    except Exception as e:
        app.logger.error(f'Error sending test email: {str(e)}')
        return f'Error sending email: {str(e)}'

@app.route('/check_verification_status')
def check_verification_status():
    email = session.get('verification_email')
    if not email:
        return jsonify({'verified': False})
    
    user = User.query.filter_by(email=email).first()
    if user and user.verified:
        # Clear the verification email from session
        session.pop('verification_email', None)
        # Log the user in
        login_user(user)
        return jsonify({'verified': True})
    
    return jsonify({'verified': False})

# Add OAuth token storage model
class OAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    token = db.Column(db.JSON, nullable=False)

# Add after app configuration
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

# Create Google OAuth blueprint
google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    scope=['https://www.googleapis.com/auth/userinfo.email',
           'https://www.googleapis.com/auth/userinfo.profile',
           'openid'],
    offline=True,
    reprompt_consent=True,
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# Register the blueprint with a URL prefix
app.register_blueprint(google_bp, url_prefix='/login')

# Configure session for OAuth
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
    SESSION_TYPE='filesystem'
)

# Handle Google OAuth login
@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", "error")
        return False

    try:
        resp = blueprint.session.get("https://www.googleapis.com/oauth2/v3/userinfo")
        if not resp.ok:
            flash("Failed to fetch user info from Google.", "error")
            return False

        google_info = resp.json()
        google_user_id = str(google_info["sub"])  # Google uses 'sub' as the user ID
        email = google_info.get("email")

        if not email:
            flash("Failed to get email from Google.", "error")
            return False

        # First, try to find existing user
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create a new user
            user = User(
                email=email,
                first_name=google_info.get("given_name", ""),
                last_name=google_info.get("family_name", ""),
                verified=True  # Google users are automatically verified
            )
            # Set a random password
            password = secrets.token_urlsafe(16)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # This will assign an ID to the user

        # Now find or create the OAuth record
        oauth = OAuth.query.filter_by(
            provider="google",
            provider_user_id=google_user_id
        ).first()

        if not oauth:
            oauth = OAuth(
                provider="google",
                provider_user_id=google_user_id,
                token=token,
                user_id=user.id
            )
            db.session.add(oauth)
        else:
            oauth.token = token

        db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google.", "success")
        return False  # Disable Flask-Dance's default behavior

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in Google OAuth callback: {str(e)}")
        flash("An error occurred during Google sign in.", "error")
        return False

# Add Google login route
@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)
