import { motion } from 'framer-motion';
import { useState } from 'react';

export default function AnalysisResults({ result, onNewAnalysis }) {
  const statusConfig = {
    GREEN: {
      bgColor: 'bg-green-50',
      borderColor: 'border-green-500',
      textColor: 'text-green-700',
      label: 'All Normal',
    },
    YELLOW: {
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-500',
      textColor: 'text-yellow-700',
      label: 'Review Needed',
    },
    RED: {
      bgColor: 'bg-red-50',
      borderColor: 'border-red-500',
      textColor: 'text-red-700',
      label: 'Action Required',
    },
  };

  const config = statusConfig[result.overall_status] || statusConfig.YELLOW;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="py-4"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">Your Results</h2>
        <button
          onClick={onNewAnalysis}
          className="text-sm text-gray-600 hover:text-gray-900 transition flex items-center gap-1.5"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4v16m8-8H4" />
          </svg>
          New Analysis
        </button>
      </div>

      {/* Overall Status */}
      <div className={`${config.bgColor} rounded-lg p-4 mb-6 border-l-4 ${config.borderColor}`}>
        <div className="flex items-start gap-3">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className={`text-xs font-semibold uppercase tracking-wider ${config.textColor}`}>
                {config.label}
              </span>
            </div>
            <p className="text-sm text-gray-700 leading-relaxed">{result.summary}</p>
          </div>
        </div>
      </div>

      {/* Biomarkers List */}
      <div className="mb-6">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Biomarkers ({result.biomarkers?.length || 0})
        </h3>
        <div className="space-y-2">
          {result.biomarkers?.map((biomarker, index) => (
            <BiomarkerCard key={index} biomarker={biomarker} index={index} />
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
        <p className="text-xs text-gray-500 leading-relaxed">
          <span className="font-medium">Note:</span> This analysis is for educational purposes only 
          and does not constitute medical advice. Please consult your healthcare provider for 
          medical concerns.
        </p>
      </div>
    </motion.div>
  );
}

function BiomarkerCard({ biomarker, index }) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const statusConfig = {
    NORMAL: { 
      bgColor: 'bg-white', 
      textColor: 'text-gray-600', 
      borderColor: 'border-gray-200', 
      label: 'Normal',
      indicator: 'bg-gray-300'
    },
    BORDERLINE: { 
      bgColor: 'bg-white', 
      textColor: 'text-yellow-700', 
      borderColor: 'border-yellow-300', 
      label: 'Borderline',
      indicator: 'bg-yellow-500'
    },
    CONCERN: { 
      bgColor: 'bg-white', 
      textColor: 'text-red-700', 
      borderColor: 'border-red-300', 
      label: 'Attention',
      indicator: 'bg-red-500'
    },
  };

  const config = statusConfig[biomarker.status?.toUpperCase()] || statusConfig.NORMAL;

  return (
    <div className={`rounded-lg border ${config.borderColor} ${config.bgColor} overflow-hidden`}>
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-3 cursor-pointer"
      >
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            {/* Status Indicator */}
            <div className={`w-2 h-2 rounded-full ${config.indicator} flex-shrink-0`} />
            
            {/* Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-0.5">
                <h4 className="text-sm font-medium text-gray-900 truncate">{biomarker.name}</h4>
                <span className={`text-xs px-2 py-0.5 rounded-full ${config.textColor} bg-gray-100 flex-shrink-0`}>
                  {config.label}
                </span>
              </div>
              <p className="text-xs text-gray-600">
                <span className="font-mono">{biomarker.value} {biomarker.unit}</span>
                <span className="mx-2 text-gray-300">•</span>
                <span className="text-gray-500">Ref: {biomarker.normal_range}</span>
              </p>
            </div>
          </div>
          
          {/* Expand Icon */}
          <svg 
            className={`w-4 h-4 text-gray-400 transition-transform flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      {isExpanded && (
        <div className="px-3 pb-3 border-t border-gray-100">
          <div className="pt-3 space-y-3">
            <div>
              <h5 className="text-xs font-semibold text-gray-700 mb-1">Explanation</h5>
              <p className="text-sm text-gray-600 leading-relaxed">{biomarker.explanation}</p>
            </div>
            
            {biomarker.recommendations?.length > 0 && (
              <div>
                <h5 className="text-xs font-semibold text-gray-700 mb-1">Recommendations</h5>
                <ul className="space-y-1">
                  {biomarker.recommendations.map((rec, i) => (
                    <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                      <span className="text-gray-400 mt-1">-</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
