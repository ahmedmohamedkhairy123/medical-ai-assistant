import { useState } from 'react';
import axios from 'axios';
import { Activity, AlertTriangle, FileText, HeartPulse, Loader2, Stethoscope } from 'lucide-react';

function App() {
  const [symptoms, setSymptoms] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!symptoms.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      // Calling the Python Backend
      const response = await axios.post('http://127.0.0.1:8000/analyze', {
        description: symptoms
      });
      setResult(response.data);
    } catch (err) {
      setError('Failed to connect to the server. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 font-sans text-slate-900">
      <div className="max-w-3xl mx-auto space-y-8">

        {/* Header */}
        <header className="text-center space-y-2">
          <div className="flex items-center justify-center gap-3">
            <div className="p-3 bg-blue-600 rounded-full">
              <Activity className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-slate-800">AI Medical Assistant</h1>
          </div>
          <p className="text-slate-500">Advanced Symptom Analysis & Triage System</p>
        </header>

        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
          <div className="flex items-center gap-2 text-blue-700 font-medium">
            <Stethoscope className="w-5 h-5" />
            <h2>Describe Your Symptoms</h2>
          </div>
          <textarea
            className="w-full h-32 p-4 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none transition-all placeholder:text-slate-400"
            placeholder="e.g., I have a sharp pain in my chest, difficulty breathing, and sweating..."
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !symptoms}
            className="w-full py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all flex items-center justify-center gap-2 shadow-lg shadow-blue-200"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing with AI...
              </>
            ) : (
              'Run Diagnostic Analysis'
            )}
          </button>
          {error && (
            <div className="p-4 bg-red-50 text-red-600 rounded-lg flex items-center gap-2 text-sm">
              <AlertTriangle className="w-4 h-4" />
              {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6 animate-fade-in">
            {/* Disclaimer Banner */}
            <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-lg flex gap-3">
              <AlertTriangle className="w-6 h-6 text-amber-600 flex-shrink-0" />
              <p className="text-sm text-amber-800 font-medium leading-relaxed">
                {result.disclaimer}
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Disease Card */}
              <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                <div className="flex items-center gap-2 mb-3 text-purple-600">
                  <Activity className="w-5 h-5" />
                  <h3 className="font-semibold">Potential Condition</h3>
                </div>
                <p className="text-xl font-bold text-slate-800">{result.disease_name}</p>
              </div>

              {/* Treatment Card */}
              <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                <div className="flex items-center gap-2 mb-3 text-emerald-600">
                  <HeartPulse className="w-5 h-5" />
                  <h3 className="font-semibold">Suggested Actions</h3>
                </div>
                <p className="text-slate-700 leading-relaxed">{result.suggested_treatment}</p>
              </div>
            </div>

            {/* Analysis Card */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
              <div className="flex items-center gap-2 mb-3 text-blue-600">
                <FileText className="w-5 h-5" />
                <h3 className="font-semibold">Medical Reasoning</h3>
              </div>
              <p className="text-slate-600 leading-relaxed">{result.analysis_reasoning}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;