import { motion } from 'framer-motion';

export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="border-t border-gray-100 py-8 bg-white"
    >
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          {/* Brand */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg gradient-accent flex items-center justify-center">
              <span className="text-sm">🩸</span>
            </div>
            <div>
              <p className="text-sm font-semibold text-gray-900">GutCheck</p>
              <p className="text-xs text-gray-500">© {currentYear}</p>
            </div>
          </div>
          
          {/* Links */}
          <div className="flex items-center gap-6 text-sm">
            <a href="#" className="text-gray-600 hover:text-gray-900 transition">
              Privacy
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition">
              Terms
            </a>
            <a href="mailto:hello@gutcheck.ai" className="text-gray-600 hover:text-gray-900 transition">
              Contact
            </a>
          </div>
          
          {/* Tech Stack */}
          <p className="text-xs text-gray-500">
            Powered by <span className="text-sky-600 font-medium">Mistral AI</span>
          </p>
        </div>
        
        {/* Disclaimer */}
        <div className="mt-6 pt-6 border-t border-gray-100 text-center">
          <p className="text-xs text-gray-400 max-w-2xl mx-auto">
            ⚕️ This analysis is for educational purposes only and does not constitute medical advice. 
            Always consult with a qualified healthcare provider for medical concerns.
          </p>
        </div>
      </div>
    </motion.footer>
  );
}
