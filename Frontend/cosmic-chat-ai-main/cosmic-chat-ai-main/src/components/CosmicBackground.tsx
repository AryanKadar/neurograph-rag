import { useEffect, useRef, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Parallax, ParallaxProvider } from 'react-scroll-parallax';

interface Star {
  id: number;
  x: number;
  y: number;
  size: number;
  opacity: number;
  delay: number;
  duration: number;
}

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  color: string;
  delay: number;
}

const generateStars = (count: number): Star[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 2 + 1,
    opacity: Math.random() * 0.5 + 0.3,
    delay: Math.random() * 5,
    duration: Math.random() * 3 + 2,
  }));
};

const generateParticles = (count: number): Particle[] => {
  const colors = [
    'rgba(0, 212, 255, 0.6)',
    'rgba(155, 77, 255, 0.6)',
    'rgba(255, 107, 157, 0.5)',
    'rgba(255, 215, 0, 0.4)',
  ];
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 4 + 2,
    color: colors[Math.floor(Math.random() * colors.length)],
    delay: Math.random() * 8,
  }));
};

const StarField = ({ stars, speed }: { stars: Star[]; speed: number }) => (
  <Parallax speed={speed} className="absolute inset-0 pointer-events-none">
    {stars.map((star) => (
      <motion.div
        key={star.id}
        className="absolute rounded-full bg-cosmic-star"
        style={{
          left: `${star.x}%`,
          top: `${star.y}%`,
          width: star.size,
          height: star.size,
        }}
        animate={{
          opacity: [star.opacity, star.opacity * 2, star.opacity],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: star.duration,
          delay: star.delay,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
    ))}
  </Parallax>
);

const NebulaLayer = () => (
  <Parallax speed={-5} className="absolute inset-0 pointer-events-none">
    {/* Main nebula */}
    <motion.div
      className="absolute w-[800px] h-[800px] rounded-full blur-[120px] opacity-20"
      style={{
        background: 'radial-gradient(circle, rgba(155, 77, 255, 0.4) 0%, transparent 70%)',
        left: '10%',
        top: '20%',
      }}
      animate={{
        scale: [1, 1.1, 1],
        opacity: [0.15, 0.25, 0.15],
      }}
      transition={{
        duration: 15,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
    />
    {/* Secondary nebula */}
    <motion.div
      className="absolute w-[600px] h-[600px] rounded-full blur-[100px] opacity-15"
      style={{
        background: 'radial-gradient(circle, rgba(0, 212, 255, 0.3) 0%, transparent 70%)',
        right: '5%',
        bottom: '10%',
      }}
      animate={{
        scale: [1.1, 1, 1.1],
        opacity: [0.1, 0.2, 0.1],
      }}
      transition={{
        duration: 12,
        repeat: Infinity,
        ease: 'easeInOut',
        delay: 2,
      }}
    />
    {/* Accent nebula */}
    <motion.div
      className="absolute w-[400px] h-[400px] rounded-full blur-[80px] opacity-10"
      style={{
        background: 'radial-gradient(circle, rgba(255, 107, 157, 0.4) 0%, transparent 70%)',
        left: '50%',
        top: '60%',
        transform: 'translate(-50%, -50%)',
      }}
      animate={{
        scale: [1, 1.2, 1],
        x: [0, 30, 0],
      }}
      transition={{
        duration: 20,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
    />
  </Parallax>
);

const FloatingParticles = ({ particles }: { particles: Particle[] }) => (
  <Parallax speed={15} className="absolute inset-0 pointer-events-none">
    {particles.map((particle) => (
      <motion.div
        key={particle.id}
        className="absolute rounded-full"
        style={{
          left: `${particle.x}%`,
          top: `${particle.y}%`,
          width: particle.size,
          height: particle.size,
          background: particle.color,
          boxShadow: `0 0 ${particle.size * 2}px ${particle.color}`,
        }}
        animate={{
          y: [0, -30, 0],
          x: [0, Math.random() > 0.5 ? 15 : -15, 0],
          opacity: [0.4, 0.8, 0.4],
        }}
        transition={{
          duration: 8 + Math.random() * 4,
          delay: particle.delay,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
    ))}
  </Parallax>
);

const GalaxySpiral = () => (
  <Parallax speed={-10} className="absolute inset-0 pointer-events-none overflow-hidden">
    <motion.div
      className="absolute w-[300px] h-[300px] opacity-10"
      style={{
        right: '15%',
        top: '25%',
        background: `
          conic-gradient(from 0deg at 50% 50%, 
            transparent 0deg, 
            rgba(155, 77, 255, 0.3) 60deg, 
            transparent 120deg,
            rgba(0, 212, 255, 0.2) 180deg,
            transparent 240deg,
            rgba(255, 107, 157, 0.2) 300deg,
            transparent 360deg
          )
        `,
        borderRadius: '50%',
        filter: 'blur(30px)',
      }}
      animate={{
        rotate: [0, 360],
        scale: [0.9, 1.1, 0.9],
      }}
      transition={{
        rotate: { duration: 60, repeat: Infinity, ease: 'linear' },
        scale: { duration: 10, repeat: Infinity, ease: 'easeInOut' },
      }}
    />
  </Parallax>
);

const CosmicBackground = () => {
  const distantStars = useMemo(() => generateStars(100), []);
  const mediumStars = useMemo(() => generateStars(60), []);
  const closeStars = useMemo(() => generateStars(30), []);
  const particles = useMemo(() => generateParticles(20), []);

  return (
    <div className="fixed inset-0 overflow-hidden bg-background">
      {/* Base gradient */}
      <div 
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(ellipse at 50% 0%, hsl(270, 50%, 8%) 0%, hsl(240, 30%, 4%) 50%, hsl(240, 20%, 3%) 100%)',
        }}
      />
      
      <ParallaxProvider>
        {/* Distant layer - slow movement */}
        <StarField stars={distantStars} speed={-30} />
        
        {/* Nebulae layer */}
        <NebulaLayer />
        
        {/* Galaxy spiral */}
        <GalaxySpiral />
        
        {/* Medium layer */}
        <StarField stars={mediumStars} speed={-15} />
        
        {/* Close layer - fast movement */}
        <StarField stars={closeStars} speed={-5} />
        
        {/* Floating particles - foreground */}
        <FloatingParticles particles={particles} />
      </ParallaxProvider>

      {/* Vignette overlay */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at 50% 50%, transparent 0%, hsl(240, 20%, 3%) 100%)',
          opacity: 0.6,
        }}
      />
    </div>
  );
};

export default CosmicBackground;
