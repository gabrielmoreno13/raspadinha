// Sistema de Afiliados - Tracking de Links e Comissões

class AffiliateSystem {
  constructor() {
    this.affiliates = this.loadAffiliates()
    this.conversions = this.loadConversions()
    this.deposits = this.loadDeposits()
  }

  // Carregar dados do localStorage
  loadAffiliates() {
    return JSON.parse(localStorage.getItem('raspadinha_affiliates') || '[]')
  }

  loadConversions() {
    return JSON.parse(localStorage.getItem('raspadinha_conversions') || '[]')
  }

  loadDeposits() {
    return JSON.parse(localStorage.getItem('raspadinha_deposits') || '[]')
  }

  // Salvar dados no localStorage
  saveAffiliates() {
    localStorage.setItem('raspadinha_affiliates', JSON.stringify(this.affiliates))
  }

  saveConversions() {
    localStorage.setItem('raspadinha_conversions', JSON.stringify(this.conversions))
  }

  saveDeposits() {
    localStorage.setItem('raspadinha_deposits', JSON.stringify(this.deposits))
  }

  // Gerar código de afiliado único
  generateAffiliateCode(name) {
    const cleanName = name.replace(/[^a-zA-Z0-9]/g, '').toUpperCase()
    const randomSuffix = Math.random().toString(36).substring(2, 8).toUpperCase()
    return `${cleanName.substring(0, 6)}${randomSuffix}`
  }

  // Registrar novo afiliado
  registerAffiliate(affiliateData) {
    const newAffiliate = {
      id: Date.now().toString(),
      code: this.generateAffiliateCode(affiliateData.name),
      name: affiliateData.name,
      email: affiliateData.email,
      phone: affiliateData.phone,
      instagram: affiliateData.instagram,
      pixKey: affiliateData.pixKey,
      pixKeyType: affiliateData.pixKeyType,
      commissionRate: 0.5, // 50% de comissão
      status: 'active',
      createdAt: new Date().toISOString(),
      totalEarnings: 0,
      totalConversions: 0,
      totalDeposits: 0,
      pendingPayment: 0,
      lastPayment: null
    }

    this.affiliates.push(newAffiliate)
    this.saveAffiliates()
    return newAffiliate
  }

  // Obter afiliado por código
  getAffiliateByCode(code) {
    return this.affiliates.find(affiliate => affiliate.code === code)
  }

  // Obter afiliado por ID
  getAffiliateById(id) {
    return this.affiliates.find(affiliate => affiliate.id === id)
  }

  // Gerar link de afiliado
  generateAffiliateLink(affiliateCode, baseUrl = window.location.origin) {
    return `${baseUrl}?ref=${affiliateCode}`
  }

  // Rastrear clique no link de afiliado
  trackClick(affiliateCode, userAgent = navigator.userAgent, ip = 'unknown') {
    const affiliate = this.getAffiliateByCode(affiliateCode)
    if (!affiliate) return false

    const click = {
      id: Date.now().toString(),
      affiliateId: affiliate.id,
      affiliateCode: affiliateCode,
      timestamp: new Date().toISOString(),
      userAgent,
      ip,
      converted: false
    }

    // Salvar no sessionStorage para rastrear conversão posterior
    sessionStorage.setItem('affiliate_click', JSON.stringify(click))
    
    return true
  }

  // Rastrear conversão (cadastro)
  trackConversion(userId, userEmail) {
    const clickData = JSON.parse(sessionStorage.getItem('affiliate_click') || 'null')
    if (!clickData) return false

    const affiliate = this.getAffiliateById(clickData.affiliateId)
    if (!affiliate) return false

    const conversion = {
      id: Date.now().toString(),
      affiliateId: affiliate.id,
      affiliateCode: affiliate.code,
      userId: userId,
      userEmail: userEmail,
      timestamp: new Date().toISOString(),
      clickId: clickData.id,
      status: 'converted'
    }

    this.conversions.push(conversion)
    this.saveConversions()

    // Atualizar estatísticas do afiliado
    affiliate.totalConversions += 1
    this.saveAffiliates()

    // Limpar dados de clique da sessão
    sessionStorage.removeItem('affiliate_click')

    return conversion
  }

  // Rastrear depósito e calcular comissão
  trackDeposit(userId, amount) {
    // Encontrar conversão do usuário
    const userConversion = this.conversions.find(conv => conv.userId === userId)
    if (!userConversion) return false

    const affiliate = this.getAffiliateById(userConversion.affiliateId)
    if (!affiliate) return false

    const commission = amount * affiliate.commissionRate
    
    const deposit = {
      id: Date.now().toString(),
      affiliateId: affiliate.id,
      affiliateCode: affiliate.code,
      userId: userId,
      amount: amount,
      commission: commission,
      timestamp: new Date().toISOString(),
      conversionId: userConversion.id,
      status: 'pending_payment'
    }

    this.deposits.push(deposit)
    this.saveDeposits()

    // Atualizar estatísticas do afiliado
    affiliate.totalDeposits += amount
    affiliate.totalEarnings += commission
    affiliate.pendingPayment += commission
    this.saveAffiliates()

    return deposit
  }

  // Obter estatísticas do afiliado
  getAffiliateStats(affiliateId) {
    const affiliate = this.getAffiliateById(affiliateId)
    if (!affiliate) return null

    const affiliateConversions = this.conversions.filter(conv => conv.affiliateId === affiliateId)
    const affiliateDeposits = this.deposits.filter(dep => dep.affiliateId === affiliateId)

    const today = new Date()
    const thisMonth = new Date(today.getFullYear(), today.getMonth(), 1)
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1)

    const thisMonthConversions = affiliateConversions.filter(conv => 
      new Date(conv.timestamp) >= thisMonth
    )
    const thisMonthDeposits = affiliateDeposits.filter(dep => 
      new Date(dep.timestamp) >= thisMonth
    )

    const thisMonthEarnings = thisMonthDeposits.reduce((sum, dep) => sum + dep.commission, 0)
    const thisMonthDepositAmount = thisMonthDeposits.reduce((sum, dep) => sum + dep.amount, 0)

    return {
      affiliate,
      totalStats: {
        conversions: affiliate.totalConversions,
        deposits: affiliate.totalDeposits,
        earnings: affiliate.totalEarnings,
        pendingPayment: affiliate.pendingPayment
      },
      thisMonth: {
        conversions: thisMonthConversions.length,
        deposits: thisMonthDepositAmount,
        earnings: thisMonthEarnings
      },
      recentConversions: affiliateConversions.slice(-10).reverse(),
      recentDeposits: affiliateDeposits.slice(-10).reverse()
    }
  }

  // Obter todos os afiliados (para admin)
  getAllAffiliates() {
    return this.affiliates.map(affiliate => {
      const stats = this.getAffiliateStats(affiliate.id)
      return {
        ...affiliate,
        stats: stats.totalStats
      }
    })
  }

  // Processar pagamento de comissão
  processPayment(affiliateId, amount) {
    const affiliate = this.getAffiliateById(affiliateId)
    if (!affiliate) return false

    if (amount > affiliate.pendingPayment) return false

    const payment = {
      id: Date.now().toString(),
      affiliateId: affiliateId,
      amount: amount,
      timestamp: new Date().toISOString(),
      status: 'paid',
      method: 'pix',
      pixKey: affiliate.pixKey
    }

    // Atualizar saldo do afiliado
    affiliate.pendingPayment -= amount
    affiliate.lastPayment = payment
    this.saveAffiliates()

    // Atualizar status dos depósitos pagos
    const depositsToUpdate = this.deposits.filter(dep => 
      dep.affiliateId === affiliateId && dep.status === 'pending_payment'
    )

    let remainingAmount = amount
    depositsToUpdate.forEach(deposit => {
      if (remainingAmount >= deposit.commission) {
        deposit.status = 'paid'
        deposit.paidAt = new Date().toISOString()
        remainingAmount -= deposit.commission
      }
    })

    this.saveDeposits()
    return payment
  }

  // Obter relatório geral (para admin)
  getGeneralReport() {
    const totalAffiliates = this.affiliates.length
    const activeAffiliates = this.affiliates.filter(aff => aff.status === 'active').length
    const totalConversions = this.conversions.length
    const totalDeposits = this.deposits.reduce((sum, dep) => sum + dep.amount, 0)
    const totalCommissions = this.deposits.reduce((sum, dep) => sum + dep.commission, 0)
    const pendingPayments = this.affiliates.reduce((sum, aff) => sum + aff.pendingPayment, 0)

    const today = new Date()
    const thisMonth = new Date(today.getFullYear(), today.getMonth(), 1)

    const thisMonthConversions = this.conversions.filter(conv => 
      new Date(conv.timestamp) >= thisMonth
    ).length

    const thisMonthDeposits = this.deposits.filter(dep => 
      new Date(dep.timestamp) >= thisMonth
    ).reduce((sum, dep) => sum + dep.amount, 0)

    const thisMonthCommissions = this.deposits.filter(dep => 
      new Date(dep.timestamp) >= thisMonth
    ).reduce((sum, dep) => sum + dep.commission, 0)

    return {
      overview: {
        totalAffiliates,
        activeAffiliates,
        totalConversions,
        totalDeposits,
        totalCommissions,
        pendingPayments
      },
      thisMonth: {
        conversions: thisMonthConversions,
        deposits: thisMonthDeposits,
        commissions: thisMonthCommissions
      },
      topAffiliates: this.affiliates
        .sort((a, b) => b.totalEarnings - a.totalEarnings)
        .slice(0, 10),
      recentActivity: {
        conversions: this.conversions.slice(-20).reverse(),
        deposits: this.deposits.slice(-20).reverse()
      }
    }
  }
}

// Instância global do sistema de afiliados
export const affiliateSystem = new AffiliateSystem()

// Função para inicializar tracking de afiliado na página
export const initAffiliateTracking = () => {
  const urlParams = new URLSearchParams(window.location.search)
  const refCode = urlParams.get('ref')
  
  if (refCode) {
    affiliateSystem.trackClick(refCode)
    
    // Remover parâmetro ref da URL sem recarregar a página
    const newUrl = window.location.pathname + window.location.hash
    window.history.replaceState({}, document.title, newUrl)
  }
}

// Função para rastrear conversão após cadastro
export const trackAffiliateConversion = (userId, userEmail) => {
  return affiliateSystem.trackConversion(userId, userEmail)
}

// Função para rastrear depósito
export const trackAffiliateDeposit = (userId, amount) => {
  return affiliateSystem.trackDeposit(userId, amount)
}

export default affiliateSystem

