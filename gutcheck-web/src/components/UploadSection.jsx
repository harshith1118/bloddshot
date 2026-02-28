import { motion } from 'framer-motion';

export default function UploadSection({ getRootProps, getInputProps, isDragActive }) {
  return (
    <section className="pb-12">
      <div className="max-w-xl mx-auto">
        {/* Upload Card */}
        <motion.div
          {...getRootProps()}
          whileHover={{ scale: 1.005 }}
          whileTap={{ scale: 0.998 }}
          className={`
            relative border-2 border-dashed rounded-xl p-10 text-center cursor-pointer
            transition-all duration-200
            ${isDragActive
              ? 'border-sky-500 bg-sky-50'
              : 'border-gray-200 bg-white hover:border-sky-400 hover:bg-gray-50'
            }
          `}
        >
          <input {...getInputProps()} />
          
          <div className="space-y-4">
            {/* Icon */}
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100">
              <svg className="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            
            {/* Text */}
            <div>
              <p className="text-base font-medium text-gray-900 mb-1">
                {isDragActive ? 'Drop your PDF' : 'Upload your blood test report'}
              </p>
              <p className="text-sm text-gray-500">
                {isDragActive ? 'Release to upload' : 'Drag & drop or click to browse'}
              </p>
            </div>
            
            {/* Details */}
            <div className="flex items-center justify-center gap-3 text-xs text-gray-500">
              <span>PDF</span>
              <span className="w-0.5 h-0.5 rounded-full bg-gray-300" />
              <span>Max 10MB</span>
              <span className="w-0.5 h-0.5 rounded-full bg-gray-300" />
              <span>~30 seconds</span>
            </div>
            
            {/* Button */}
            <button className="inline-flex items-center justify-center px-5 py-2 rounded-lg gradient-accent text-white text-sm font-medium shadow-subtle hover:shadow-card transition-shadow">
              Select File
            </button>
          </div>
        </motion.div>

        {/* How It Works - Compact Inline */}
        <div className="mt-10">
          <div className="grid grid-cols-3 gap-4">
            <Step number="1" title="Upload" description="Upload your PDF report" />
            <Step number="2" title="Analyze" description="AI analyzes biomarkers" />
            <Step number="3" title="Results" description="Get instant insights" />
          </div>
        </div>
      </div>
    </section>
  );
}

function Step({ number, title, description }) {
  return (
    <div className="text-center">
      <div className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-sky-100 text-sky-600 text-sm font-semibold mb-2">
        {number}
      </div>
      <h4 className="text-sm font-semibold text-gray-900">{title}</h4>
      <p className="text-xs text-gray-500 mt-0.5">{description}</p>
    </div>
  );
}
