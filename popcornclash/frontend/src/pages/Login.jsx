import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useGame } from '../context/GameStateContext';
import { api } from '../utils/backendApi';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setUser } = useGame();
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await api.auth.login({ email, password });
      localStorage.setItem('token', data.token);
      setUser({
        isAuthenticated: true,
        username: data.user.username,
        role: data.user.role,
        streak_count: data.user.prediction_streak,
        current_level: data.user.current_level,
        current_xp: data.user.total_xp,
        xp_to_next_level: 100,
        favorite_club: data.user.favorite_club,
      });
      navigate('/');
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 bg-pitch-card border border-gray-800 p-8 rounded-2xl shadow-gold-glow">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-black text-white uppercase tracking-wider mt-2">Sign In</h2>
      </div>
      {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 text-red-400 text-xs">{error}</div>}
      <form onSubmit={handleLoginSubmit} className="space-y-5">
        <div>
          <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Email Address</label>
          <input type="email" required value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-pitch-over border border-gray-800 focus:border-popcorn-gold outline-none p-3 rounded-lg text-sm text-white transition-all" />
        </div>
        <div>
          <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Password</label>
          <input type="password" required value={password} onChange={e => setPassword(e.target.value)} className="w-full bg-pitch-over border border-gray-800 focus:border-popcorn-gold outline-none p-3 rounded-lg text-sm text-white transition-all" />
        </div>
        <div className="text-right">
          <Link to="/forgot-password" className="text-xs text-popcorn-gold hover:underline">Forgot Password?</Link>
        </div>
        <button type="submit" disabled={loading} className="w-full py-3 bg-linear-to-r from-popcorn-gold to-popcorn-glow text-pitch-dark font-black rounded-lg text-sm uppercase tracking-wider shadow-md hover:opacity-90 active:scale-[0.99] transition-all disabled:opacity-50">
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
      <p className="text-center text-xs text-gray-400 mt-6">
        New here? <Link to="/signup" className="text-popcorn-gold font-bold hover:underline">Create Account</Link>
      </p>
    </div>
  );
}
