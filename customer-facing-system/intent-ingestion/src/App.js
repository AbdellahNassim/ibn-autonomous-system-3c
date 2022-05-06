import HeroSection from './components/HeroSection';
import Layout from './components/layout';
import WebChatWidget from './components/WebChat';

/**
 *
 * @return {*} App component
 */
function App() {
  return (
    <Layout>
      <HeroSection></HeroSection>
      <WebChatWidget></WebChatWidget>
    </Layout>
  );
}

export default App;
