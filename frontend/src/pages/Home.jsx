import NavbarApp from '../components/Navbar';
import Footer from '../components/Footer';
import { Button } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import "../styles/Home.css"

function HomePage() {
    return (
        <div className="App d-flex flex-column min-vh-100">
            <header className="App-header" >
                <NavbarApp />
            </header>


            <div class="main justify-content-center">
                <main >
                    <div class="card" href="https://haltinaa.github.io/tochno_last/p4.html" >
                        <div class="row" >
                            <div class="card-body col-md-5" >
                                <h2>Server 1</h2>
                            </div>
                            <div class="card-body col-sm-2">
                                <p>ok: 12</p>
                            </div>
                            <div class="card-body col-sm-2">
                                <p>err: 0</p>
                            </div>
                            <div class="card-body col-sm-2">
                                <Button variant="outline-lime" href='../pages/Info.jsx'>see more</Button>{' '}
                            </div>
                        </div>

                    </div>
                    <div class="card" href="#" >
                        <div class="row" >
                            <div class="card-body col-md-5" >
                                <h2>Server 2</h2>
                            </div>
                            <div class="card-body col-sm-2">
                                <p>ok: 12</p>
                            </div>
                            <div class="card-body col-sm-2">
                                <p>err: 0</p>
                            </div>
                            <div class="card-body col-sm-2">
                                <Button variant="outline-secondary" href='../pages/Info.jsx'>see more</Button>{' '}
                            </div>
                        </div>

                    </div>


                </main>

            </div>
            
            <div className="flex-grow-1"></div>
            <Footer />
        </div>
    );
}

export default HomePage;
