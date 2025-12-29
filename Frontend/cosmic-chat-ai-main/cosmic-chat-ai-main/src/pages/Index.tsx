import { Helmet } from 'react-helmet-async';
import CosmicBackground from '@/components/CosmicBackground';
import ChatContainer from '@/components/ChatContainer';

const Index = () => {
  return (
    <>
      <Helmet>
        <title>Cosmic AI - Your Gateway to Infinite Knowledge</title>
        <meta 
          name="description" 
          content="Experience the next generation of AI conversation with Cosmic AI. Explore infinite knowledge with stunning visuals and seamless interactions." 
        />
      </Helmet>
      
      <div className="relative min-h-screen flex flex-col">
        {/* Cosmic background with parallax */}
        <CosmicBackground />
        
        {/* Chat interface */}
        <div className="relative z-10 flex-1 flex flex-col">
          <ChatContainer />
        </div>
      </div>
    </>
  );
};

export default Index;
