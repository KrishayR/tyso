const projectId = "Use Own ID from descope"
const sdk = Descope({ projectId: projectId, persistTokens: true, autoRefresh: true })

const sessionToken = sdk.getSessionToken()

const refreshToken = sdk.getRefreshToken()
const validRefreshToken = refreshToken && !sdk.isJwtExpired(refreshToken)
