import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from './ui/button'
import LoginModal from './LoginModal'

export default function Header({ user, balance, isLoggedIn, onLogout }) {
  const [showLoginModal, setShowLoginModal] = useState(false)

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value || 0)
  }

  const handleLogin = (email, password) => {
    // Simular login bem-sucedido
    const userData = {
      name: 'Gabriel Henrique Braga Miguel',
      email: email,
      balance: 10.00
    }
    
    localStorage.setItem('raspadinha_user', JSON.stringify(userData))
    window.location.reload() // Recarregar para atualizar estado
  }

  return (
    <>
      <header className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="text-2xl font-bold">
                <span className="text-white">RASPADINHA</span>
                <span className="text-green-400 block text-xs">DA SORTE</span>
              </div>
            </Link>

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-1">
              <Button 
                variant="ghost" 
                className="text-white hover:bg-gray-800 hover:text-green-400 px-4 py-2 rounded-lg border border-green-400"
              >
                <span className="mr-2">🏠</span>
                Início
              </Button>
              
              <Button 
                variant="ghost" 
                className="text-white hover:bg-gray-800 hover:text-blue-400 px-4 py-2 rounded-lg border border-blue-400"
              >
                <span className="mr-2">🎮</span>
                Raspadinhas
              </Button>
              
              <Button 
                variant="ghost" 
                className="text-white hover:bg-gray-800 hover:text-yellow-400 px-4 py-2 rounded-lg border border-yellow-400"
              >
                <span className="mr-2">🏆</span>
                Prêmios
              </Button>
            </nav>

            {/* User Actions */}
            <div className="flex items-center space-x-2">
              {isLoggedIn ? (
                <>
                  {/* Deposit Button */}
                  <Button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
                    <span className="mr-2">💰</span>
                    Depositar
                  </Button>
                  
                  {/* Withdraw Button */}
                  <Button className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
                    <span className="mr-2">💸</span>
                    Sacar
                  </Button>
                  
                  {/* User Profile */}
                  <div className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg cursor-pointer flex items-center space-x-2">
                    <div className="text-right">
                      <div className="text-white font-medium text-sm">
                        {user?.name || 'Usuário'}
                      </div>
                      <div className="text-purple-200 text-xs">
                        {formatCurrency(balance)}
                      </div>
                    </div>
                    <div className="w-8 h-8 bg-purple-800 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">
                        {user?.name?.charAt(0) || 'U'}
                      </span>
                    </div>
                  </div>
                </>
              ) : (
                <>
                  {/* Login Button */}
                  <Button 
                    onClick={() => setShowLoginModal(true)}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg"
                  >
                    Entrar
                  </Button>
                  
                  {/* Register Button */}
                  <Button className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg">
                    Registrar
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Login Modal */}
      {showLoginModal && (
        <LoginModal 
          onClose={() => setShowLoginModal(false)}
          onLogin={handleLogin}
        />
      )}
    </>
  )
}

