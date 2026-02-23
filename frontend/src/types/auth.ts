export type User = {
  id: string;
  role: string;
  full_name: string;
  email: string;
  phone: string;
  is_active: boolean;
  created_at: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: string;
  user: User;
};
