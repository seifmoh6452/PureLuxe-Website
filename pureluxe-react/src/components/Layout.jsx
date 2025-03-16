import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShoppingCart, faUser, faSearch, faGlobe } from '@fortawesome/free-solid-svg-icons';

const Header = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.95);
  border-bottom: 1px solid #C6A664;
`;

const Navbar = styled.nav`
  padding: 1rem 0;
`;

const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
`;

const Logo = styled(Link)`
  color: #C6A664;
  font-size: 1.5rem;
  font-weight: 600;
  font-family: 'Cormorant Garamond', serif;
  text-decoration: none;
`;

const NavLinks = styled.div`
  display: flex;
  align-items: center;
  gap: 2rem;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
`;

const NavLink = styled(Link)`
  color: #C6A664;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    color: #D4B36B;
  }
`;

const Actions = styled.div`
  display: flex;
  align-items: center;
  gap: 1.5rem;
`;

const IconButton = styled.button`
  color: #C6A664;
  font-size: 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  
  &:hover {
    color: #D4B36B;
  }
`;

const CartCount = styled.span`
  position: absolute;
  top: -8px;
  right: -8px;
  background: #C6A664;
  color: #000;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 50%;
  min-width: 18px;
  text-align: center;
`;

const Layout = ({ children }) => {
  const location = useLocation();

  return (
    <>
      <Header>
        <Navbar>
          <Container>
            <Logo to="/">PureLuxe</Logo>
            
            <NavLinks>
              <NavLink to="/" className={location.pathname === "/" ? "active" : ""}>
                Home
              </NavLink>
              <NavLink to="/shop" className={location.pathname === "/shop" ? "active" : ""}>
                Shop
              </NavLink>
              <NavLink to="/about" className={location.pathname === "/about" ? "active" : ""}>
                About
              </NavLink>
              <NavLink to="/contact" className={location.pathname === "/contact" ? "active" : ""}>
                Contact
              </NavLink>
            </NavLinks>

            <Actions>
              <IconButton>
                <FontAwesomeIcon icon={faSearch} />
              </IconButton>
              <IconButton>
                <FontAwesomeIcon icon={faUser} />
              </IconButton>
              <IconButton style={{ position: 'relative' }}>
                <FontAwesomeIcon icon={faShoppingCart} />
                <CartCount>0</CartCount>
              </IconButton>
              <IconButton>
                <FontAwesomeIcon icon={faGlobe} />
              </IconButton>
            </Actions>
          </Container>
        </Navbar>
      </Header>
      <main style={{ paddingTop: '80px' }}>
        {children}
      </main>
    </>
  );
};

export default Layout;
