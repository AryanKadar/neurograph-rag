import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
}

const ChatInput = ({ onSend, isLoading, disabled }: ChatInputProps) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (input.trim() && !isLoading && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [input]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative"
    >
      {/* Glow effect behind input */}
      <div className="absolute inset-0 bg-gradient-to-r from-cosmic-cyan/10 via-cosmic-purple/10 to-cosmic-pink/10 rounded-2xl blur-xl" />
      
      <div className="relative flex items-end gap-3 p-3 bg-card/80 backdrop-blur-xl border border-border/50 rounded-2xl shadow-lg">
        {/* Cosmic accent */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-px bg-gradient-to-r from-transparent via-cosmic-cyan/50 to-transparent" />
        
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Send a message across the cosmos..."
            disabled={isLoading || disabled}
            className="min-h-[44px] max-h-[150px] resize-none bg-muted/50 border-border/30 focus:border-cosmic-cyan/50 rounded-xl placeholder:text-muted-foreground/60 transition-all duration-200"
            rows={1}
          />
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={isLoading ? 'loading' : 'send'}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ duration: 0.15 }}
          >
            <Button
              onClick={handleSubmit}
              disabled={!input.trim() || isLoading || disabled}
              className="h-11 w-11 rounded-xl bg-gradient-to-br from-cosmic-cyan via-cosmic-purple to-cosmic-pink hover:opacity-90 disabled:opacity-40 transition-all duration-200 shadow-lg hover:shadow-cosmic-cyan/25"
              size="icon"
            >
              {isLoading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                >
                  <Sparkles className="w-5 h-5 text-foreground" />
                </motion.div>
              ) : (
                <Send className="w-5 h-5 text-foreground" />
              )}
            </Button>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default ChatInput;
