// Simple icons as React components to avoid import issues
const SearchIcon = ({ className = "w-5 h-5" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" }, 
  React.createElement('circle', { cx: "11", cy: "11", r: "8" }),
  React.createElement('path', { d: "m21 21-4.35-4.35" })
);

const FileTextIcon = ({ className = "w-5 h-5" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('path', { d: "M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" }),
  React.createElement('polyline', { points: "14,2 14,8 20,8" }),
  React.createElement('line', { x1: "16", y1: "13", x2: "8", y2: "13" }),
  React.createElement('line', { x1: "16", y1: "17", x2: "8", y2: "17" }),
  React.createElement('polyline', { points: "10,9 9,9 8,9" })
);

const CheckCircleIcon = ({ className = "w-6 h-6 text-green-600" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('path', { d: "M22 11.08V12a10 10 0 1 1-5.93-9.14" }),
  React.createElement('polyline', { points: "22,4 12,14.01 9,11.01" })
);

const AlertCircleIcon = ({ className = "w-5 h-5 text-red-600" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('circle', { cx: "12", cy: "12", r: "10" }),
  React.createElement('line', { x1: "12", y1: "8", x2: "12", y2: "12" }),
  React.createElement('line', { x1: "12", y1: "16", x2: "12.01", y2: "16" })
);

const DownloadIcon = ({ className = "w-4 h-4" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('path', { d: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" }),
  React.createElement('polyline', { points: "7,10 12,15 17,10" }),
  React.createElement('line', { x1: "12", y1: "15", x2: "12", y2: "3" })
);

const BarChart3Icon = ({ className = "w-5 h-5 text-blue-600" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('path', { d: "M3 3v18h18" }),
  React.createElement('path', { d: "M18 17V9" }),
  React.createElement('path', { d: "M13 17V5" }),
  React.createElement('path', { d: "M8 17v-3" })
);

const BrainIcon = ({ className = "w-4 h-4" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('circle', { cx: "12", cy: "12", r: "10" }),
  React.createElement('circle', { cx: "12", cy: "10", r: "3" })
);

const GlobeIcon = ({ className = "w-4 h-4" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('circle', { cx: "12", cy: "12", r: "10" }),
  React.createElement('line', { x1: "2", y1: "12", x2: "22", y2: "12" }),
  React.createElement('path', { d: "M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" })
);

const ShieldIcon = ({ className = "w-4 h-4" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('path', { d: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" })
);

const ZapIcon = ({ className = "w-4 h-4" }) => React.createElement('svg', { className: className, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
  React.createElement('polygon', { points: "13,2 3,14 12,14 11,22 21,10 12,10 13,2" })
);

// Main Research Assistant Component
const ResearchAssistant = () => {
  const [query, setQuery] = React.useState('');
  const [isResearching, setIsResearching] = React.useState(false);
  const [sessionId, setSessionId] = React.useState(null);
  const [progress, setProgress] = React.useState({ step: '', percentage: 0 });
  const [result, setResult] = React.useState(null);
  const [error, setError] = React.useState('');
  const [stats, setStats] = React.useState(null);

  const exampleQueries = [
    "What are the environmental impacts of cryptocurrency mining?",
    "Latest developments in gene therapy for cancer treatment",
    "Economic implications of remote work trends post-pandemic",
    "AI's impact on cybersecurity: threats and opportunities",
    "Sustainable agriculture practices and food security challenges"
  ];

  const researchSteps = [
    { key: 'analyzing_query', label: 'Analyzing Query', icon: BrainIcon, color: 'text-purple-600' },
    { key: 'conducting_research', label: 'Conducting Research', icon: GlobeIcon, color: 'text-blue-600' },
    { key: 'fact_checking', label: 'Fact Checking', icon: ShieldIcon, color: 'text-green-600' },
    { key: 'synthesizing', label: 'Synthesizing', icon: ZapIcon, color: 'text-orange-600' },
    { key: 'generating_report', label: 'Generating Report', icon: FileTextIcon, color: 'text-indigo-600' }
  ];

  // Fetch stats on component mount
  React.useEffect(() => {
    fetchStats();
  }, []);

  // Poll for progress updates
  React.useEffect(() => {
    let interval;
    if (sessionId && isResearching) {
      interval = setInterval(checkProgress, 2000);
    }
    return () => clearInterval(interval);
  }, [sessionId, isResearching]);

  const fetchStats = async () => {
    try {
      const response = await fetch('/stats');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  const startResearch = async () => {
    if (!query.trim()) {
      setError('Please enter a research query');
      return;
    }

    setIsResearching(true);
    setError('');
    setResult(null);
    setProgress({ step: 'initializing', percentage: 0 });

    try {
      const response = await fetch('/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query.trim() })
      });

      const data = await response.json();
      setSessionId(data.session_id);
    } catch (err) {
      setError('Failed to start research: ' + err.message);
      setIsResearching(false);
    }
  };

  const checkProgress = async () => {
    if (!sessionId) return;

    try {
      const response = await fetch(`/research/${sessionId}`);
      const data = await response.json();

      if (data.progress) {
        setProgress(data.progress);
      }

      if (data.status === 'completed') {
        setResult(data);
        setIsResearching(false);
        fetchStats(); // Update stats after completion
      } else if (data.status === 'failed') {
        setError('Research failed: ' + (data.error || 'Unknown error'));
        setIsResearching(false);
      }
    } catch (err) {
      setError('Error checking progress: ' + err.message);
      setIsResearching(false);
    }
  };

  const downloadReport = () => {
    if (sessionId) {
      window.open(`/research/${sessionId}/download`, '_blank');
    }
  };

  const getCurrentStepInfo = () => {
    return researchSteps.find(step => 
      progress.step.includes(step.key.replace('_', ''))
    ) || researchSteps[0];
  };

  return React.createElement('div', { className: "min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50" },
    React.createElement('div', { className: "container mx-auto px-4 py-8 max-w-6xl" },
      // Header
      React.createElement('div', { className: "text-center mb-12" },
        React.createElement('div', { className: "flex items-center justify-center mb-6" },
          React.createElement('div', { className: "bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-full" },
            React.createElement(SearchIcon, { className: "w-8 h-8 text-white" })
          )
        ),
        React.createElement('h1', { className: "text-4xl font-bold text-gray-800 mb-4" }, "Multi-Agent Research Assistant"),
        React.createElement('p', { className: "text-xl text-gray-600 max-w-2xl mx-auto" },
          "AI-powered research using specialized agents for comprehensive analysis and fact-checking"
        )
      ),

      // Stats Bar
      stats && React.createElement('div', { className: "bg-white rounded-xl shadow-lg p-6 mb-8" },
        React.createElement('div', { className: "flex items-center justify-between" },
          React.createElement('div', { className: "flex items-center space-x-2" },
            React.createElement(BarChart3Icon),
            React.createElement('span', { className: "font-semibold text-gray-700" }, "System Stats")
          ),
          React.createElement('div', { className: "flex space-x-6 text-sm" },
            React.createElement('div', { className: "text-center" },
              React.createElement('div', { className: "font-bold text-2xl text-blue-600" }, stats.total_sessions),
              React.createElement('div', { className: "text-gray-500" }, "Total")
            ),
            React.createElement('div', { className: "text-center" },
              React.createElement('div', { className: "font-bold text-2xl text-green-600" }, stats.completed),
              React.createElement('div', { className: "text-gray-500" }, "Completed")
            ),
            React.createElement('div', { className: "text-center" },
              React.createElement('div', { className: "font-bold text-2xl text-orange-600" }, stats.in_progress),
              React.createElement('div', { className: "text-gray-500" }, "In Progress")
            ),
            React.createElement('div', { className: "text-center" },
              React.createElement('div', { className: "font-bold text-2xl text-purple-600" }, stats.success_rate),
              React.createElement('div', { className: "text-gray-500" }, "Success Rate")
            )
          )
        )
      ),

      // Main Research Interface
      React.createElement('div', { className: "bg-white rounded-xl shadow-xl p-8 mb-8" },
        // Query Input
        React.createElement('div', { className: "mb-6" },
          React.createElement('label', { className: "block text-sm font-medium text-gray-700 mb-2" }, "Research Query"),
          React.createElement('textarea', {
            value: query,
            onChange: (e) => setQuery(e.target.value),
            placeholder: "Enter your research question here...",
            className: "w-full h-32 p-4 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none resize-none text-lg",
            disabled: isResearching
          })
        ),

        // Example Queries
        React.createElement('div', { className: "mb-6" },
          React.createElement('p', { className: "text-sm font-medium text-gray-700 mb-3" }, "Quick Examples:"),
          React.createElement('div', { className: "flex flex-wrap gap-2" },
            exampleQueries.map((example, index) =>
              React.createElement('button', {
                key: index,
                onClick: () => setQuery(example),
                disabled: isResearching,
                className: "px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors disabled:opacity-50"
              }, example.slice(0, 50) + "...")
            )
          )
        ),

        // Research Button
        React.createElement('button', {
          onClick: startResearch,
          disabled: isResearching || !query.trim(),
          className: "w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center space-x-2"
        },
          isResearching ? [
              React.createElement('div', { key: 'spinner', className: "animate-spin rounded-full h-5 w-5 border-b-2 border-white" }),
              React.createElement('span', { key: 'text' }, "Researching...")
            ] : [
              React.createElement(SearchIcon, { key: 'icon' }),
              React.createElement('span', { key: 'text' }, "Start Research")
            ]
        )
      ),

      // Progress Display
      isResearching && React.createElement('div', { className: "bg-white rounded-xl shadow-lg p-6 mb-8" },
        React.createElement('div', { className: "mb-4" },
          React.createElement('div', { className: "flex items-center justify-between mb-2" },
            React.createElement('div', { className: "flex items-center space-x-2" },
              React.createElement(getCurrentStepInfo().icon, {
                className: `w-5 h-5 ${getCurrentStepInfo().color}`
              }),
              React.createElement('span', { className: "font-semibold text-gray-700" },
                getCurrentStepInfo().label
              )
            ),
            React.createElement('span', { className: "text-sm text-gray-500" }, progress.percentage + "%")
          ),
          React.createElement('div', { className: "w-full bg-gray-200 rounded-full h-3" },
            React.createElement('div', {
              className: "bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500",
              style: { width: `${progress.percentage}%` }
            })
          )
        ),

        // Step Progress
        React.createElement('div', { className: "flex justify-between mt-6" },
          researchSteps.map((step, index) => {
            const isCompleted = progress.percentage > (index + 1) * 20;
            const isCurrent = progress.step.includes(step.key.replace('_', ''));
            
            return React.createElement('div', { key: step.key, className: "flex flex-col items-center" },
              React.createElement('div', {
                className: `p-2 rounded-full mb-2 ${
                  isCompleted ? 'bg-green-100' : 
                  isCurrent ? 'bg-blue-100' : 'bg-gray-100'
                }`
              },
                React.createElement(step.icon, {
                  className: `w-4 h-4 ${
                    isCompleted ? 'text-green-600' :
                    isCurrent ? step.color : 'text-gray-400'
                  }`
                })
              ),
              React.createElement('span', {
                className: `text-xs text-center ${
                  isCompleted || isCurrent ? 'text-gray-700' : 'text-gray-400'
                }`
              }, step.label)
            );
          })
        )
      ),

      // Error Display
      error && React.createElement('div', { className: "bg-red-50 border border-red-200 rounded-lg p-4 mb-8" },
        React.createElement('div', { className: "flex items-center space-x-2" },
          React.createElement(AlertCircleIcon),
          React.createElement('span', { className: "text-red-800" }, error)
        )
      ),

      // Results Display
      result && React.createElement('div', { className: "bg-white rounded-xl shadow-lg p-8" },
        React.createElement('div', { className: "flex items-center justify-between mb-6" },
          React.createElement('div', { className: "flex items-center space-x-2" },
            React.createElement(CheckCircleIcon),
            React.createElement('h2', { className: "text-2xl font-bold text-gray-800" }, "Research Complete")
          ),
          React.createElement('button', {
            onClick: downloadReport,
            className: "flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          },
            React.createElement(DownloadIcon),
            React.createElement('span', null, "Download Report")
          )
        ),

        // Result Metadata
        React.createElement('div', { className: "bg-gray-50 rounded-lg p-4 mb-6" },
          React.createElement('div', { className: "grid grid-cols-1 md:grid-cols-3 gap-4 text-sm" },
            React.createElement('div', null,
              React.createElement('span', { className: "font-semibold text-gray-600" }, "Query:"),
              React.createElement('p', { className: "text-gray-800 mt-1" }, result.query)
            ),
            React.createElement('div', null,
              React.createElement('span', { className: "font-semibold text-gray-600" }, "Sources Consulted:"),
              React.createElement('p', { className: "text-gray-800 mt-1" }, result.metadata?.sources_consulted || 'N/A')
            ),
            React.createElement('div', null,
              React.createElement('span', { className: "font-semibold text-gray-600" }, "Report Length:"),
              React.createElement('p', { className: "text-gray-800 mt-1" }, (result.metadata?.report_length || 'N/A') + " characters")
            )
          )
        ),

        // Report Content
        React.createElement('div', { className: "prose max-w-none" },
          React.createElement('div', { className: "whitespace-pre-wrap text-gray-700 leading-relaxed" },
            result.report
          )
        )
      )
    )
  );
};

// Initialize the app
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    React.createElement(React.StrictMode, null,
      React.createElement(ResearchAssistant)
    )
  );
}