import NavbarApp from './components/Navbar';
import Footer from './components/Footer';

function App() {
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

export default App;
