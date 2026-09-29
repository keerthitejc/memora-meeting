import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, ArrowRight, Sparkles, UserCheck, Lock, Mail, UserPlus, LogIn, AlertCircle } from 'lucide-react';
import { loginUser, registerUser } from '../services/api';

export default function LoginPage({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('judge@hackathon.com');
  const [password, setPassword] = useState('demo123');
  const [name, setName] = useState('Hackathon Judge');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegister) {
        const res = await registerUser(email, password, name);
        onLogin(res.user);
      } else {
        const res = await loginUser(email, password);
        onLogin(res.user);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Authentication failed. Check details or server status.");
    } finally {
      setLoading(false);
    }
  };

  const handleGuestLogin = () => {
    onLogin({
      id: 'guest_judge',
      name: 'Guest / Demo Judge',
      email: 'judge@memora.ai',
      role: 'Judge',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=128&q=80'
    });
  };

  return (
    <div className="min-h-screen bg-[#FAFAFC] flex items-center justify-center relative overflow-hidden px-4 py-8">
      {/* Background Soft Blurred Gradient Blobs */}
      <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-gradient-to-br from-indigo-400/20 to-violet-500/20 blur-3xl pointer-events-none" />
      <div className="absolute -bottom-32 -right-32 w-96 h-96 rounded-full bg-gradient-to-tr from-teal-400/20 to-indigo-500/20 blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full bg-violet-300/10 blur-3xl pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 15 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md bg-white rounded-3xl p-8 border border-slate-100 shadow-card relative z-10"
      >
        {/* Logo & Header */}
        <div className="text-center mb-6">
          <div className="w-14 h-14 mx-auto rounded-2xl gradient-bg flex items-center justify-center text-white shadow-lg shadow-indigo-200 mb-3">
            <Brain className="w-8 h-8 animate-pulse-slow" />
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight gradient-text">MEMORA</h1>
          <p className="text-xs text-slate-500 font-semibold mt-1">
            AI Relationship Memory & Meeting Intelligence Agent
          </p>
          <div className="inline-flex items-center space-x-1.5 mt-3 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-700 text-[11px] font-bold">
            <Sparkles className="w-3.5 h-3.5 text-teal-600" />
            <span>Powered by Hindsight Engine</span>
          </div>
        </div>

        {/* Mode Toggle Tabs */}
        <div className="flex bg-slate-100 p-1 rounded-xl mb-6">
          <button
            type="button"
            onClick={() => { setIsRegister(false); setError(''); }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition flex items-center justify-center space-x-1.5 ${
              !isRegister ? 'bg-white text-indigo-700 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </button>
          <button
            type="button"
            onClick={() => { setIsRegister(true); setError(''); }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition flex items-center justify-center space-x-1.5 ${
              isRegister ? 'bg-white text-indigo-700 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Create Account</span>
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-semibold flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                Full Name
              </label>
              <div className="relative">
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Alex Rivera"
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Email / Gmail Address
            </label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="user@gmail.com"
                className="w-full px-4 py-3 rounded-xl border border-slate-200 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Password
            </label>
            <div className="relative">
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-xl border border-slate-200 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
              />
            </div>
          </div>

          {/* Primary CTA */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-xl gradient-bg text-white text-xs font-bold tracking-wide shadow-md hover:opacity-95 transition flex items-center justify-center space-x-2 group disabled:opacity-50"
          >
            {loading ? (
              <span>Connecting to Database...</span>
            ) : (
              <>
                <span>{isRegister ? "Create Account & Continue" : "Sign In with Password"}</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition" />
              </>
            )}
          </button>
        </form>

        {/* Divider */}
        <div className="relative my-6 text-center">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-100"></div></div>
          <span className="relative bg-white px-3 text-[10px] uppercase font-bold text-slate-400">Hackathon Quick Access</span>
        </div>

        {/* One-Click Guest Demo Button */}
        <button
          type="button"
          onClick={handleGuestLogin}
          className="w-full py-3 rounded-xl bg-slate-50 hover:bg-indigo-50 border border-slate-200 hover:border-indigo-300 text-indigo-700 text-xs font-bold transition flex items-center justify-center space-x-2 shadow-2xs"
        >
          <UserCheck className="w-4 h-4 text-indigo-600" />
          <span>⚡ Try Demo (One-Click Guest Login)</span>
        </button>

        <p className="text-[11px] text-slate-400 text-center mt-6">
          "Most meeting assistants remember the meeting. MEMORA remembers the relationship."
        </p>
      </motion.div>
    </div>
  );
}
