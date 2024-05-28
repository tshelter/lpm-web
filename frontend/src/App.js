import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home';
import Info from './pages/Info'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/" element={<Info />} />
      </Routes>
      
    </BrowserRouter>
  );
}

export default App;
