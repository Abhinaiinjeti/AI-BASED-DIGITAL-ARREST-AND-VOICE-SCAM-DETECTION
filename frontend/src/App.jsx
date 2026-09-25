import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import TextAnalysis from './pages/TextAnalysis';
import VoiceAnalysis from './pages/VoiceAnalysis';
import Dashboard from './pages/Dashboard';
import HistoryPage from './pages/History';
import HowItWorks from './pages/HowItWorks';
import About from './pages/About';
import { checkBackendHealth } from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [backendStatus, setBackendStatus] = useState({ online: false, data: null });

  useEffect(() => {
    const pingBackend = async () => {
      const res = await checkBackendHealth();
      if (res.status === 'online') {
        setBackendStatus({ online: true, data: res });
      } else {
        setBackendStatus({ online: false, data: null });
      }
    };

    pingBackend();
    const interval = setInterval(pingBackend, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#080C14] text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      
      {/* Dynamic Cyber Grid Background */}
      <div 
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: `radial-gradient(rgba(6, 182, 212, 0.15) 1px, transparent 1px)`,
          backgroundSize: '32px 32px',
        }}
      />

      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        backendStatus={backendStatus}
      />

      {/* Main Content Area */}
      <main className="flex-1 relative z-10">
        {activeTab === 'home' && (
          <Home
            setActiveTab={setActiveTab}
            backendStatus={backendStatus}
          />
        )}
        {activeTab === 'text' && <TextAnalysis />}
        {activeTab === 'voice' && <VoiceAnalysis />}
        {activeTab === 'dashboard' && <Dashboard setActiveTab={setActiveTab} />}
        {activeTab === 'history' && <HistoryPage />}
        {activeTab === 'how-it-works' && <HowItWorks />}
        {activeTab === 'about' && <About />}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
