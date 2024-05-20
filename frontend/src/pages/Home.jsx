import NavbarApp from '../components/Navbar';
import Footer from '../components/Footer';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function HomePage() {
    return (
        <div className="App d-flex flex-column min-vh-100">
            <header className="App-header">
                <NavbarApp />
            </header>
            <main>

            </main>
            <div className="flex-grow-1"></div>
            <Footer />
        </div>
    );
}

export default HomePage;