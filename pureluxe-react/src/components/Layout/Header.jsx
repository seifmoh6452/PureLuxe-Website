import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import {
  Badge,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material';
import {
  ShoppingCart,
  Person,
  Menu as MenuIcon
} from '@mui/icons-material';
import '../../styles/Header.css';

const Header = () => {
  const location = useLocation();
  const cartItems = useSelector((state) => state.cart.items);
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <header className="header">
      <nav className="navbar">
        <Link to="/" className="logo">
          <img src="/images/logo.svg" alt="PureLuxe" />
          <span className="brand-name">PureLuxe</span>
        </Link>

        <div className="nav-links">
          <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            Home
          </Link>
          <Link to="/shop" className={`nav-link ${location.pathname === '/shop' ? 'active' : ''}`}>
            Shop
          </Link>
          <Link to="/about" className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}>
            About
          </Link>
          <Link to="/contact" className={`nav-link ${location.pathname === '/contact' ? 'active' : ''}`}>
            Contact
          </Link>
        </div>

        <div className="nav-actions">
          <IconButton
            className="cart-icon"
            component={Link}
            to="/cart"
          >
            <Badge 
              badgeContent={cartItems?.length || 0}
              classes={{
                badge: 'cart-badge'
              }}
            >
              <ShoppingCart />
            </Badge>
          </IconButton>

          <Link to="/login" className="btn-outline">
            <Person />
            <span>Login</span>
          </Link>

          <IconButton
            className="mobile-menu-toggle"
            onClick={handleMenuClick}
            sx={{ display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
        </div>
      </nav>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        sx={{
          '& .MuiPaper-root': {
            backgroundColor: '#000',
            border: '1px solid #C6A664',
            borderRadius: '4px',
            minWidth: '200px'
          }
        }}
      >
        <MenuItem 
          component={Link} 
          to="/" 
          onClick={handleMenuClose}
          sx={{ color: '#C6A664' }}
        >
          Home
        </MenuItem>
        <MenuItem 
          component={Link} 
          to="/shop" 
          onClick={handleMenuClose}
          sx={{ color: '#C6A664' }}
        >
          Shop
        </MenuItem>
        <MenuItem 
          component={Link} 
          to="/about" 
          onClick={handleMenuClose}
          sx={{ color: '#C6A664' }}
        >
          About
        </MenuItem>
        <MenuItem 
          component={Link} 
          to="/contact" 
          onClick={handleMenuClose}
          sx={{ color: '#C6A664' }}
        >
          Contact
        </MenuItem>
      </Menu>
    </header>
  );
};

export default Header; 