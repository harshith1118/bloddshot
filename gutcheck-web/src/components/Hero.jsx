import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section className="py-12 md:py-16">
      <div className="max-w-4xl mx-auto text-center">
        {/* Logo/Brand */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl gradient-accent shadow-lg">
            <span className="text-2xl">🩸</span>
          </div>
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-gray-900 mb-4"
        >
          Your blood test,<br />
          <span className="text-sky-600">finally explained.</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="text-base text-gray-600 mb-8 max-w-xl mx-auto"
        >
          Upload your blood test report and get instant analysis powered by Mistral AI. 
          Clear explanations, no medical jargon.
        </motion.p>

        {/* Trust indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex items-center justify-center gap-4 text-xs text-gray-500 mb-10"
        >
          <div className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
            <span>HIPAA compliant</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-sky-500" />
            <span>Mistral Large 3</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
            <span>Results in ~30s</span>
          </div>
        </motion.div>

        {/* Trusted By Logos */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="border-t border-gray-100 pt-8"
        >
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-4">Uses technology from</p>
          <div className="flex items-center justify-center gap-8 opacity-50 grayscale">
            {/* Mistral Logo Placeholder */}
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-gray-800" />
              <span className="text-sm font-medium text-gray-600">Mistral AI</span>
            </div>
            {/* Hugging Face Style Logo */}
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-yellow-500" />
              <span className="text-sm font-medium text-gray-600">Hugging Face</span>
            </div>
            {/* AWS Style Logo */}
            <div className="flex items-center gap-2">
              <div className="w-6 h-4 rounded bg-orange-400" />
              <span className="text-sm font-medium text-gray-600">AWS</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
