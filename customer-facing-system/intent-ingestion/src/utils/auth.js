import * as React from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import jwtDecode from 'jwt-decode';

// creating a react context for saving auth state
const AuthContext = React.createContext(null);


/**
 * Authentication provider
 * @param {*} children components
 * @return {*}
 */
export function AuthProvider({children}) {
  /**
   * Allows to retrieve the current user
   * @return {*} user
   */
  const getCurrentUser = ()=>{
    const currentUserString = localStorage.getItem('user');
    return JSON.parse(currentUserString);
  };


  const [currentUser, setCurrentUser] = React.useState(getCurrentUser());

  /**
   * signIn function to allow changing the auth state
   * @param {*} userToken jwt token received from authenticator
   */
  const signIn= (userToken)=>{
    // decode the token and save it in local storage
    const user= JSON.stringify(jwtDecode(userToken));
    localStorage.setItem('user', user);
    setCurrentUser(user);
  };


  /**
   * Sign Out function to allow signing out user
   */
  const signOut = ()=>{
    localStorage.removeItem('user');
    setCurrentUser(null);
  };

  // create auth state
  const authState = {
    user: currentUser,
    signIn,
    signOut,
    getCurrentUser,
  };

  return (<AuthContext.Provider value={authState}>
    {children}
  </AuthContext.Provider>);
}

/**
 * useAuth function to be used to access the context
 * @return {*}
 */
export function useAuth() {
  return React.useContext(AuthContext);
}


/**
 * Authentication guard component
 * @param {*} redirectTo page
 * @return {*}
 */
export function AuthGuard({redirectTo, children}) {
  // get current auth state
  const auth = useAuth();
  // access the current location
  const location = useLocation();

  if (auth.user) {
    return children;
  } else {
    // when it is not logged in then it will be redirected
    // the current location is saved so that when logged in
    // it can be redirected to
    return <Navigate to={redirectTo} state={{from: location}} replace/>;
  }
}
