import {Formik} from 'formik';
import adapters from '../../../adapters';
import {useAuth} from '../../../utils/auth';
import {useLocation, useNavigate} from 'react-router-dom';

// eslint-disable-next-line valid-jsdoc
/**
 *
 * @return Return the login form component
 */
export default function LoginForm() {
  // get auth global state
  const auth = useAuth();
  // get navigation utilities
  const navigate = useNavigate();
  // get also current location
  // the location will allow us to access the page user wanted to access
  // before being redirected to the login
  const location = useLocation();

  return (
    <div className="bg-primary-500 h-full flex flex-col items-center justify-between p-4  md:p-9">
      <div className="flex flex-col items-start justify-around mt-12 ">
        <h1 className=" text-2xl sm:text-3xl md:text-5xl text-white ">
            Hello ! Welcome Back
        </h1>
        <p className="text-center w-10/12 text-white mt-8 font-light">
          Login with the data you have already used when registering your account
        </p>
      </div>

      <div className=" flex flex-col w-full items-center justify-center h-full">

        <Formik
          initialValues={{username: '', password: ''}}
          validate={(values) => {
            const errors = {};
            if (!values.username) {
              errors.username = 'Username required';
            }
            if (!values.password) {
              errors.password = 'Password required';
            }
            return errors;
          }}
          onSubmit={async (values, {setSubmitting, setErrors} ) => {
            try {
              // login user
              const loginResponse = await adapters.loginUser(values.username, values.password);
              // get user token
              const userToken = loginResponse.data.token;
              // sign in user
              auth.signIn(userToken);
              setSubmitting(false);
              // check if the user is coming from another page
              // else redirect him to dashboard
              const from = location.state?.from?.pathname || '/dashboard';
              // redirect user
              navigate(from, {replace: true});
            } catch (error) {
              console.log(error);
              if (error.response.status===401) {
                setErrors({
                  loginStatus: 'Invalid Credentials',
                });
              } else {
                setErrors({
                  loginStatus: 'Invalid Credentials',
                });
                console.log('Unknown error occurred');
                setSubmitting(false);
              }
            }
          }}
        >{({
            values,
            errors,
            touched,
            handleChange,
            handleBlur,
            handleSubmit,
            isSubmitting,
          /* and other goodies */
          }) => (
            <form className=" w-3/4" onSubmit={handleSubmit}>
              <div className="w-full pb-8 mb-4 flex flex-col">
                <div className="mb-4">
                  <label className="block text-white text-lg font-bold mb-2" htmlFor="username">
                  Username
                  </label>
                  <input className="appearance-none rounded w-full py-2 px-3"
                    id="username"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.username}
                    type="text" placeholder="Username"/>
                  <p className=" text-slate-800 text-sm">{errors.username && touched.username && errors.username}</p>
                </div>
                <div className="mb-1">
                  <label className="block text-white text-lg font-bold mb-2" htmlFor="password">
                  Password
                  </label>
                  <input className="appearance-none border border-red rounded w-full py-2 px-3  mb-3"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.password}
                    id="password"
                    type="password"
                    placeholder="******************"/>
                  <p className=" text-slate-800 text-sm">{errors.password && touched.password && errors.password}</p>
                </div>
                <p className=" text-slate-800 text-sm mb-4">{errors.loginStatus ?errors.loginStatus: '' }</p>
                <div className="flex items-center justify-between">
                  <button className=" bg-white  text-slate-800 font-bold py-2 px-4 rounded"
                    disabled={isSubmitting}
                    type="submit">
                    Sign In
                  </button>
                  <a className="inline-block align-baseline font-bold text-lg text-white " href="#">
                    Forgot Password?
                  </a>
                </div>
              </div>
            </form>)}

        </Formik>

      </div>

      <div>
        <p className="text-white">
          Copyright © 2022 L3I, Univ La Rochelle
        </p>
        <p className="text-white mt-2">
          <span className=" cursor-pointer font-bold underline mr-2">Privacy policy </span> |  <span className="cursor-pointer ml-2 font-bold underline">Terms and Conditions </span>
        </p>


      </div>


    </div>
  );
}

