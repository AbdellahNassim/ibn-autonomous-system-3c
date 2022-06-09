import HeroSection from '../../components/HeroSection';
import Layout from '../../layouts/Landing';

/**
 *
 * @return {*} Landing component
 */
function Landing() {
  return (
    <Layout className={'h-screen'}>
      <HeroSection></HeroSection>
    </Layout>
  );
}

export default Landing;
