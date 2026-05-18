import { useState } from 'react'
import { AuthContext } from '../hooks/useAuth'
import '../styles/auth.css'

interface LoginProps {
  auth: AuthContext
  onLoginSuccess: () => void
}

export default function Login({ auth, onLoginSuccess }: LoginProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showRegister, setShowRegister] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await auth.login(email, password)
      onLoginSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await auth.register(email, password)
      onLoginSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
    } finally {
      setIsLoading(false)
    }
  }

  if (showRegister) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <span className="auth-icon">⊕</span>
            <h1>Create Account</h1>
            <p>Join Cartograph to save routes and track exploration</p>
          </div>

          <form onSubmit={handleRegister} className="auth-form">
            <div className="auth-field">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="auth-field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {error && <div className="auth-error">{error}</div>}

            <button type="submit" className="auth-submit" disabled={isLoading}>
              {isLoading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <div className="auth-footer">
            <p>
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => {
                  setShowRegister(false)
                  setError('')
                }}
                className="auth-link"
              >
                Sign in
              </button>
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <span className="auth-icon">⊕</span>
          <h1>Welcome to Cartograph</h1>
          <p>Sign in to save routes and explore Chelsea & Gatineau Park</p>
        </div>

        <form onSubmit={handleLogin} className="auth-form">
          <div className="auth-field">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="auth-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="auth-error">{error}</div>}

          <button type="submit" className="auth-submit" disabled={isLoading}>
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account?{' '}
            <button
              type="button"
              onClick={() => {
                setShowRegister(true)
                setError('')
              }}
              className="auth-link"
            >
              Create one
            </button>
          </p>
          <p className="auth-note">
            🔒 Privacy first: No tracking, no ads, fully open source
          </p>
        </div>
      </div>
    </div>
  )
}
