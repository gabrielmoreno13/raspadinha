import { useState } from 'react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'

export default function LoginModal({ onClose, onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLogin, setIsLogin] = useState(true)

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Simular login bem-sucedido
    if (email && password) {
      onLogin(email, password)
      onClose()
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4 relative">
        {/* Close Button */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
        >
          ✕
        </button>

        {/* Tabs */}
        <div className="flex mb-6">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 px-4 rounded-l-lg border ${
              isLogin 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'bg-gray-700 text-gray-300 border-gray-600'
            }`}
          >
            Entrar
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 px-4 rounded-r-lg border ${
              !isLogin 
                ? 'bg-yellow-600 text-white border-yellow-600' 
                : 'bg-gray-700 text-gray-300 border-gray-600'
            }`}
          >
            Registrar
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="email" className="text-white">
              E-mail *
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="Seu e-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-gray-700 border-gray-600 text-white placeholder-gray-400"
              required
            />
          </div>

          <div>
            <Label htmlFor="password" className="text-white flex justify-between">
              Senha *
              {isLogin && (
                <span className="text-blue-400 text-sm cursor-pointer hover:underline">
                  Esqueceu a senha?
                </span>
              )}
            </Label>
            <Input
              id="password"
              type="password"
              placeholder="Sua senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-gray-700 border-gray-600 text-white placeholder-gray-400"
              required
            />
          </div>

          {isLogin && (
            <div className="flex items-center space-x-2">
              <input 
                type="checkbox" 
                id="remember" 
                className="rounded border-gray-600 bg-gray-700"
              />
              <Label htmlFor="remember" className="text-gray-300 text-sm">
                Lembrar de mim
              </Label>
            </div>
          )}

          <Button 
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium"
          >
            {isLogin ? 'Entrar' : 'Registrar'}
          </Button>

          <div className="text-center text-sm text-gray-400">
            Ao prosseguir, você concorda com nossos{' '}
            <span className="text-blue-400 cursor-pointer hover:underline">
              Termos de Uso
            </span>
          </div>
        </form>

        {/* Demo Account Info */}
        {isLogin && (
          <div className="mt-6 p-4 bg-gray-700 rounded-lg">
            <h4 className="text-green-400 font-medium mb-2">
              🎮 Conta de Demonstração
            </h4>
            <p className="text-gray-300 text-sm mb-2">
              Use estas credenciais para testar:
            </p>
            <div className="text-sm space-y-1">
              <div>
                <strong className="text-white">Email:</strong>{' '}
                <span className="text-green-400">demo@raspadinha.com</span>
              </div>
              <div>
                <strong className="text-white">Senha:</strong>{' '}
                <span className="text-green-400">demo123456</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

