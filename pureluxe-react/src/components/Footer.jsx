import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

const FooterContainer = styled.footer`
  background: #000000;
  color: #E5E5E5;
  padding: 4rem 2rem 2rem;
  position: relative;
  z-index: 2;
  border-top: 1px solid #C6A664;
`;

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
`;

const FooterSection = styled.div`
  h3 {
    color: #C6A664;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    font-family: 'Mula', sans-serif;
  }

  p {
    color: #E5E5E5;
    opacity: 0.9;
  }
`;

const FooterLinks = styled.ul`
  list-style: none;
  padding: 0;
  
  li {
    margin-bottom: 1rem;
    
    a {
      color: #E5E5E5;
      text-decoration: none;
      transition: color 0.3s ease;
      font-family: 'Mula', sans-serif;
      font-size: 0.95rem;
      
      &:hover {
        color: #C6A664;
      }
    }
  }
`;

const FooterBottom = styled.div`
  text-align: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(198, 166, 100, 0.3);
  font-family: 'Mula', sans-serif;
  font-size: 0.9rem;
  color: #E5E5E5;
  opacity: 0.8;
`;

const ContactInfo = styled.div`
  margin-top: 1rem;
  line-height: 1.8;
  font-family: 'Mula', sans-serif;
  color: #E5E5E5;

  p {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    opacity: 0.9;
  }
`;

const Footer = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <FooterSection>
          <h3>Quick Links</h3>
          <FooterLinks>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/shop">Shop</Link></li>
            <li><Link to="/about">About Us</Link></li>
            <li><Link to="/contact">Contact</Link></li>
          </FooterLinks>
        </FooterSection>

        <FooterSection>
          <h3>Customer Service</h3>
          <FooterLinks>
            <li><Link to="/shipping">Shipping Information</Link></li>
            <li><Link to="/returns">Returns & Exchanges</Link></li>
            <li><Link to="/faq">FAQ</Link></li>
            <li><Link to="/privacy">Privacy Policy</Link></li>
          </FooterLinks>
        </FooterSection>

        <FooterSection>
          <h3>Contact Us</h3>
          <ContactInfo>
            <p>Email: info@pureluxe.com</p>
            <p>Phone: +20 123 456 789</p>
            <p>Address: Cairo, Egypt</p>
          </ContactInfo>
        </FooterSection>

        <FooterSection>
          <h3>About PureLuxe</h3>
          <p style={{ lineHeight: '1.8', fontFamily: 'Mula, sans-serif' }}>
            Discover our premium collection of natural beauty products. We believe in combining nature's finest ingredients with scientific innovation to create exceptional skincare solutions.
          </p>
        </FooterSection>
      </FooterContent>

      <FooterBottom>
        <p>&copy; {new Date().getFullYear()} PureLuxe. All rights reserved.</p>
      </FooterBottom>
    </FooterContainer>
  );
};

export default Footer;
