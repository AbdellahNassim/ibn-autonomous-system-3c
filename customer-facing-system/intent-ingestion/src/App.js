import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Auth from './pages/Authentication';
import LandingPage from './pages/Landing';

/**
 *
 * @return {*} App component
 */
function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={ <LandingPage/> }/>
        <Route path="/login" element={ <Auth/>} />
      </Routes>
    </Router>
  );
}

export default App;
