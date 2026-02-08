export interface JWTClaims {
  sub: string;
  exp: number;
  iat: number;
  user_id: string;
}

export interface AuthUser {
  userId: string;
  isAuthenticated: boolean;
}

export interface LoginCredentials {
  userId: string;
  password: string;
}

export interface SignupCredentials {
  userId: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  user_id: string;
  token_type: string;
}
