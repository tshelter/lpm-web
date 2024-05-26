import React from 'react';
import "../styles/Footer.css";
import { Container } from 'react-bootstrap';

function Footer() {
    return (
        <footer>
            <Container>
            
                <div className="footer-bottom">
                    <div className="container">
                        <div className="d-flex flex-column flex-md-row align-items-center">
                            <div className="me-0 me-md-auto">
                                <a href="#">
                                    © 2024 Company Name
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </Container>
        </footer>
    );
}

export default Footer;