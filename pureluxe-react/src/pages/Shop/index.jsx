import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardMedia,
  Button,
  CircularProgress,
  IconButton,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import {
  FavoriteBorder,
  Favorite,
  ShoppingCart,
  FilterList,
  Search,
} from '@mui/icons-material';
import { fetchProducts } from '../../store/slices/productSlice';
import './Shop.css';

const Shop = () => {
  const dispatch = useDispatch();
  const { products, loading } = useSelector((state) => state.products);
  const [sortBy, setSortBy] = useState('featured');
  const [category, setCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);

  const toggleFavorite = (productId) => {
    setFavorites(prev => 
      prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    );
  };

  const filteredProducts = products
    ?.filter(product => 
      (category === 'all' || product.product_type.toLowerCase() === category) &&
      (product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
       product.description.toLowerCase().includes(searchQuery.toLowerCase()))
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'price-low':
          return a.price - b.price;
        case 'price-high':
          return b.price - a.price;
        case 'name':
          return a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
        <CircularProgress sx={{ color: 'var(--gold)' }} />
      </Box>
    );
  }

  return (
    <Box className="shop-container">
      <div className="pattern-background" />
      
      <Container maxWidth="xl">
        {/* Shop Header */}
        <Box className="shop-header">
          <Typography variant="h1" className="shop-title">
            Our Collection
          </Typography>
          <Typography variant="subtitle1" className="shop-subtitle">
            Discover our range of natural and luxurious products
          </Typography>
        </Box>

        {/* Filters and Search */}
        <Box className="filters-section">
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: <Search className="search-icon" />,
                }}
                className="search-field"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth variant="outlined" className="filter-select">
                <InputLabel>Category</InputLabel>
                <Select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  label="Category"
                >
                  <MenuItem value="all">All Products</MenuItem>
                  <MenuItem value="body wash">Body Care</MenuItem>
                  <MenuItem value="cleanser">Skin Care</MenuItem>
                  <MenuItem value="treatment">Treatments</MenuItem>
                  <MenuItem value="gift set">Gift Sets</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth variant="outlined" className="filter-select">
                <InputLabel>Sort By</InputLabel>
                <Select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  label="Sort By"
                >
                  <MenuItem value="featured">Featured</MenuItem>
                  <MenuItem value="price-low">Price: Low to High</MenuItem>
                  <MenuItem value="price-high">Price: High to Low</MenuItem>
                  <MenuItem value="name">Name</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Box>

        {/* Products Grid */}
        <Grid container spacing={4} className="products-grid">
          {filteredProducts?.map((product) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
              <Card className="product-card">
                <CardMedia
                  component="img"
                  image={`/images/products/${product.image_url}`}
                  alt={product.name}
                  className="product-image"
                />
                <CardContent className="product-content">
                  <Box className="product-header">
                    <Typography variant="h6" className="product-name">
                      {product.name}
                    </Typography>
                    <IconButton
                      className="favorite-button"
                      onClick={() => toggleFavorite(product.id)}
                    >
                      {favorites.includes(product.id) ? (
                        <Favorite className="favorite-icon active" />
                      ) : (
                        <FavoriteBorder className="favorite-icon" />
                      )}
                    </IconButton>
                  </Box>
                  <Typography variant="body2" className="product-description">
                    {product.description}
                  </Typography>
                  <Box className="product-meta">
                    <Typography variant="body2" className="product-size">
                      {product.size}
                    </Typography>
                    <Typography variant="body2" className="product-type">
                      {product.product_type}
                    </Typography>
                  </Box>
                  <Box className="product-footer">
                    <Typography variant="h6" className="product-price">
                      {product.price} EGP
                    </Typography>
                    <Button
                      variant="contained"
                      className="add-to-cart-button"
                      startIcon={<ShoppingCart />}
                      disabled={product.stock <= 0}
                    >
                      {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Shop; 