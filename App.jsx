import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import PreparePage from './pages/PreparePage';
import RelationshipTimeline from './components/RelationshipTimeline';
import CommitmentTracker from './components/CommitmentTracker';
import MemoryExplorer from './components/MemoryExplorer';
import SettingsPanel from './components/SettingsPanel';

export default function App() {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('memora_user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedContactId, setSelectedContactId] = useState('c1');

  const handleLogin = (userData) => {
    setUser(userData);
    try {
      localStorage.setItem('memora_user', JSON.stringify(userData));
    } catch (e) {
      console.error(e);
    }
  };

  const handleLogout = () => {
    setUser(null);
    try {
      localStorage.removeItem('memora_user');
    } catch (e) {
      console.error(e);
    }
  };

  if (!user) {
    return <LoginPage onLogin={handleLogin} />;
  }

  const handleNavigateToPrepare = (contactId) => {
    setSelectedContactId(contactId || 'c1');
    setActiveTab('prepare');
  };

  const handleSelectContact = (contactId, targetTab) => {
    setSelectedContactId(contactId);
    setActiveTab(targetTab || 'timeline');
  };

  return (
    <div className="min-h-screen bg-[#FAFAFC] flex flex-col">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onLogout={handleLogout}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && (
          <DashboardPage
            user={user}
            onNavigateToPrepare={handleNavigateToPrepare}
            onSelectContact={handleSelectContact}
          />
        )}

        {activeTab === 'prepare' && (
          <PreparePage
            initialContactId={selectedContactId}
            onBack={() => setActiveTab('dashboard')}
          />
        )}

        {activeTab === 'timeline' && (
          <RelationshipTimeline contactId={selectedContactId} />
        )}

        {activeTab === 'commitments' && (
          <CommitmentTracker />
        )}

        {activeTab === 'explorer' && (
          <MemoryExplorer contactId={selectedContactId} />
        )}

        {activeTab === 'settings' && (
          <SettingsPanel contactId={selectedContactId} />
        )}
      </main>

      <footer className="bg-white border-t border-slate-100 py-6 text-center text-xs text-slate-400 font-medium">
        <p>MEMORA — AI Relationship Memory & Meeting Intelligence Agent • Built for Hackathon with Hindsight (Vectorize)</p>
      </footer>
    </div>
  );
}
