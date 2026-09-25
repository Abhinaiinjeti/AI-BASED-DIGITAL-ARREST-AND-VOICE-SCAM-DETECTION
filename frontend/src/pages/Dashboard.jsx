import React, { useEffect, useState } from 'react';
import { 
  BarChart3, 
  ShieldAlert, 
  AlertTriangle, 
  FileText, 
  Mic, 
  Activity, 
  Database,
  RefreshCw,
  FolderOpen
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell, 
  Legend 
} from 'recharts';
import { fetchStatistics } from '../api/client';

export default function Dashboard({ setActiveTab }) {
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  const loadStats = async () => {
    setIsLoading(true);
    setErrorMsg('');
    try {
      const data = await fetchStatistics();
      setStats(data);
    } catch (err) {
      setErrorMsg(err.message || 'Failed to load dashboard data.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const COLORS = ['#06B6D4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#3B82F6'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider">
            <BarChart3 className="w-4 h-4" />
            <span>REAL-TIME APPLICATION TELEMETRY</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-100 mt-1">
            Cyber Threat Intelligence Dashboard
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Aggregated statistics derived strictly from real user sessions recorded in the local SQLite database.
          </p>
        </div>

        <button
          onClick={loadStats}
          disabled={isLoading}
          className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs font-mono transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-cyan-400 ${isLoading ? 'animate-spin' : ''}`} />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {isLoading ? (
        <div className="p-16 text-center space-y-3 glass-panel rounded-2xl border border-slate-800">
          <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <div className="text-xs font-mono text-slate-400">Loading verified session analytics...</div>
        </div>
      ) : !stats || !stats.has_data || stats.total_analyses === 0 ? (
        /* Explicit Empty State - Directive 11 Compliance (No Fake Data) */
        <div className="p-16 text-center space-y-4 glass-panel rounded-2xl border border-slate-800/80 max-w-xl mx-auto">
          <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-500 mx-auto">
            <FolderOpen className="w-8 h-8 text-cyan-500/70" />
          </div>
          <h3 className="text-lg font-bold text-slate-200">
            No analysis data yet
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            In compliance with strict scientific integrity guidelines, this dashboard displays only authentic analysis activity. 
            No synthetic or fabricated statistics are displayed.
          </p>
          <div className="pt-2 flex justify-center gap-3">
            <button
              onClick={() => setActiveTab('text')}
              className="px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs tracking-wider transition-colors shadow-lg"
            >
              Analyze a Message
            </button>
            <button
              onClick={() => setActiveTab('voice')}
              className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-bold text-xs tracking-wider transition-colors"
            >
              Analyze Audio
            </button>
          </div>
        </div>
      ) : (
        /* Real Session Metrics Cards */
        <div className="space-y-8 animate-fadeIn">
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
            
            <div className="p-5 rounded-2xl glass-panel border border-slate-800">
              <div className="text-[11px] font-mono text-slate-400 uppercase">
                Total Analyses
              </div>
              <div className="text-3xl font-extrabold font-mono text-slate-100 mt-2">
                {stats.total_analyses}
              </div>
              <div className="text-[10px] text-slate-500 mt-1 font-mono">
                {stats.text_analyses} text / {stats.voice_analyses} voice
              </div>
            </div>

            <div className="p-5 rounded-2xl glass-panel border border-rose-500/30 bg-rose-950/20">
              <div className="text-[11px] font-mono text-rose-400 uppercase">
                Scam Detections
              </div>
              <div className="text-3xl font-extrabold font-mono text-rose-400 mt-2">
                {stats.scam_detections}
              </div>
              <div className="text-[10px] text-rose-300/70 mt-1 font-mono">
                {((stats.scam_detections / stats.total_analyses) * 100).toFixed(0)}% detection rate
              </div>
            </div>

            <div className="p-5 rounded-2xl glass-panel border border-purple-500/30 bg-purple-950/20">
              <div className="text-[11px] font-mono text-purple-400 uppercase">
                Digital Arrests
              </div>
              <div className="text-3xl font-extrabold font-mono text-purple-300 mt-2">
                {stats.digital_arrest_detections}
              </div>
              <div className="text-[10px] text-purple-300/70 mt-1 font-mono">
                Coercion patterns flagged
              </div>
            </div>

            <div className="p-5 rounded-2xl glass-panel border border-orange-500/30 bg-orange-950/20">
              <div className="text-[11px] font-mono text-orange-400 uppercase">
                High Risk Cases
              </div>
              <div className="text-3xl font-extrabold font-mono text-orange-400 mt-2">
                {stats.high_risk_detections}
              </div>
              <div className="text-[10px] text-orange-300/70 mt-1 font-mono">
                Risk score &gt; 50/100
              </div>
            </div>

            <div className="p-5 rounded-2xl glass-panel border border-cyan-500/30 bg-cyan-950/20">
              <div className="text-[11px] font-mono text-cyan-400 uppercase">
                Average Risk
              </div>
              <div className="text-3xl font-extrabold font-mono text-cyan-300 mt-2">
                {stats.avg_risk_score}
              </div>
              <div className="text-[10px] text-cyan-300/70 mt-1 font-mono">
                Out of 100 index
              </div>
            </div>

          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Chart 1: Risk Level Distribution */}
            <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <Activity className="w-4 h-4 text-cyan-400" />
                  <span>Risk Level Distribution</span>
                </h3>
                <span className="text-[11px] font-mono text-slate-500">Live Database</span>
              </div>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={stats.risk_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <XAxis dataKey="level" stroke="#64748B" fontSize={11} />
                    <YAxis stroke="#64748B" fontSize={11} allowDecimals={false} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                    />
                    <Bar dataKey="count" fill="#06B6D4" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 2: Scam Categories Breakdown */}
            <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-rose-400" />
                  <span>Scam Category Distribution</span>
                </h3>
                <span className="text-[11px] font-mono text-slate-500">Ground Truth Classes</span>
              </div>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={stats.category_distribution}
                      dataKey="count"
                      nameKey="category"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={({ name, percent }) => `${name.replace(/_/g, ' ')} (${(percent * 100).toFixed(0)}%)`}
                      labelLine={false}
                    >
                      {stats.category_distribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}
