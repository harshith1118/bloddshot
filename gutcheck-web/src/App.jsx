import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import Header from './components/Header';
import Hero from './components/Hero';
import UploadSection from './components/UploadSection';
import AnalysisResults from './components/AnalysisResults';
import Footer from './components/Footer';
import { analyzeBloodTestPDF } from './lib/api';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);
    setProgress(10);
    setProgressMessage('Reading PDF file...');
    
    try {
      setProgress(30);
      setProgressMessage('Uploading and extracting text...');
      
      setProgress(50);
      setProgressMessage('Analyzing with Mistral AI...');
      
      // Analyze with backend
      const result = await analyzeBloodTestPDF(file);
      
      setProgress(100);
      setProgressMessage('Analysis complete!');
      
      setTimeout(() => {
        setAnalysisResult(result);
        setIsLoading(false);
        setProgress(0);
        setProgressMessage('');
      }, 500);
      
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to analyze blood test. Please try again.');
      setIsLoading(false);
      setProgress(0);
      setProgressMessage('');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const resetAnalysis = () => {
    setAnalysisResult(null);
    setError(null);
    setProgress(0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <AnimatePresence mode="wait">
          {!analysisResult && !isLoading && (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Hero />
              <UploadSection
                getRootProps={getRootProps}
                getInputProps={getInputProps}
                isDragActive={isDragActive}
                onReset={resetAnalysis}
              />
            </motion.div>
          )}

          {isLoading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-20"
            >
              <div className="w-full max-w-md">
                <div className="mb-4 text-center">
                  <p className="text-lg font-medium text-gray-700">{progressMessage}</p>
                </div>
                <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
                  <motion.div
                    className="absolute inset-y-0 left-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
                <div className="mt-4 flex justify-center">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"
                  />
                </div>
              </div>
            </motion.div>
          )}

          {analysisResult && (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <AnalysisResults result={analysisResult} onNewAnalysis={resetAnalysis} />
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8 p-4 bg-red-50 border border-red-200 rounded-xl"
          >
            <p className="text-red-600">{error}</p>
          </motion.div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
