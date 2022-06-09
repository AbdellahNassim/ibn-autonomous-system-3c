
// eslint-disable-next-line valid-jsdoc
/**
 *
 * @return Return the login form component
 */
export default function LoginForm() {
  return (
    <div className="bg-primary-500 h-full flex flex-col items-center p-9">
      <div className="flex flex-col items-start mt-16">
        <h1 className=" text-5xl text-white-lighter mt-12">
            Hello ! Welcome Back
        </h1>
        <p className="text-center w-10/12 text-white-lighter mt-8 font-light">
          Login with the data you have already used when registering your account
        </p>
      </div>

      <div className=" flex flex-col w-full items-center justify-center h-full">
        <form className=" w-3/4">

          <div className="bg-white w-full pb-8 mb-4 flex flex-col">
            <div className="mb-4">
              <label className="block text-white-lighter text-lg font-bold mb-2" htmlFor="username">
                  Username
              </label>
              <input className="shadow appearance-none border rounded w-full py-2 px-3 text-white-lighter" id="username" type="text" placeholder="Username"/>
            </div>
            <div className="mb-6">
              <label className="block text-white-lighter text-lg font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input className="shadow appearance-none border border-red rounded w-full py-2 px-3 text-white-lighter mb-3" id="password" type="password" placeholder="******************"/>
              <p className=" text-black-default text-sm">Please choose a password.</p>
            </div>
            <div className="flex items-center justify-between">
              <button className=" bg-white-lighter hover:bg-blue-dark text-white font-bold py-2 px-4 rounded" type="button">
                Sign In
              </button>
              <a className="inline-block align-baseline font-bold text-lg text-white-lighter " href="#">
                Forgot Password?
              </a>
            </div>
          </div>
        </form>
      </div>

      <div>
        <p className="text-white-lighter">
          Copyright © 2022 L3I, Univ La Rochelle
        </p>
        <p className="text-white-lighter mt-2">
          <span className=" font-bold underline mr-2">Privacy policy </span> |  <span className=" ml-2 font-bold underline">Terms and Conditions </span>
        </p>


      </div>


    </div>
  );
}

