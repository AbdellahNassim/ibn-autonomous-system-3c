import Layout from '../../layouts/FullScreen';
import ScoringLogo from '../../assets/scoring_logo.png';
import LoginForm from '../../components/forms/LoginForm';
import ChisteraLogo from '../../assets/chistera.png';
import L3iLogo from '../../assets/l3i.png';
import BgCity from '../../assets/bg-city.jpg';
/**
 *
 * @return {*} Auth component
 */
function Auth() {
  return (
    <Layout className={'h-screen'}>
      <div className="flex flex-row h-full">
        <div className=" hidden md:w-4/6 sm:flex justify-center h-full items-center"
          style={{
            backgroundImage: `url(${BgCity})`,
          }}
        >
          <div className="flex flex-col w-3/5 rounded-2xl "
            style={{
              background: 'rgba(255, 255, 255, 0.18)',
              boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
              backdropFilter: 'blur(10px)',
              WebkitBackdropFilter: 'blur(10px)',
            }}
          >
            <div className=" flex flex-col items-center justify-center">
              <div className="w-64">
                <img src={ScoringLogo} alt="SCORING" />
              </div>
              <div className="mt-8 text-white-lighter text-center font-bold w-11/12 text-2xl">
                <p><span className=" text-primary-400">S</span>mart <span className=" text-primary-400">C</span>ollaborative c<span className=" text-primary-400">O</span>mputing, caching and netwo<span className=" text-primary-400">R</span>ing parad<span className=" text-primary-400">I</span>gm for <span className=" text-primary-400">N</span>ext <span className=" text-primary-400">G</span>eneration communication infrastructures</p>
              </div>
            </div>
            <div className="flex flex-col justify-end mt-16">
              <div className="flex-1 flex flex-row justify-center mb-12">
                <div className=" w-40 mr-8">
                  <img src={ChisteraLogo} />
                </div>
                <div className=" w-20">
                  <img src={L3iLogo} />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="w-full sm:w-2/6  ">
          <LoginForm></LoginForm>
        </div>
      </div>
    </Layout>
  );
}

export default Auth;
