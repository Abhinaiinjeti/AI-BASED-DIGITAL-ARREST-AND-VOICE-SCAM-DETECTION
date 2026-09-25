import React, { useEffect, useState } from 'react';
import { 
  History, 
  Trash2, 
  Search, 
  ShieldCheck, 
  ShieldAlert, 
  Lock, 
  FileText, 
  Mic, 
  RefreshCw,
  FolderOpen
} from 'lucide-react';
import { fetchHistory, clearHistory } from '../api/client';

export default function HistoryPage() {
  const [historyItems, setHistoryItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [feedbackMsg, setFeedbackMsg] = useState('');

  const loadHistory = async () => {
    setIsLoading(true);
    try {
      const data = await fetchHistory(100);
      setHistoryItems(data);
    } catch (err) {
      setFeedbackMsg('Failed to load history audit log.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleClearHistory = async () => {
    if (!window.confirm('Are you sure you want to permanently purge the local analysis history?')) return;
    try {
      await clearHistory();
      setHistoryItems([]);
      setFeedbackMsg('History purged successfully.');
      setTimeout(() => setFeedbackMsg(''), 3000);
    } catch (err) {
      setFeedbackMsg('Failed to purge history.');
    }
  };

  // Filter items
  const filtered = historyItems.filter((item) => {
    const matchesRisk = riskFilter === 'ALL' || item.risk_level === riskFilter;
    const matchesQuery = 
      item.scam_category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.detected_language.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.input_type.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesRisk && matchesQuery;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider">
            <History className="w-4 h-4" />
            <span>LOCAL AUDIT TRAIL</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-100 mt-1">
            Analysis Session History
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Browse previous threat assessments recorded in the local privacy-first SQLite database.
          </p>
        </div>

        {historyItems.length > 0 && (
          <button
            onClick={handleClearHistory}
            className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-rose-950/80 hover:bg-rose-900 text-rose-300 border border-rose-500/40 text-xs font-mono transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Purge History</span>
          </button>
        )}
      </div>

      {/* Privacy Notice Banner */}
      <div className="p-4 rounded-xl glass-panel border border-emerald-500/30 flex items-start space-x-3 text-xs bg-emerald-950/20">
        <Lock className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
        <div className="text-slate-300 leading-relaxed">
          <span className="font-bold text-emerald-400">Zero-Sensitive-Data Logging Policy: </span>
          In accordance with cybersecurity privacy principles, this application does NOT save raw message 
          text transcripts or voice audio files in the database. Only metadata (timestamp, language, category, 
          risk score, and classification) is maintained locally for accountability.
        </div>
      </div>

      {feedbackMsg && (
        <div className="p-3 rounded-xl bg-cyan-950/80 border border-cyan-500/50 text-cyan-300 text-xs font-mono">
          {feedbackMsg}
        </div>
      )}

      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search category or language..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-950 text-slate-200 pl-9 pr-4 py-2 rounded-xl border border-slate-800 text-xs focus:outline-none focus:border-cyan-500 font-mono"
          />
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono w-full sm:w-auto justify-end">
          <span className="text-slate-400 text-[11px]">FILTER:</span>
          {['ALL', 'VERY HIGH', 'HIGH', 'SUSPICIOUS', 'LOW'].map((lvl) => (
            <button
              key={lvl}
              onClick={() => setRiskFilter(lvl)}
              className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition-all ${
                riskFilter === lvl
                  ? 'bg-cyan-950 text-cyan-300 border border-cyan-500/50'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {lvl}
            </button>
          ))}
        </div>
      </div>

      {/* Table Container */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        {isLoading ? (
          <div className="p-12 text-center text-slate-400 text-xs font-mono">
            <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-cyan-400" />
            Loading history records...
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-xs font-mono space-y-2">
            <FolderOpen className="w-8 h-8 text-slate-600 mx-auto" />
            <div>No matching analysis history records found.</div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                <tr>
                  <th className="p-3.5">ID / Timestamp</th>
                  <th className="p-3.5">Type</th>
                  <th className="p-3.5">Language</th>
                  <th className="p-3.5">Classification</th>
                  <th className="p-3.5">Scam Category</th>
                  <th className="p-3.5">Risk Level</th>
                  <th className="p-3.5 text-right">Risk Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80 text-slate-300">
                {filtered.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-900/50 transition-colors">
                    <td className="p-3.5 whitespace-nowrap">
                      <div className="text-slate-200 font-bold">#{item.id}</div>
                      <div className="text-[10px] text-slate-500">
                        {item.timestamp ? new Date(item.timestamp).toLocaleString() : 'N/A'}
                      </div>
                    </td>

                    <td className="p-3.5 whitespace-nowrap">
                      <span className="inline-flex items-center gap-1 text-[11px]">
                        {item.input_type === 'voice' ? (
                          <>
                            <Mic className="w-3.5 h-3.5 text-teal-400" />
                            <span>Voice</span>
                          </>
                        ) : (
                          <>
                            <FileText className="w-3.5 h-3.5 text-cyan-400" />
                            <span>Text</span>
                          </>
                        )}
                      </span>
                    </td>

                    <td className="p-3.5 whitespace-nowrap text-slate-200">
                      {item.detected_language}
                    </td>

                    <td className="p-3.5 whitespace-nowrap">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        item.classification === 'Scam'
                          ? 'bg-rose-950 text-rose-300 border border-rose-800'
                          : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                      }`}>
                        {item.classification}
                      </span>
                    </td>

                    <td className="p-3.5 whitespace-nowrap text-cyan-300">
                      {item.scam_category.replace(/_/g, ' ')}
                      {item.is_digital_arrest === 1 && (
                        <span className="ml-2 text-[9px] bg-rose-950 text-rose-400 px-1 py-0.5 rounded border border-rose-800">
                          DIGITAL ARREST
                        </span>
                      )}
                    </td>

                    <td className="p-3.5 whitespace-nowrap">
                      <span className={`text-[11px] font-bold ${
                        item.risk_level === 'VERY HIGH'
                          ? 'text-rose-400'
                          : item.risk_level === 'HIGH'
                          ? 'text-orange-400'
                          : item.risk_level === 'SUSPICIOUS'
                          ? 'text-amber-400'
                          : 'text-emerald-400'
                      }`}>
                        {item.risk_level}
                      </span>
                    </td>

                    <td className="p-3.5 whitespace-nowrap text-right font-bold text-slate-100">
                      {item.risk_score} / 100
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
}
