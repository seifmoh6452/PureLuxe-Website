import React from 'react';
import './Home.css'; // Importing the CSS file for styles

const Home = () => {
    return (
        <div className="home">
            <header className="shop-header">
                <h1>PureLuxe - Ramadan Kareem</h1>
                <p className="shop-subtitle">Discover our special range of natural, premium products perfect for your self-care routine during the blessed month</p>
            </header>
            <section className="features">
                <div className="features-grid">
                    {/* Example product card */}
                    <div className="feature-card">
                        <div className="feature-icon">
                            <i className="fas fa-leaf"></i>
                        </div>
                        <h3>Product Name</h3>
                        <p>Product Description</p>
                    </div>
                    {/* Add more product cards as needed */}
                </div>
            </section>
        </div>
    );
};

export default Home; 