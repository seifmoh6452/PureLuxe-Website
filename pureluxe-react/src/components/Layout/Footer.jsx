import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Typography,
  Link,
  IconButton,
  Stack,
} from '@mui/material';
import FacebookIcon from '@mui/icons-material/Facebook';
import InstagramIcon from '@mui/icons-material/Instagram';
import TwitterIcon from '@mui/icons-material/Twitter';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: 'transparent',
        color: 'var(--ramadan-gold)',
        py: 6,
        mt: 'auto',
        borderTop: '1px solid var(--ramadan-gold)',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography 
              variant="h6" 
              gutterBottom
              sx={{ 
                color: 'var(--ramadan-gold)',
                textShadow: '0 2px 10px rgba(198, 166, 100, 0.3)',
              }}
            >
              PURELUXE
            </Typography>
            <Typography variant="body2" sx={{ color: 'var(--ramadan-gold)' }}>
              Crafting pure, luxurious solutions for hair and skin care.
            </Typography>
            <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
              <IconButton 
                sx={{ 
                  color: 'var(--ramadan-gold)',
                  '&:hover': {
                    color: 'var(--ramadan-gold-light)',
                  },
                }}
                aria-label="Facebook"
              >
                <FacebookIcon />
              </IconButton>
              <IconButton 
                sx={{ 
                  color: 'var(--ramadan-gold)',
                  '&:hover': {
                    color: 'var(--ramadan-gold-light)',
                  },
                }}
                aria-label="Instagram"
              >
                <InstagramIcon />
              </IconButton>
              <IconButton 
                sx={{ 
                  color: 'var(--ramadan-gold)',
                  '&:hover': {
                    color: 'var(--ramadan-gold-light)',
                  },
                }}
                aria-label="Twitter"
              >
                <TwitterIcon />
              </IconButton>
            </Stack>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography 
              variant="h6" 
              gutterBottom
              sx={{ 
                color: 'var(--ramadan-gold)',
                textShadow: '0 2px 10px rgba(198, 166, 100, 0.3)',
              }}
            >
              Quick Links
            </Typography>
            <Link
              component={RouterLink}
              to="/shop"
              sx={{ 
                color: 'var(--ramadan-gold)',
                display: 'block',
                mb: 1,
                '&:hover': {
                  color: 'var(--ramadan-gold-light)',
                },
              }}
            >
              Shop
            </Link>
            <Link
              component={RouterLink}
              to="/about"
              sx={{ 
                color: 'var(--ramadan-gold)',
                display: 'block',
                mb: 1,
                '&:hover': {
                  color: 'var(--ramadan-gold-light)',
                },
              }}
            >
              About Us
            </Link>
            <Link
              component={RouterLink}
              to="/contact"
              sx={{ 
                color: 'var(--ramadan-gold)',
                display: 'block',
                mb: 1,
                '&:hover': {
                  color: 'var(--ramadan-gold-light)',
                },
              }}
            >
              Contact
            </Link>
            <Link
              component={RouterLink}
              to="/privacy"
              sx={{ 
                color: 'var(--ramadan-gold)',
                display: 'block',
                mb: 1,
                '&:hover': {
                  color: 'var(--ramadan-gold-light)',
                },
              }}
            >
              Privacy Policy
            </Link>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography 
              variant="h6" 
              gutterBottom
              sx={{ 
                color: 'var(--ramadan-gold)',
                textShadow: '0 2px 10px rgba(198, 166, 100, 0.3)',
              }}
            >
              Contact Us
            </Typography>
            <Typography variant="body2" paragraph sx={{ color: 'var(--ramadan-gold)' }}>
              Email: info@pureluxe.shop
            </Typography>
            <Typography variant="body2" paragraph sx={{ color: 'var(--ramadan-gold)' }}>
              Phone: +1 234 567 8900
            </Typography>
            <Typography variant="body2" sx={{ color: 'var(--ramadan-gold)' }}>
              Address: 123 Beauty Street
              <br />
              Luxury Lane, BT 12345
            </Typography>
          </Grid>
        </Grid>
        <Typography
          variant="body2"
          align="center"
          sx={{ 
            mt: 4, 
            color: 'var(--ramadan-gold)',
            opacity: 0.7 
          }}
        >
          © {new Date().getFullYear()} PURELUXE. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer; 