import { motion } from 'framer-motion';

interface CosmicLoaderProps {
  size?: 'sm' | 'md' | 'lg';
}

const CosmicLoader = ({ size = 'md' }: CosmicLoaderProps) => {
  const sizeMap = {
    sm: { container: 24, orb: 4, orbit: 8 },
    md: { container: 40, orb: 6, orbit: 14 },
    lg: { container: 56, orb: 8, orbit: 20 },
  };

  const { container, orb, orbit } = sizeMap[size];

  const getOrbitTransition = (i: number) => ({
    duration: 2 + i * 0.3,
    repeat: Infinity,
    ease: 'linear' as const,
  });

  const orbColors = [
    'bg-cosmic-cyan',
    'bg-cosmic-purple', 
    'bg-cosmic-pink',
  ];

  const glowColors = [
    '0 0 12px rgba(0, 212, 255, 0.8), 0 0 24px rgba(0, 212, 255, 0.4)',
    '0 0 12px rgba(155, 77, 255, 0.8), 0 0 24px rgba(155, 77, 255, 0.4)',
    '0 0 12px rgba(255, 107, 157, 0.8), 0 0 24px rgba(255, 107, 157, 0.4)',
  ];

  return (
    <div 
      className="relative flex items-center justify-center"
      style={{ width: container, height: container }}
    >
      {/* Central core */}
      <motion.div
        className="absolute rounded-full bg-gradient-to-br from-cosmic-cyan via-cosmic-purple to-cosmic-pink"
        style={{
          width: orb * 1.5,
          height: orb * 1.5,
          boxShadow: '0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(155, 77, 255, 0.4)',
        }}
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.8, 1, 0.8],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      {/* Orbiting particles */}
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="absolute"
          style={{
            width: container,
            height: container,
          }}
          animate={{ rotate: 360 }}
          transition={getOrbitTransition(i)}
          initial={{ rotate: i * 120 }}
        >
          <motion.div
            className={`absolute rounded-full ${orbColors[i]}`}
            style={{
              width: orb,
              height: orb,
              top: '50%',
              left: '50%',
              marginTop: -orb / 2,
              marginLeft: orbit,
              boxShadow: glowColors[i],
            }}
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.7, 1, 0.7],
            }}
            transition={{
              duration: 0.8 + i * 0.2,
              repeat: Infinity,
              ease: 'easeInOut',
              delay: i * 0.2,
            }}
          />
        </motion.div>
      ))}

      {/* Outer glow ring */}
      <motion.div
        className="absolute rounded-full border border-cosmic-cyan/30"
        style={{
          width: container * 0.9,
          height: container * 0.9,
        }}
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
    </div>
  );
};

export default CosmicLoader;
