import Home from './components/Home';
import Footer from "./components/Footer";
import NavbarApp from "./components/Navbar";

function App() {
    return (
        <div className="d-flex flex-column min-vh-100">
            <NavbarApp/>
            <Home/>
            <div className="flex-grow-1"></div>
            <Footer/>
        </div>
    );
}

export default App;
