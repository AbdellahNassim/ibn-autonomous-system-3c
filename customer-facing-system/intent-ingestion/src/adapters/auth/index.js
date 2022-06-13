import axios from 'axios';
/**
 * login function to send the credentials to the authenticator and check if valid
 * @param {*} username
 * @param {*} password
 */
export const loginUser = async (username, password)=> {
  // get authenticator host
  if (!('REACT_APP_CUSTOMER_AUTHENTICATOR' in process.env )) {
    console.log('An error occurred there is some environment variables that are not set ');
  } else {
    const response = await axios.post(process.env['REACT_APP_CUSTOMER_AUTHENTICATOR']+'/auth/login',
        {username: username, password: password});
    return response;
  }
};
