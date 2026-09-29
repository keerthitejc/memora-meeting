import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Calendar, Clock, User, ArrowRight, Brain, CheckSquare, Layers, AlertCircle } from 'lucide-react';
import { fetchStats, fetchNextMeeting, fetchContacts } from '../services/api';

export default function DashboardPage({ user, onNavigateToPrepare, onSelectContact }) {
  const [stats, setStats] = useState(null);
  const [nextMeeting, setNextMeeting] = useState(null);
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    fetchStats().then(setStats);
    fetchNextMeeting().then(setNextMeeting);
    fetchContacts().then(setContacts);
  }, []);

  return (
    <div className="space-y-8">
      {/* Greeting Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-indigo-900 via-indigo-800 to-violet-900 p-8 rounded-3xl text-white shadow-card relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none" />
        
        <div className="relative z-10">
          <div className="flex items-center space-x-2 text-indigo-200 text-xs font-bold uppercase tracking-wider mb-2">
            <Sparkles className="w-4 h-4 text-teal-400" />
            <span>Autonomous Intelligence Agent Active</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome back, {user?.name || "Alex"} 👋
          </h1>
          <p className="text-xs sm:text-sm text-indigo-200 mt-1 max-w-xl font-medium leading-relaxed">
            MEMORA has continuously retained your interaction memory across meetings, Slack updates, and promised deliverables.
          </p>
        </div>

        <button
          onClick={() => onNavigateToPrepare(nextMeeting?.contact_id || "c1")}
          className="relative z-10 px-6 py-3.5 rounded-2xl bg-white text-indigo-900 hover:bg-indigo-50 text-xs font-extrabold shadow-lg transition flex items-center space-x-2 group"
        >
          <Brain className="w-5 h-5 text-indigo-600 group-hover:scale-110 transition" />
          <span>✨ Prepare Me for Next Meeting</span>
          <ArrowRight className="w-4 h-4 text-indigo-600 group-hover:translate-x-1 transition" />
        </button>
      </div>

      {/* Relationship Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-soft flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-indigo-50 text-indigo-600">
            <User className="w-6 h-6" />
          </div>
          <div>
            <span className="text-2xl font-extrabold text-slate-900">{stats?.total_contacts || 3}</span>
            <p className="text-xs text-slate-500 font-semibold">Active Contacts</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-soft flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-teal-50 text-teal-600">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <span className="text-2xl font-extrabold text-slate-900">{stats?.total_memories || 42}</span>
            <p className="text-xs text-slate-500 font-semibold">Retained Memory Units</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-soft flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-amber-50 text-amber-600">
            <CheckSquare className="w-6 h-6" />
          </div>
          <div>
            <span className="text-2xl font-extrabold text-slate-900">{stats?.open_commitments || 4}</span>
            <p className="text-xs text-slate-500 font-semibold">Open Commitments</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-soft flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-red-50 text-red-600">
            <AlertCircle className="w-6 h-6" />
          </div>
          <div>
            <span className="text-2xl font-extrabold text-slate-900">{stats?.overdue_count || 1}</span>
            <p className="text-xs text-slate-500 font-semibold">Overdue Promises</p>
          </div>
        </div>
      </div>

      {/* Next Meeting Hero Card */}
      {nextMeeting && (
        <div className="bg-white rounded-3xl p-8 border border-indigo-100 shadow-card relative overflow-hidden">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <span className="text-[11px] font-extrabold px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 uppercase tracking-wider">
                  Hero Meeting
                </span>
                <span className="text-xs text-slate-400 font-semibold flex items-center space-x-1">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{nextMeeting.time}</span>
                </span>
              </div>

              <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900">
                {nextMeeting.title}
              </h2>

              <p className="text-xs text-slate-600 font-medium max-w-2xl leading-relaxed">
                Agenda: {nextMeeting.agenda}
              </p>

              {/* Contact Pill */}
              <div className="flex items-center space-x-3 pt-2">
                <img
                  src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=128&q=80"
                  alt="Rahul Sharma"
                  className="w-10 h-10 rounded-full border border-indigo-200 object-cover"
                />
                <div>
                  <h4 className="text-xs font-bold text-slate-900">{nextMeeting.contact_name}</h4>
                  <p className="text-[10px] text-slate-500 font-semibold">VP Engineering & Product Lead @ Acme Cloud</p>
                </div>
              </div>
            </div>

            {/* Action CTA */}
            <div className="flex flex-col items-end justify-center space-y-3">
              <button
                onClick={() => onNavigateToPrepare(nextMeeting.contact_id)}
                className="px-6 py-3.5 rounded-2xl gradient-bg text-white text-xs font-extrabold shadow-md hover:shadow-lg transition flex items-center space-x-2"
              >
                <Brain className="w-4 h-4" />
                <span>✨ Prepare Me (Run Hindsight Agent)</span>
              </button>
              <span className="text-[10px] text-slate-400 font-medium">
                Recalls history + reflects on decision pivots
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Relationship Contacts Grid */}
      <div>
        <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-900 mb-4">
          Relationship Memory Banks ({contacts.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {contacts.map((contact) => (
            <div
              key={contact.id}
              className="bg-white p-6 rounded-2xl border border-slate-100 shadow-soft hover:shadow-md transition duration-200 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <img
                    src={contact.avatar}
                    alt={contact.name}
                    className="w-12 h-12 rounded-full border border-slate-200 object-cover"
                  />
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">{contact.name}</h4>
                    <p className="text-xs text-slate-500 font-medium">{contact.role}</p>
                    <p className="text-[10px] text-indigo-600 font-bold">{contact.company}</p>
                  </div>
                </div>

                <div className="space-y-1.5 text-xs text-slate-600 font-medium bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-400">Status:</span>
                    <span className="font-bold text-slate-700">{contact.relationship_status}</span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-400">Hindsight Bank:</span>
                    <span className="font-mono text-teal-700 font-semibold">{contact.bank_id}</span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between">
                <button
                  onClick={() => onNavigateToPrepare(contact.id)}
                  className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center space-x-1"
                >
                  <span>✨ Prepare Me</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>

                <button
                  onClick={() => onSelectContact(contact.id, 'timeline')}
                  className="text-xs font-semibold text-slate-500 hover:text-slate-800"
                >
                  History
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
