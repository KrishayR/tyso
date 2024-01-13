const projectId = "P2QCGhyesv6kk1BL2RGvh063o2gF"
const sdk = Descope({ projectId: projectId, persistTokens: true, autoRefresh: true })

const sessionToken = sdk.getSessionToken()

const refreshToken = sdk.getRefreshToken()
const validRefreshToken = refreshToken && !sdk.isJwtExpired(refreshToken)