import HeroSection from '../../components/HeroSection';
import Layout from '../../layouts/TopNavbarLayout';

/**
 *
 * @return {*} Landing component
 */
function Landing() {
  return (
    <Layout className={'h-screen overflow-hidden'}>
      <HeroSection></HeroSection>
    </Layout>
  );
}

export default Landing;
