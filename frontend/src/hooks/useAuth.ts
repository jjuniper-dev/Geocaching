import { useState, useCallback, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_KEY = 'cartograph_token'

export interface AuthUser {
  id: number
  email: string
  preferences: Record<string, any>
  created_at: string
}

export interface AuthContext {
  user: AuthUser | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
  getToken: () => string | null
}

export function useAuth(): AuthContext {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check if user is already logged in on mount
  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token) {
      fetchCurrentUser(token)
    } else {
      setIsLoading(false)
    }
  }, [])

  const fetchCurrentUser = async (token: string) => {
    try {
      const response = await fetch(`${API_BASE}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
      localStorage.removeItem(TOKEN_KEY)
    } finally {
      setIsLoading(false)
    }
  }

  const register = useCallback(
    async (email: string, password: string) => {
      setIsLoading(true)
      try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Registration failed')
        }
        const userData = await response.json()
        setUser(userData)

        // Now login to get token
        const loginResponse = await fetch(`${API_BASE}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })
        if (!loginResponse.ok) {
          throw new Error('Login after registration failed')
        }
        const { access_token } = await loginResponse.json()
        localStorage.setItem(TOKEN_KEY, access_token)
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const login = useCallback(
    async (email: string, password: string) => {
      setIsLoading(true)
      try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Login failed')
        }
        const { access_token } = await response.json()
        localStorage.setItem(TOKEN_KEY, access_token)

        // Fetch user info
        await fetchCurrentUser(access_token)
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setUser(null)
  }, [])

  const getToken = useCallback(() => {
    return localStorage.getItem(TOKEN_KEY)
  }, [])

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    getToken,
  }
}
