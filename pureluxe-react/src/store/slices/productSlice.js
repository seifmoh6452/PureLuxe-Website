import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Sample data matching Flask products exactly
const sampleProducts = [
  {
    id: 1,
    name: 'PureLuxe Body Wash',
    description: 'Our classic body wash for daily use. Premium formula enriched with natural oils for gentle cleansing.',
    price: 129.00,
    image_url: 'PureLuxe Signature Cleanser.jpg',
    size: '250ml',
    stock: 50,
    product_type: 'Body Wash'
  },
  {
    id: 2,
    name: 'PureLuxe Clarifying Cleanser',
    description: 'Deep cleansing formula that removes impurities while maintaining skin balance. Perfect for all skin types.',
    price: 149.00,
    image_url: 'PureLuxe Clarifying Cleanser.jpg',
    size: '250ml',
    stock: 50,
    product_type: 'Cleanser'
  },
  {
    id: 3,
    name: 'PureLuxe Family Size',
    description: 'Generous family-sized packaging for extended use.',
    price: 249.00,
    image_url: 'PureLuxe Family Size.jpg',
    size: '500ml',
    stock: 40,
    product_type: 'Family Pack'
  },
  {
    id: 4,
    name: 'PureLuxe Gift Set',
    description: 'Luxurious gift set featuring our premium products. Perfect for special occasions.',
    price: 399.00,
    image_url: 'PureLuxe Gift Set.jpg',
    size: 'Set',
    stock: 30,
    product_type: 'Gift Set'
  },
  {
    id: 5,
    name: 'PureLuxe Hydration Boost',
    description: 'Intensive hydration formula for all skin types. Enriched with hyaluronic acid and natural moisturizers.',
    price: 169.00,
    image_url: 'PureLuxe Hydration Boost.jpg',
    size: '250ml',
    stock: 45,
    product_type: 'Hydrator'
  },
  {
    id: 6,
    name: 'PureLuxe Intensive Treatment',
    description: 'Advanced treatment for specific skin concerns. Concentrated formula with active ingredients.',
    price: 199.00,
    image_url: 'PureLuxe Intensive Treatment.jpg',
    size: '250ml',
    stock: 35,
    product_type: 'Treatment'
  },
  {
    id: 7,
    name: 'PureLuxe Sensitive Formula',
    description: 'Gentle formula specially designed for sensitive skin.',
    price: 159.00,
    image_url: 'PureLuxe Sensitive Formula.jpg',
    size: '200ml',
    stock: 40,
    product_type: 'Sensitive'
  }
];

export const fetchProducts = createAsyncThunk(
  'products/fetchProducts',
  async () => {
    // Simulating API call with sample data
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(sampleProducts);
      }, 1000);
    });
  }
);

export const fetchFeaturedProducts = createAsyncThunk(
  'products/fetchFeaturedProducts',
  async () => {
    // Simulating API call with featured products (Gift Set)
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(sampleProducts.filter(p => ['Gift Set'].includes(p.product_type)));
      }, 1000);
    });
  }
);

const productSlice = createSlice({
  name: 'products',
  initialState: {
    products: [],
    featuredProducts: [],
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(fetchFeaturedProducts.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchFeaturedProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.featuredProducts = action.payload;
      })
      .addCase(fetchFeaturedProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export default productSlice.reducer; 