import React, { useEffect, useState, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Grid,
  Typography,
  CircularProgress,
  Card,
  CardContent,
} from '@mui/material';
import { fetchFeaturedProducts } from '../../store/slices/productSlice';
import '../../styles/RamadanTheme.css';
import {
  LocalOffer,
  Star,
  LocalShipping,
  Nature,
  Recycling,
  Science,
  CardGiftcard,
  Percent,
  LocalMall,
} from '@mui/icons-material';
import './Home.css';

const Home = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { featuredProducts, loading } = useSelector((state) => state.products);
  const [countdown, setCountdown] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  });

  useEffect(() => {
    dispatch(fetchFeaturedProducts());
  }, [dispatch]);

  useEffect(() => {
    const ramadanEndDate = new Date('2024-04-09T19:00:00');

    const timer = setInterval(() => {
      const now = new Date();
      const difference = ramadanEndDate - now;

      if (difference > 0) {
        setCountdown({
          days: Math.floor(difference / (1000 * 60 * 60 * 24)),
          hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
          minutes: Math.floor((difference / 1000 / 60) % 60),
          seconds: Math.floor((difference / 1000) % 60)
        });
      }
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const features = useMemo(() => [
    {
      icon: <Nature />,
      title: '100% Natural',
      description: 'Made with carefully selected natural ingredients that nourish both hair and skin.'
    },
    {
      icon: <Recycling />,
      title: 'Eco-Friendly',
      description: 'Sustainable packaging and biodegradable formula for minimal environmental impact.'
    },
    {
      icon: <Science />,
      title: 'Science-Backed',
      description: 'Formulated with proven scientific principles for optimal pH balance.'
    }
  ], []);

  const specialOffers = useMemo(() => [
    {
      icon: <CardGiftcard />,
      title: 'Ramadan Gift Sets',
      description: 'Special gift packages perfect for Iftar gatherings and Eid celebrations'
    },
    {
      icon: <Percent />,
      title: 'Special Discounts',
      description: 'Enjoy up to 30% off on selected products throughout Ramadan'
    },
    {
      icon: <LocalMall />,
      title: 'Free Gift Wrapping',
      description: 'Complimentary luxury gift wrapping service for all orders'
    }
  ], []);

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          backgroundColor: '#000'
        }}
      >
        <CircularProgress sx={{ color: 'var(--ramadan-gold)' }} />
      </Box>
    );
  }

  return (
    <Box className="home-container">
      <div className="pattern-background" />
      
      {/* Hero Section */}
      <Container maxWidth="lg">
        <Box className="hero-section">
          <Typography variant="h3" className="arabic-text">
            رمضان كريم
          </Typography>
          <Typography variant="h1" className="main-title">
            Welcome to Our<br />
            Ramadan Collection
          </Typography>
          <Typography variant="subtitle1" className="subtitle">
            Discover our special Ramadan collection of natural care<br />
            products, perfect for your self-care routine during the<br />
            blessed month
          </Typography>

          {/* Countdown Timer */}
          <Box className="countdown-container">
            <Box className="countdown-box">
              <Typography variant="h4">{countdown.days}</Typography>
              <Typography variant="body2">Days</Typography>
            </Box>
            <Box className="countdown-box">
              <Typography variant="h4">{countdown.hours}</Typography>
              <Typography variant="body2">Hours</Typography>
            </Box>
            <Box className="countdown-box">
              <Typography variant="h4">{countdown.minutes}</Typography>
              <Typography variant="body2">Minutes</Typography>
            </Box>
            <Box className="countdown-box">
              <Typography variant="h4">{countdown.seconds}</Typography>
              <Typography variant="body2">Seconds</Typography>
            </Box>
          </Box>

          <Box className="cta-buttons">
            <Button
              variant="contained"
              className="shop-button"
              onClick={(e) => {
                e.preventDefault();
                const bestSellersSection = document.querySelector('.bestsellers-section');
                if (bestSellersSection) {
                  window.scrollTo({
                    top: bestSellersSection.offsetTop - 100,
                    behavior: 'smooth'
                  });
                }
              }}
            >
              Explore Collection
            </Button>
            <Button
              variant="outlined"
              className="offers-button"
              onClick={(e) => {
                e.preventDefault();
                const offersSection = document.querySelector('.offers-section');
                if (offersSection) {
                  window.scrollTo({
                    top: offersSection.offsetTop - 100,
                    behavior: 'smooth'
                  });
                }
              }}
            >
              View Special Offers
            </Button>
          </Box>
        </Box>

        {/* Special Ramadan Offers */}
        <Box className="section offers-section">
          <Typography variant="h2" className="section-title">
            Special Ramadan Offers
          </Typography>
          <Typography variant="subtitle1" className="section-subtitle">
            Celebrate this blessed month with our exclusive deals and packages
          </Typography>
          <Grid container spacing={4} className="offers-grid">
            <Grid item xs={12} md={4}>
              <Card className="offer-card">
                <CardContent>
                  <CardGiftcard className="card-icon" />
                  <Typography variant="h6">Ramadan Gift Sets</Typography>
                  <Typography variant="body2">
                    Luxurious gift sets perfect for Iftar gatherings and Eid celebrations
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card className="offer-card">
                <CardContent>
                  <Percent className="card-icon" />
                  <Typography variant="h6">Special Discounts</Typography>
                  <Typography variant="body2">
                    Enjoy up to 30% off on selected products throughout Ramadan
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card className="offer-card">
                <CardContent>
                  <LocalMall className="card-icon" />
                  <Typography variant="h6">Free Gift Wrapping</Typography>
                  <Typography variant="body2">
                    Complimentary luxury gift wrapping service for all orders
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>

        {/* Why Choose PureLuxe */}
        <Box className="section">
          <Typography variant="h2" className="section-title">
            Why Choose PureLuxe?
          </Typography>
          <Grid container spacing={4} className="features-grid">
            <Grid item xs={12} md={4}>
              <Card className="feature-card">
                <CardContent>
                  <Nature className="card-icon" />
                  <Typography variant="h6">100% Natural</Typography>
                  <Typography variant="body2">
                    Made with carefully selected natural ingredients that nourish both hair and skin
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card className="feature-card">
                <CardContent>
                  <Recycling className="card-icon" />
                  <Typography variant="h6">Eco-Friendly</Typography>
                  <Typography variant="body2">
                    Sustainable packaging and biodegradable formula for minimal environmental impact
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card className="feature-card">
                <CardContent>
                  <Science className="card-icon" />
                  <Typography variant="h6">Science-Backed</Typography>
                  <Typography variant="body2">
                    Formulated with proven scientific principles for optimal pH balance
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>

        {/* One Product, Double Benefits */}
        <Box className="section benefits-section">
          <Typography variant="h2" className="section-title">
            One Product, Double Benefits
          </Typography>
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Box className="benefits-box">
                <Typography variant="h5">For Your Hair</Typography>
                <ul className="benefits-list">
                  <li>Deep cleansing</li>
                  <li>Moisture balance</li>
                  <li>Strengthens roots</li>
                  <li>Prevents hair loss</li>
                  <li>Promotes healthy growth</li>
                </ul>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box className="benefits-box">
                <Typography variant="h5">For Your Skin</Typography>
                <ul className="benefits-list">
                  <li>Natural glow</li>
                  <li>Deep hydration</li>
                  <li>Even skin tone</li>
                  <li>Reduces fine lines</li>
                  <li>Anti-aging effect</li>
                </ul>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <img src="/images/products.png" alt="Product Benefits" className="benefits-image" />
            </Grid>
          </Grid>
        </Box>

        {/* Natural Ingredients */}
        <Box className="section">
          <Typography variant="h2" className="section-title">
            Natural Ingredients
          </Typography>
          <Grid container spacing={4} className="ingredients-grid">
            {[
              {
                name: 'Aloe Vera',
                description: 'Hydration & Soothing',
                image: '/images/ingredients/aloe-vera.png'
              },
              {
                name: 'Coconut Oil',
                description: 'Deep Nourishment',
                image: '/images/ingredients/coconut-oil.png'
              },
              {
                name: 'Chamomile',
                description: 'Calming',
                image: '/images/ingredients/chamomile.png'
              },
              {
                name: 'Tea Tree Oil',
                description: 'Purifying',
                image: '/images/ingredients/tea-tree.png'
              }
            ].map((ingredient) => (
              <Grid item xs={6} md={3} key={ingredient.name}>
                <Card className="ingredient-card">
                  <CardContent>
                    <img src={ingredient.image} alt={ingredient.name} />
                    <Typography variant="h6">{ingredient.name}</Typography>
                    <Typography variant="body2">{ingredient.description}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Customer Testimonials */}
        <Box className="section testimonials-section">
          <Typography variant="h2" className="section-title">
            What Our Customers Say
          </Typography>
          <Box className="testimonials-container">
            {[
              {
                text: "Amazing natural lip balm and skin care set! when I use it all season! I just like it in all season!",
                author: "Sara Ahmed",
                image: "/images/testimonials/user1.jpg"
              },
              {
                text: "Finally, a product that works for both my hair and body. Simplified my routine!",
                text: "John B.",
                image: "/images/testimonials/user2.jpg"
              },
              {
                text: "The eco-friendly packaging and natural ingredients make me feel good about my purchase.",
                author: "Maria T.",
                image: "/images/testimonials/user3.jpg"
              }
            ].map((testimonial, index) => (
              <Card className="testimonial-card" key={index}>
                <CardContent>
                  <Typography variant="body1" className="testimonial-text">
                    "{testimonial.text}"
                  </Typography>
                  <Box className="testimonial-author">
                    <img src={testimonial.image} alt={testimonial.author} />
                    <Typography variant="subtitle2">{testimonial.author}</Typography>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        </Box>

        {/* FAQ Section */}
        <Box className="section faq-section">
          <Typography variant="h2" className="section-title">
            Frequently Asked Questions
          </Typography>
          <Grid container spacing={4}>
            {[
              {
                question: "Is it suitable for all hair types?",
                answer: "Yes! Our formula is designed to work effectively on all hair types while being gentle enough for daily use."
              },
              {
                question: "How often should I use it?",
                answer: "For best results, use 2-3 times per week. The gentle formula won't strip your hair's natural oils."
              },
              {
                question: "Is it really non-toxic?",
                answer: "Absolutely! Our products are free from harsh chemicals and formulated with natural ingredients."
              },
              {
                question: "What makes it different?",
                answer: "Our unique blend of natural ingredients and scientific formulation provides double benefits for both hair and skin."
              }
            ].map((faq, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card className="faq-card">
                  <CardContent>
                    <Typography variant="h6" className="faq-question">
                      {faq.question}
                    </Typography>
                    <Typography variant="body2" className="faq-answer">
                      {faq.answer}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Best Sellers Section */}
        <Box className="section bestsellers-section">
          <Typography variant="h2" className="section-title">
            Our Best Sellers
          </Typography>
          <Typography variant="subtitle1" className="section-subtitle">
            Experience the perfect blend of nature and luxury with our most loved products
          </Typography>
          <Grid container spacing={4}>
            {featuredProducts.map((product) => (
              <Grid item xs={12} sm={6} md={3} key={product.id}>
                <Card className="bestseller-card">
                  <CardContent>
                    <img src={product.image} alt={product.name} />
                    <Typography variant="h6">{product.name}</Typography>
                    <Typography variant="body2">{product.description}</Typography>
                    <Typography className="price">${product.price}</Typography>
                    <Button
                      variant="contained"
                      className="shop-button"
                      onClick={() => navigate(`/product/${product.id}`)}
                    >
                      Shop Now
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Box>
  );
};

export default Home; 