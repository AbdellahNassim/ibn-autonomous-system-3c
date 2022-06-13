import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Auth from './pages/Authentication';
import LandingPage from './pages/Landing';
import Dashboard from './pages/Dashboard';
import {AuthProvider, AuthGuard} from './utils/auth';

/**
 *
 * @return {*} App component
 */
function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path='/' element={ <LandingPage/> }/>
          <Route path="/login" element={ <Auth/>} />
          <Route path="/dashboard" element={
            <AuthGuard redirectTo="/login">
              <Dashboard/>
            </AuthGuard>
          }/>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
