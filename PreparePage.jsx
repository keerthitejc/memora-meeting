import React, { useState, useEffect } from 'react';
import { Brain, ToggleLeft, ToggleRight, Sparkles, RefreshCw, User, ShieldAlert, ArrowLeft } from 'lucide-react';
import PipelineAnimation from '../components/PipelineAnimation';
import BriefingView from '../components/BriefingView';
import { prepareMeeting, fetchContacts } from '../services/api';

export default function PreparePage({ initialContactId = "c1", onBack }) {
  const [contacts, setContacts] = useState([]);
  const [selectedContactId, setSelectedContactId] = useState(initialContactId);
  const [memoryOn, setMemoryOn] = useState(true);
  
  const [loading, setLoading] = useState(false);
  const [pipelineSteps, setPipelineSteps] = useState([]);
  const [briefing, setBriefing] = useState(null);

  useEffect(() => {
    if (initialContactId) {
      setSelectedContactId(initialContactId);
    }
  }, [initialContactId]);

  useEffect(() => {
    fetchContacts().then((data) => {
      setContacts(data);
      if (data.length > 0 && !selectedContactId) {
        setSelectedContactId(data[0].id);
      }
    });
  }, []);

  const runPrepare = async (contactId = selectedContactId, useMemory = memoryOn) => {
    setLoading(true);
    setBriefing(null);

    // Initial step setup for animated pipeline
    if (useMemory) {
      setPipelineSteps([
        { step: "recall", status: "in_progress", label: "1. Hindsight Recall", detail: "Querying multi-strategy memory index (semantic + keyword + temporal)..." },
        { step: "reflect", status: "pending", label: "2. Hindsight Reflect", detail: "Synthesizing relationship trajectory & decision shifts..." },
        { step: "brief", status: "pending", label: "3. Build Briefing", detail: "Groq LLM turning reflection into structured brief..." }
      ]);
    } else {
      setPipelineSteps([
        { step: "bypass", status: "completed", label: "Memory OFF Mode", detail: "Bypassing Hindsight memory bank. Generic LLM call only." }
      ]);
    }

    try {
      // Simulate step-by-step pipeline progression for visual demo clarity
      if (useMemory) {
        await new Promise(r => setTimeout(r, 600));
        setPipelineSteps(prev => [
          { ...prev[0], status: "completed", result: "Retrieved 3 memory units & interaction history." },
          { ...prev[1], status: "in_progress" },
          prev[2]
        ]);
        
        await new Promise(r => setTimeout(r, 700));
        setPipelineSteps(prev => [
          prev[0],
          { ...prev[1], status: "completed", result: "Reflected on OpenAPI delay & OAuth2 to API Key shift." },
          { ...prev[2], status: "in_progress" }
        ]);
      }

      const res = await prepareMeeting(contactId, useMemory);
      setBriefing(res.briefing);

      if (useMemory) {
        setPipelineSteps(prev => [
          prev[0],
          prev[1],
          { ...prev[2], status: "completed", result: "Grounded briefing object generated successfully." }
        ]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedContactId) {
      runPrepare(selectedContactId, memoryOn);
    }
  }, [selectedContactId]);

  const handleToggleMemory = () => {
    const nextState = !memoryOn;
    setMemoryOn(nextState);
    runPrepare(selectedContactId, nextState);
  };

  const selectedContact = contacts.find(c => c.id === selectedContactId) || contacts[0];

  return (
    <div className="space-y-8">
      {/* Navigation & Controls Bar */}
      <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-soft flex flex-wrap items-center justify-between gap-4">
        
        {/* Contact Selector */}
        <div className="flex items-center space-x-3">
          {onBack && (
            <button onClick={onBack} className="p-2 rounded-xl text-slate-400 hover:bg-slate-100 transition">
              <ArrowLeft className="w-5 h-5" />
            </button>
          )}

          <div className="w-11 h-11 rounded-2xl gradient-bg flex items-center justify-center text-white shadow-md">
            <Brain className="w-6 h-6 animate-pulse-slow" />
          </div>

          <div>
            <span className="text-[10px] font-extrabold uppercase text-indigo-600 tracking-wider">
              Autonomous Agent Mode
            </span>
            <div className="flex items-center space-x-2">
              <select
                value={selectedContactId}
                onChange={(e) => setSelectedContactId(e.target.value)}
                className="font-extrabold text-base text-slate-900 bg-transparent border-none focus:outline-none cursor-pointer"
              >
                {contacts.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.company})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* High-Leverage Memory ON vs OFF Toggle */}
        <div className="flex items-center space-x-4 bg-slate-50 p-2 rounded-2xl border border-slate-200/80">
          <div className="text-right">
            <span className="text-xs font-bold text-slate-800 block">
              {memoryOn ? "Memory ON" : "Memory OFF"}
            </span>
            <span className="text-[10px] text-slate-500 font-medium">
              {memoryOn ? "Hindsight Grounded" : "Generic LLM Prompt"}
            </span>
          </div>

          <button
            onClick={handleToggleMemory}
            className={`p-1.5 rounded-xl transition duration-200 flex items-center ${
              memoryOn ? 'bg-indigo-600 text-white shadow-md' : 'bg-slate-300 text-slate-600'
            }`}
          >
            {memoryOn ? <ToggleRight className="w-8 h-8" /> : <ToggleLeft className="w-8 h-8" />}
          </button>
        </div>
      </div>

      {/* Centerpiece Animated Agent Pipeline */}
      <PipelineAnimation steps={pipelineSteps} isRunning={loading} />

      {/* Grounded Brief Output */}
      {briefing && (
        <BriefingView briefing={briefing} contactId={selectedContactId} memoryOn={memoryOn} />
      )}
    </div>
  );
}
