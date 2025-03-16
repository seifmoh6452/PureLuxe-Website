import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGift, faPercentage, faBoxOpen, faLeaf, faRecycle, faFlask } from '@fortawesome/free-solid-svg-icons';

const PageWrapper = styled.div`
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(to bottom, #000, #1a1a1a);

  &::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('/images/ramadan/islamic-pattern.jpg');
    background-size: 600px;
    background-repeat: repeat;
    background-position: center;
    opacity: 0.2;
    z-index: 1;
    animation: patternFloat 60s linear infinite;
  }

  &::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.9) 100%);
    z-index: 2;
  }

  @keyframes patternFloat {
    0% {
      background-position: 0 0;
    }
    100% {
      background-position: 600px 600px;
    }
  }
`;

const Hero = styled.section`
  position: relative;
  padding-top: 2rem;
  padding-bottom: 3rem;
  z-index: 3;
  text-align: center;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('/images/ramadan/islamic-pattern.jpg');
    background-size: 400px;
    background-repeat: repeat;
    background-position: center;
    opacity: 0.15;
    z-index: -1;
    animation: patternFloatHero 40s linear infinite;
  }

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(0,0,0,0.8), rgba(0,0,0,0.5));
    z-index: -1;
  }

  @keyframes patternFloatHero {
    0% {
      background-position: 0 0;
    }
    100% {
      background-position: 400px 400px;
    }
  }
`;

const RamadanGreeting = styled.h2`
  font-size: 4rem;
  color: #C6A664;
  margin: 1rem 0;
  font-family: 'Noto Naskh Arabic', serif;
  text-align: center;
  background: linear-gradient(120deg, #C6A664, #E5B668);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  opacity: 0;
  animation: fadeInUp 1s forwards;
  animation-delay: 0.5s;

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const HeroTitle = styled.h1`
  font-size: 3.5rem;
  color: #fff;
  margin-bottom: 1rem;
  font-family: 'Cormorant Garamond', serif;
  opacity: 0;
  animation: fadeInUp 1s forwards;
  animation-delay: 0.7s;
`;

const HeroSubtitle = styled.p`
  font-size: 1.2rem;
  color: #E5E5E5;
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.8;
  font-family: 'Inter', sans-serif;
  opacity: 0;
  animation: fadeInUp 1s forwards;
  animation-delay: 0.9s;
`;

const Button = styled(Link)`
  display: inline-block;
  padding: 1rem 2rem;
  margin: 0.5rem;
  border-radius: 50px;
  text-decoration: none;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  transition: all 0.3s ease;
  opacity: 0;
  animation: fadeInUp 1s forwards;
  animation-delay: 1.1s;

  ${props => props.$primary ? `
    background: linear-gradient(120deg, #C6A664, #E5B668);
    color: #000;
    border: none;

    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(198, 166, 100, 0.3);
    }
  ` : `
    background: transparent;
    color: #C6A664;
    border: 2px solid #C6A664;

    &:hover {
      background: rgba(198, 166, 100, 0.1);
      transform: translateY(-3px);
    }
  `}
`;

const Container = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 3;
`;

const Section = styled.section`
  position: relative;
  z-index: 3;
  padding: 6rem 0;
  
  &:nth-child(even) {
    background: rgba(198, 166, 100, 0.05);
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-image: url('/images/ramadan/islamic-pattern.jpg');
      background-size: 500px;
      background-repeat: repeat;
      background-position: center;
      opacity: 0.05;
      z-index: -1;
      animation: patternFloatSection 50s linear infinite;
    }
  }

  @keyframes patternFloatSection {
    0% {
      background-position: 0 0;
    }
    100% {
      background-position: 500px 500px;
    }
  }
`;

const SectionTitle = styled.h2`
  font-size: 3rem;
  background: linear-gradient(120deg, #C6A664, #E5B668);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  margin-bottom: 1rem;
  font-family: 'Cormorant Garamond', serif;
`;

const SectionSubtitle = styled.p`
  font-size: 1.2rem;
  color: #E5E5E5;
  text-align: center;
  max-width: 800px;
  margin: 0 auto 3rem;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;
`;

const ProductsSection = styled.section`
  padding: 8rem 0;
  background: linear-gradient(45deg, #0a0a0a, #1a1a1a);
`;

const ProductsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 3rem;
  margin-top: 4rem;
`;

const ProductCard = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(198, 166, 100, 0.1);

  &:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba(198, 166, 100, 0.1);
    border-color: rgba(198, 166, 100, 0.3);
  }
`;

const ProductImage = styled.img`
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-bottom: 1px solid rgba(198, 166, 100, 0.1);
`;

const ProductContent = styled.div`
  padding: 2rem;
`;

const ProductTitle = styled.h3`
  font-size: 1.8rem;
  color: #C6A664;
  margin-bottom: 1rem;
  font-family: 'Cormorant Garamond', serif;
`;

const ProductPrice = styled.span`
  font-size: 1.4rem;
  color: #E5E5E5;
  display: block;
  margin-bottom: 1.5rem;
  font-family: 'Inter', sans-serif;
`;

const ProductDescription = styled.p`
  color: #999;
  margin-bottom: 2rem;
  line-height: 1.6;
`;

const CountdownContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 2rem 0;
  padding: 2rem;
  background: linear-gradient(45deg, rgba(198, 166, 100, 0.1), rgba(229, 182, 104, 0.1));
  border-radius: 15px;
  border: 1px solid rgba(198, 166, 100, 0.2);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);

  @media (max-width: 768px) {
    gap: 1rem;
    padding: 1rem;
    flex-wrap: wrap;
  }
`;

const CountdownItem = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
  padding: 1.5rem;
  background: linear-gradient(45deg, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.5));
  border-radius: 10px;
  border: 1px solid rgba(198, 166, 100, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(0);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(198, 166, 100, 0.2);
  }

  @media (max-width: 768px) {
    min-width: 100px;
    padding: 1rem;
  }
`;

const CountdownNumber = styled.span`
  font-size: 3rem;
  font-weight: 700;
  color: #C6A664;
  font-family: 'Cormorant Garamond', serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  background: linear-gradient(120deg, #C6A664, #E5B668);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;

  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const CountdownLabel = styled.span`
  font-size: 1rem;
  color: #E5E5E5;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-family: 'Inter', sans-serif;
`;

const CountdownMessage = styled.div`
  text-align: center;
  margin-top: 1rem;
  font-size: 1.5rem;
  color: #C6A664;
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  background: linear-gradient(120deg, #C6A664, #E5B668);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: fadeIn 1s ease-in;

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
`;

const FeatureCard = styled.div`
  background: rgba(198, 166, 100, 0.05);
  border: 1px solid rgba(198, 166, 100, 0.2);
  border-radius: 20px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    transform: translateY(-10px);
    border-color: #C6A664;
    box-shadow: 0 10px 30px rgba(198, 166, 100, 0.1);
  }
`;

const FeatureIcon = styled.div`
  font-size: 2.5rem;
  color: #C6A664;
  margin-bottom: 1.5rem;
`;

const FeatureTitle = styled.h3`
  font-size: 1.8rem;
  color: #C6A664;
  margin-bottom: 1rem;
  font-family: 'Cormorant Garamond', serif;
`;

const FeatureDescription = styled.p`
  color: #E5E5E5;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;
`;

const IngredientsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
`;

const IngredientCard = styled.div`
  position: relative;
  height: 400px;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(198, 166, 100, 0.2);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-10px);
    border-color: #C6A664;
    box-shadow: 0 10px 30px rgba(198, 166, 100, 0.1);
  }
`;

const IngredientImage = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url(${props => props.image});
  background-size: cover;
  background-position: center;
  transition: all 0.3s ease;

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.8) 100%);
  }

  ${IngredientCard}:hover & {
    transform: scale(1.1);
  }
`;

const IngredientContent = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem;
  z-index: 2;
`;

const IngredientName = styled.h4`
  font-size: 1.8rem;
  color: #C6A664;
  margin-bottom: 1rem;
  font-family: 'Cormorant Garamond', serif;
`;

const IngredientDescription = styled.p`
  color: #E5E5E5;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;
`;

const RamadanOffers = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
`;

const OfferCard = styled.div`
  background: rgba(198, 166, 100, 0.05);
  border: 1px solid rgba(198, 166, 100, 0.2);
  border-radius: 20px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    transform: translateY(-10px);
    border-color: #C6A664;
    box-shadow: 0 10px 30px rgba(198, 166, 100, 0.1);
  }
`;

const OfferIcon = styled.div`
  font-size: 3rem;
  color: #C6A664;
  margin-bottom: 1.5rem;
`;

const OfferTitle = styled.h3`
  font-size: 1.8rem;
  color: #C6A664;
  margin-bottom: 1rem;
  font-family: 'Cormorant Garamond', serif;
`;

const OfferDescription = styled.p`
  color: #E5E5E5;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;
`;

const FAQSection = styled(Section)`
  background: linear-gradient(45deg, rgba(198, 166, 100, 0.05), rgba(229, 182, 104, 0.05));
`;

const FAQContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const FAQItem = styled.div`
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  border: 1px solid rgba(198, 166, 100, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(198, 166, 100, 0.1);
    transform: translateX(5px);
  }
`;

const FAQQuestion = styled.h3`
  font-size: 1.2rem;
  color: #C6A664;
  margin-bottom: ${props => props.isOpen ? '1rem' : '0'};
  font-family: 'Inter', sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;

  &::after {
    content: '${props => props.isOpen ? '−' : '+'}';
    font-size: 1.5rem;
    color: #C6A664;
  }
`;

const FAQAnswer = styled.div`
  color: #E5E5E5;
  line-height: 1.6;
  font-size: 1rem;
  max-height: ${props => props.isOpen ? '500px' : '0'};
  opacity: ${props => props.isOpen ? '1' : '0'};
  overflow: hidden;
  transition: all 0.3s ease;
`;

const TestimonialsSection = styled.section`
  position: relative;
  z-index: 3;
  padding: 6rem 0;
  background: rgba(198, 166, 100, 0.05);
`;

const TestimonialsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
`;

const TestimonialCard = styled.div`
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(198, 166, 100, 0.2);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-10px);
    border-color: #C6A664;
  }
`;

const TestimonialText = styled.p`
  color: #E5E5E5;
  font-style: italic;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  font-family: 'Inter', sans-serif;
`;

const TestimonialAuthor = styled.div`
  color: #C6A664;
  font-weight: 500;
  font-family: 'Cormorant Garamond', serif;
`;

const Home = () => {
  const [days, setDays] = React.useState(0);
  const [hours, setHours] = React.useState(0);
  const [minutes, setMinutes] = React.useState(0);
  const [seconds, setSeconds] = React.useState(0);
  const [openFAQ, setOpenFAQ] = React.useState(null);

  const faqs = [
    {
      question: "What are your shipping times?",
      answer: "We typically process orders within 1-2 business days. Shipping times vary by location, usually 3-5 business days domestically."
    },
    {
      question: "Are your products suitable for all skin types?",
      answer: "Yes, our products are formulated to be gentle and suitable for all skin types. We use natural ingredients that are carefully selected to provide effective care without causing irritation."
    },
    {
      question: "Do you offer international shipping?",
      answer: "Yes, we offer international shipping to most countries. Shipping costs and delivery times vary by location. Please check our shipping policy for more details."
    },
    {
      question: "What is your return policy?",
      answer: "We offer a 30-day return policy for unopened products in their original packaging. If you're not satisfied with your purchase, please contact our customer service team."
    }
  ];

  const toggleFAQ = (index) => {
    setOpenFAQ(openFAQ === index ? null : index);
  };

  React.useEffect(() => {
    const calculateCountdown = () => {
      const ramadanEnd = new Date('2024-04-09T18:00:00');
      const now = new Date();
      const difference = ramadanEnd - now;

      if (difference > 0) {
        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((difference / 1000 / 60) % 60);
        const seconds = Math.floor((difference / 1000) % 60);

        setDays(days);
        setHours(hours);
        setMinutes(minutes);
        setSeconds(seconds);
      }
    };

    calculateCountdown();
    const timer = setInterval(calculateCountdown, 1000);

    return () => clearInterval(timer);
  }, []);

  const products = [
    {
      id: 1,
      image: '/images/products/PureLuxe Signature Cleanser.jpg',
      title: 'Signature Cleanser',
      price: '299 EGP',
      description: 'Our bestselling gentle cleanser enriched with natural oils'
    },
    {
      id: 2,
      image: '/images/products/PureLuxe Clarifying Cleanser.jpg',
      title: 'Clarifying Cleanser',
      price: '349 EGP',
      description: 'Deep cleansing formula with activated charcoal'
    },
    {
      id: 3,
      image: '/images/products/PureLuxe Family Size.jpg',
      title: 'Luxury Collection',
      price: '899 EGP',
      description: 'Complete skincare routine in one elegant package'
    }
  ];

  const features = [
    {
      icon: faLeaf,
      title: '100% Natural',
      description: 'Made with carefully selected natural ingredients that nourish both hair and skin'
    },
    {
      icon: faRecycle,
      title: 'Eco-Friendly',
      description: 'Sustainable packaging and biodegradable formula for minimal environmental impact'
    },
    {
      icon: faFlask,
      title: 'Science-Backed',
      description: 'Formulated with proven scientific principles for optimal pH balance'
    }
  ];

  const ingredients = [
    {
      id: 1,
      image: '/images/ingredients/aloe-vera.jpg',
      name: 'Aloe Vera',
      description: 'Natural healing and soothing properties'
    },
    {
      id: 2,
      image: '/images/ingredients/chamomile.jpg',
      name: 'Chamomile',
      description: 'Calming and anti-inflammatory benefits'
    },
    {
      id: 3,
      image: '/images/ingredients/coconut-oil.jpg',
      name: 'Coconut Oil',
      description: 'Deep moisturizing and nourishing'
    }
  ];

  const offers = [
    {
      icon: faGift,
      title: 'Ramadan Gift Sets',
      description: 'Luxurious gift sets perfect for Iftar gatherings and Eid celebrations'
    },
    {
      icon: faPercentage,
      title: 'Special Discounts',
      description: 'Enjoy up to 30% off on selected products throughout Ramadan'
    },
    {
      icon: faBoxOpen,
      title: 'Free Gift Wrapping',
      description: 'Complimentary luxury gift wrapping service for all orders'
    }
  ];

  const testimonials = [
    {
      text: 'The natural ingredients in PureLuxe products have transformed my skincare routine. My skin feels healthier than ever!',
      author: 'Sarah Ahmed'
    },
    {
      text: 'I love how these products are both halal and eco-friendly. The Ramadan gift set was perfect for my family.',
      author: 'Fatima Hassan'
    },
    {
      text: 'The quality is exceptional, and the customer service is outstanding. Highly recommend!',
      author: 'Mohammed Ali'
    }
  ];

  return (
    <PageWrapper>
      <Hero>
        <Container>
          <RamadanGreeting>رمضان كريم</RamadanGreeting>
          <HeroTitle>Discover Luxury Natural Care</HeroTitle>
          <HeroSubtitle>
            Indulge in our exclusive collection of premium natural skincare products,
            crafted with the finest ingredients for your ultimate self-care ritual
          </HeroSubtitle>
          
          <CountdownContainer>
            <CountdownItem>
              <CountdownNumber>{days}</CountdownNumber>
              <CountdownLabel>Days</CountdownLabel>
            </CountdownItem>
            <CountdownItem>
              <CountdownNumber>{hours}</CountdownNumber>
              <CountdownLabel>Hours</CountdownLabel>
            </CountdownItem>
            <CountdownItem>
              <CountdownNumber>{minutes}</CountdownNumber>
              <CountdownLabel>Minutes</CountdownLabel>
            </CountdownItem>
            <CountdownItem>
              <CountdownNumber>{seconds}</CountdownNumber>
              <CountdownLabel>Seconds</CountdownLabel>
            </CountdownItem>
          </CountdownContainer>
          <CountdownMessage>Ramadan has started!</CountdownMessage>
          <div style={{ textAlign: 'center', opacity: 0, animation: 'fadeInUp 1s forwards', animationDelay: '1.3s' }}>
            <Button to="/shop" $primary>
              Explore Collection
            </Button>
            <Button to="#special-offers">
              View Special Offers
            </Button>
          </div>
        </Container>
      </Hero>

      <Section>
        <Container>
          <SectionTitle>Special Ramadan Offers</SectionTitle>
          <SectionSubtitle>
            Celebrate this blessed month with our exclusive deals and packages
          </SectionSubtitle>
          <RamadanOffers>
            {offers.map((offer, index) => (
              <OfferCard key={index}>
                <OfferIcon>
                  <FontAwesomeIcon icon={offer.icon} />
                </OfferIcon>
                <OfferTitle>{offer.title}</OfferTitle>
                <OfferDescription>{offer.description}</OfferDescription>
              </OfferCard>
            ))}
          </RamadanOffers>
        </Container>
      </Section>

      <Section>
        <Container>
          <SectionTitle>Why Choose PureLuxe?</SectionTitle>
          <SectionSubtitle>
            Discover the perfect blend of nature and luxury in every product
          </SectionSubtitle>
          <FeaturesGrid>
            {features.map((feature, index) => (
              <FeatureCard key={index}>
                <FeatureIcon>
                  <FontAwesomeIcon icon={feature.icon} />
                </FeatureIcon>
                <FeatureTitle>{feature.title}</FeatureTitle>
                <FeatureDescription>{feature.description}</FeatureDescription>
              </FeatureCard>
            ))}
          </FeaturesGrid>
        </Container>
      </Section>

      <Section>
        <Container>
          <SectionTitle>Our Best Sellers</SectionTitle>
          <SectionSubtitle>
            Experience the perfect blend of nature and luxury with our most loved products
          </SectionSubtitle>
          <ProductsGrid>
            {products.map(product => (
              <ProductCard key={product.id}>
                <ProductImage src={product.image} alt={product.title} loading="lazy" />
                <ProductContent>
                  <ProductTitle>{product.title}</ProductTitle>
                  <ProductPrice>{product.price}</ProductPrice>
                  <ProductDescription>{product.description}</ProductDescription>
                  <Button to={`/shop/${product.id}`} $primary>
                    Shop Now
                  </Button>
                </ProductContent>
              </ProductCard>
            ))}
          </ProductsGrid>
        </Container>
      </Section>

      <Section>
        <Container>
          <SectionTitle>Natural Ingredients</SectionTitle>
          <SectionSubtitle>
            Only the finest natural ingredients selected for your skincare
          </SectionSubtitle>
          <IngredientsGrid>
            {ingredients.map(ingredient => (
              <IngredientCard key={ingredient.id}>
                <IngredientImage image={ingredient.image} />
                <IngredientContent>
                  <IngredientName>{ingredient.name}</IngredientName>
                  <IngredientDescription>{ingredient.description}</IngredientDescription>
                </IngredientContent>
              </IngredientCard>
            ))}
          </IngredientsGrid>
        </Container>
      </Section>

      <TestimonialsSection>
        <Container>
          <SectionTitle>Customer Stories</SectionTitle>
          <SectionSubtitle>
            Discover what our valued customers have to say about their PureLuxe experience
          </SectionSubtitle>
          <TestimonialsGrid>
            {testimonials.map((testimonial, index) => (
              <TestimonialCard key={index}>
                <TestimonialText>"{testimonial.text}"</TestimonialText>
                <TestimonialAuthor>- {testimonial.author}</TestimonialAuthor>
              </TestimonialCard>
            ))}
          </TestimonialsGrid>
        </Container>
      </TestimonialsSection>

      <FAQSection>
        <Container>
          <SectionTitle>Common Questions</SectionTitle>
          <SectionSubtitle>
            Find answers to frequently asked questions about our products and services
          </SectionSubtitle>
          <FAQContainer>
            {faqs.map((faq, index) => (
              <FAQItem key={index} onClick={() => toggleFAQ(index)}>
                <FAQQuestion isOpen={openFAQ === index}>{faq.question}</FAQQuestion>
                <FAQAnswer isOpen={openFAQ === index}>{faq.answer}</FAQAnswer>
              </FAQItem>
            ))}
          </FAQContainer>
        </Container>
      </FAQSection>
    </PageWrapper>
  );
};

export default Home;
